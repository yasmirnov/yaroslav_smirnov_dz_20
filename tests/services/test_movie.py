import pytest
from unittest.mock import MagicMock

from dao.movie import MovieDAO
from dao.model.movie import Movie
from service.movie import MovieService


@pytest.fixture
def movie_dao():
    movie_dao = MovieDAO(None)

    movie_one = Movie(
        id=1,
        title='Interstellar',
        description='Наше время на Земле подошло к концу, команда исследователей берет на себя самую важную миссию в истории человечества; путешествуя за пределами нашей галактики, чтобы узнать есть ли у человечества будущее среди звезд.',
        trailer='Yes',
        year='2016',
        rating='7.5',
        genre_id=3,
        director_id=1
    )
    movie_two = Movie(
        id=2,
        title='American Pie',
        description='На вечеринке четверо старшеклассников, Джим, Кевин, Финч и Оз, выясняют, что никто из них еще не имел сексуального опыта с девушками.',
        trailer='Yes',
        year='2013',
        rating='7.9',
        genre_id=2,
        director_id=2
    )

    movie_dao.get_one = MagicMock(return_value=movie_one)
    movie_dao.get_all = MagicMock(return_value=[movie_one, movie_two])
    movie_dao.create = MagicMock(return_value=Movie(id=3))
    movie_dao.delete = MagicMock()
    movie_dao.update = MagicMock()

    return movie_dao


class TestMovieService:
    @pytest.fixture(autouse=True)
    def movie_service(self, movie_dao):
        self.movie_service = MovieService(dao=movie_dao)

    def test_get_one(self):
        movie = self.movie_service.get_one(1)

        assert movie is not None
        assert movie.id is not None

    def test_get_all(self):
        movies = self.movie_service.get_all()

        assert len(movies) > 0

    def test_create(self):
        movie_data = {
            'title': 'Guys with guns',
            'description': 'Реальная история о приятелях-планокурах из Майами, умудрившихся выбить в Пентагоне контракт на 300 миллионов долларов на поставку оружия.',
            'trailer': 'Yes',
            'year': 2016,
            'rating': 7.1,
            'genre_id': 2,
            'director_id': 2
        }

        movie = self.movie_service.create(movie_data)

        assert movie.id is not None

    def test_delete(self):
        self.movie_service.delete(1)

    def test_update(self):
        movie_data = {
            'id': 3,
            'title': 'Guys with guns',
            'description': 'Реальная история о приятелях из Майами, умудрившихся выбить в Пентагоне контракт на 300 миллионов долларов на поставку оружия.',
            'trailer': 'Yes',
            'year': 2016,
            'rating': 7.2,
            'genre_id': 2,
            'director_id': 2
        }

        self.movie_service.update(movie_data)

    def test_partially_update(self):
        movie_data = {
            'id': 3,
            'description': 'Реальная история о друзьях из Майами, умудрившихся выбить в Пентагоне контракт на 300 миллионов долларов на поставку оружия.'
        }

        self.movie_service.partially_update(movie_data)
