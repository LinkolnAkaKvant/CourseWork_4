from flask import request
from flask_restx import Resource, Namespace

from dao.model.movie import MovieSchema
from decorators import auth_required, admin_required
from implemented import movie_service

movie_ns = Namespace('movies')


@movie_ns.route('/')
class MoviesView(Resource):
    @auth_required
    def get(self):
        director = request.args.get("director_id")
        genre = request.args.get("genre_id")
        year = request.args.get("year")
        status = request.args.get("status")
        page = request.args.get("page")
        filters = {
            "director_id": director,
            "genre_id": genre,
            "year": year,
            "status": status,
            "page": page,

        }
        all_movies = movie_service.get_all(filters)
        result = MovieSchema(many=True).dump(all_movies)
        return result, 200

    @admin_required
    def post(self):
        request_json = request.json
        movie = movie_service.create(request_json)
        return "", 201, {"location": f"/movies/{movie.id}"}


@movie_ns.route('/<int:bid>')
class MovieView(Resource):
    @auth_required
    def get(self, mid):
        movie = movie_service.get_one(mid)
        result = MovieSchema().dump(movie)
        return result, 200

    @admin_required
    def put(self, mid):
        request_json = request.json
        if "id" not in request_json:
            request_json["id"] = mid
        movie_service.update(request_json)
        return "", 204

    @admin_required
    def delete(self, mid):
        movie_service.delete(mid)
        return "", 204
