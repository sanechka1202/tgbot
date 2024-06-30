from get_list import get_list_person
from movie_api import get_movie_rating, get_omdb_ratings,calculate_average_rating, get_movie_rating1

def get_rating(list_names):
    movie_rate_list = []
    for movie in list_names:
        kp_rating, alternative_name, id_im = get_movie_rating1(movie)
        imdb_rating, crit_rating = get_omdb_ratings(alternative_name, id_im)
        average_rate = calculate_average_rating(kp_rating, imdb_rating, crit_rating)
        movie_rate_list.append((movie, average_rate))
    filtered_movie_ratings = [item for item in movie_rate_list if item[1] is not None]
    filtered_movie_ratings.sort(key=lambda x: x[1], reverse=True)
    return filtered_movie_ratings
    # for movie, average_rate in filtered_movie_ratings:
    #     print(f"Фильм: {movie}, Рейтинг: {average_rate}")
