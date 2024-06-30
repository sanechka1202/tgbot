from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from movie_api import get_omdb_ratings, calculate_average_rating,get_movie_rating
from find_id_person import get_id_person
from get_list import get_list_person
from get_rate import get_rating
from get_list_actor import get_listact_person
import keyboards as kb

router = Router()

class Film(StatesGroup):
    name = State()
class Director(StatesGroup):
    namedir = State()
class Actor(StatesGroup):
    name_act = State()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Привет! Наш бот может выдать тебе среднюю оценку любого фильма, а также получить рейтинг лучших фильмов режиссера, актера, актрисы!', reply_markup=kb.main)

@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer('Вы нажали на кнопку помощи')

@router.message(F.text == 'Рейтинг фильма')
async def film(message: Message, state: FSMContext):
    await state.set_state(Film.name)
    await message.answer('Напишите название фильма на русском языке и без ошибок!')

@router.message(Film.name)
async def process_movie_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    data = await state.get_data()
    movie_name = data["name"]
    kp_rating, alternative_name, id_imdb, year, img = get_movie_rating(movie_name)
    if not kp_rating or not alternative_name:
        await message.answer("Фильм не найден или отсутствует рейтинг.")
        return
    imdb_rating, crit_rat = get_omdb_ratings(alternative_name, id_imdb)

    # if not imdb_rating or not metascore or not rt_rating:
    #     await message.answer("Фильм не найден в OMDb или отсутствуют оценки.")
    #     return

    average_rating = calculate_average_rating(kp_rating, imdb_rating, crit_rat)

    if average_rating is None:
        await message.answer("Не удалось вычислить средний рейтинг.")

    else:
        if img is None:
            await message.answer(f"Название: {movie_name}/{alternative_name}\nГод выпуска: {year}\nСредний рейтинг: {average_rating:.2f} из 10\nРейтинг на КиноПоиск: {kp_rating}\nРейтинг на IMDB: {imdb_rating}\nРейтинг критиков: {crit_rat}\nФормула расчета средней оценки: (КП + IMDB + Критики)/ 3")
        else:
            await message.answer_photo(img, f"Название: {movie_name}/{alternative_name}\nГод выпуска: {year}\nСредний рейтинг: {average_rating:.2f} из 10\nРейтинг на КиноПоиск: {kp_rating}\nРейтинг на IMDB: {imdb_rating}\nРейтинг критиков: {crit_rat}\nФормула расчета средней оценки: (КП + IMDB + Критики)/ 3")
    await state.clear()

@router.message(F.text == 'Рейтинг фильмов режиссера')
async def direct(message: Message, state: FSMContext):
    await state.set_state(Director.namedir)
    await message.answer('Напишите имя и фамилию режиссера на русском языке и без ошибок!')

@router.message(Director.namedir)
async def list_top(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    data = await state.get_data()
    dir_name = data["name"]
    id_dir = get_id_person(dir_name)
    list_movies, portr = get_list_person(id_dir)
    text_mes = get_rating(list_movies)
    text_mes_norm = f"Топ лучших фильмов\n режиссера {dir_name}\n"
    for i, (title, rating) in enumerate(text_mes, 1):
        text_mes_norm += f"{i}) {title} - {rating:.2f}\n"
    await message.answer_photo(portr, f"{text_mes_norm}")
    await state.clear()


@router.message(F.text == 'Рейтинг фильмов актёра/актрисы')
async def direct(message: Message, state: FSMContext):
    await state.set_state(Actor.name_act)
    await message.answer('Напишите имя и фамилию актёра/актрисы на русском языке и без ошибок!')

@router.message(Actor.name_act)
async def list_topactr(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    data = await state.get_data()
    act_name = data["name"]
    id_act = get_id_person(act_name)
    list_movies, phot = get_listact_person(id_act)
    text_mes = get_rating(list_movies)
    text_mes_norm = f"Топ лучших фильмов актёра/актрисы\n{act_name}\n"
    for i, (title, rating) in enumerate(text_mes, 1):
        text_mes_norm += f"{i}) {title} - {rating:.2f}\n"
    await message.answer_photo(phot, f"{text_mes_norm}")
    await state.clear()