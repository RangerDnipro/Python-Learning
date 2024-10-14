"""
Файл ініціалізації для пакету cinema_base
"""

from .entities import Actor, Movie
from .menu import (
    print_menu,
    print_edit_movie_menu,
    print_add_actors_to_movie_menu,
    print_edit_actor_menu
)
from .movie_handler import delete_movie, add_movie, handle_add_or_edit_movie
from .actor_handler import delete_actor, add_actor, handle_add_or_edit_actor
from .database import (
    link_actor_to_movie,
    list_movies_by_actor,
    paginate_movies,
    average_birth_year_by_genre,
    list_movies_with_actors,
    list_unique_genres,
    count_movies_by_genre,
    list_actors_and_movies
)
from .search import search_movie_by_title, search_actor_by_name, print_search_results
