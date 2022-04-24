import json
import re
import uuid
from datetime import datetime
from random import randint
from classquiz.helpers import get_meili_data
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import ValidationError
import bleach

from classquiz.auth import get_current_user
from classquiz.config import redis, settings, storage, meilisearch
from classquiz.db.models import Quiz, QuizInput, User, PlayGame
from classquiz.kahoot_importer.import_quiz import import_quiz
import html

settings = settings()

router = APIRouter()


@router.post("/create")
async def create_quiz_lol(quiz_input: QuizInput, user: User = Depends(get_current_user)):
    imgur_regex = r"^https://i\.imgur\.com\/.{7}.(jpg|png|gif)$"
    server_regex = rf"^{settings.root_address}/api/v1/storage/download/.{36}--.{36}$"
    quiz_input.title = html.unescape(bleach.clean(quiz_input.title, tags=[], strip=True))
    quiz_input.description = html.unescape(bleach.clean(quiz_input.description, tags=[], strip=True))
    for question in quiz_input.questions:
        if question.image == "":
            question.image = None
        if (
            question.image is not None
            and not re.match(imgur_regex, question.image)
            and not re.match(server_regex, question.image)
        ):
            raise HTTPException(status_code=400, detail="image url is not valid")
    quiz = Quiz(**quiz_input.dict(), user_id=user.id, id=uuid.uuid4())
    await redis.delete("global_quiz_count")
    if quiz_input.public:
        meilisearch.index(settings.meilisearch_index).add_documents([await get_meili_data(quiz)])
    return await quiz.save()


@router.get("/get/{quiz_id}")
async def get_quiz_from_id(quiz_id: str, user: User | None = Depends(get_current_user)):
    try:
        quiz_id = uuid.UUID(quiz_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="badly formed quiz id")
    if user is None:
        quiz = await Quiz.objects.get_or_none(id=quiz_id, public=True)
    else:
        quiz = await Quiz.objects.get_or_none(id=quiz_id, user_id=user.id)
    if quiz is None:
        public_quiz = await Quiz.objects.get_or_none(id=quiz_id, public=True)
        if public_quiz is None:
            return JSONResponse(status_code=404, content={"detail": "quiz not found"})
        else:
            return public_quiz
    else:
        return quiz


@router.get("/get/public/{quiz_id}", response_model=Quiz)
async def get_public_quiz(quiz_id: str):
    try:
        quiz_id = uuid.UUID(quiz_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="badly formed quiz id")
    quiz = await Quiz.objects.get_or_none(id=quiz_id, public=True)
    if quiz is None:
        return JSONResponse(status_code=404, content={"detail": "quiz not found"})
    else:
        return quiz


@router.post("/start/{quiz_id}")
async def start_quiz(quiz_id: str, user: User = Depends(get_current_user)):
    try:
        quiz_id = uuid.UUID(quiz_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="badly formed quiz id")
    quiz = await Quiz.objects.get_or_none(id=quiz_id, user_id=user.id)
    if quiz is None:
        quiz = await Quiz.objects.get_or_none(id=quiz_id, public=True)
        if quiz is None:
            return JSONResponse(status_code=404, content={"detail": "quiz not found"})
    game_pin = randint(10000000, 99999999)
    game = PlayGame(
        quiz_id=quiz_id,
        game_pin=str(game_pin),
        questions=quiz.questions,
        game_id=uuid.uuid4(),
        title=quiz.title,
        description=quiz.description,
    )
    await redis.set(f"game:{str(game.game_pin)}", (game.json()), ex=18000)
    return {**quiz.dict(exclude={"id"}), **game.dict(exclude={"questions"})}


@router.get("/join/{game_pin}")
async def get_game_id(game_pin: str):
    redis_res = (await redis.get(f"game:{game_pin}")).decode()
    if redis_res is None:
        raise HTTPException(status_code=404, detail="game not found")
    else:
        return json.loads(redis_res)["game_id"]


@router.get("/list")
async def get_quiz_list(user: User = Depends(get_current_user)):
    return await Quiz.objects.filter(user_id=user.id).all()


@router.put("/update/{quiz_id}")
async def update_quiz(quiz_id: str, quiz_input: QuizInput, user: User = Depends(get_current_user)):
    imgur_regex = r"^https://i\.imgur\.com\/.{7}.(jpg|png|gif)$"
    server_regex = rf"^{settings.root_address}/api/v1/storage/download/.{{36}}--.{{36}}$"
    for question in quiz_input.questions:
        if question.image == "":
            question.image = None
        if (
            question.image is not None
            and not bool(re.match(server_regex, question.image))
            and not bool(re.match(imgur_regex, question.image))
        ):
            raise HTTPException(status_code=400, detail="image url is not valid")
    try:
        quiz_id = uuid.UUID(quiz_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="badly formed quiz id")
    quiz = await Quiz.objects.get_or_none(id=quiz_id, user_id=user.id)
    if quiz is None:
        return JSONResponse(status_code=404, content={"detail": "quiz not found"})
    else:
        quiz_input.description = html.unescape(bleach.clean(quiz_input.description, tags=[], strip=True))
        quiz_input.title = html.unescape(bleach.clean(quiz_input.title, tags=[], strip=True))
        meilisearch.index(settings.meilisearch_index).update_documents([await get_meili_data(quiz)])
        if quiz.public and not quiz_input.public:
            meilisearch.index(settings.meilisearch_index).delete_document(str(quiz.id))
        if not quiz.public and quiz_input.public:
            meilisearch.index(settings.meilisearch_index).add_documents([await get_meili_data(quiz)])
        quiz.title = quiz_input.title
        quiz.public = quiz_input.public
        quiz.description = quiz_input.description
        quiz.updated_at = datetime.now()
        quiz.questions = quiz_input.dict()["questions"]

        return await quiz.update()


@router.post("/import/{quiz_id}")
async def import_quiz_route(quiz_id: str, user: User = Depends(get_current_user)):
    try:
        return await import_quiz(quiz_id, user)
    except ValidationError:
        raise HTTPException(status_code=400, detail="This quiz isn't (yet) supported")


@router.delete("/delete/{quiz_id}")
async def delete_quiz(quiz_id: str, user: User = Depends(get_current_user)):
    try:
        quiz_id = uuid.UUID(quiz_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="badly formed quiz id")
    quiz = await Quiz.objects.get_or_none(id=quiz_id, user_id=user.id)

    if quiz is None:
        return JSONResponse(status_code=404, content={"detail": "quiz not found"})
    pics_to_delete = []
    pic_name_regex = re.compile("^.*/(.{36}--.{36})$")
    for question in quiz.questions:
        try:
            if question["image"] is not None and not str(question["image"]).startswith("https://i.imgur.com/"):
                pics_to_delete.append(pic_name_regex.match(question["image"]).group(1))
        except KeyError:
            pass
    if len(pics_to_delete) != 0:
        await storage.delete(pics_to_delete)
    meilisearch.index(settings.meilisearch_index).delete_document(str(quiz.id))
    return await quiz.delete()
