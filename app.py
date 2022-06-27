import json
import pandas as pd
from flask import Response, render_template, request
from flask_restx import Api, Resource, fields
from src import create_app
from src.models import Anime as model
from src.views import get_all, get_item, get_items_from_index, \
                        delete_item, delete_items_from_index, \
                        update_item_in_table, add_item

app = create_app()

api = Api(
    app, 
    version='0.0.1', 
    title='Anime API',
    description='Manage anime through the application',
    license="Blah",
    license_url="blahblahblah.com",
    contact="Aashish Chaubey",
    contact_url="https://aashishchaubey.com",
    contact_email="aashish.l@acldigital.com"
)

ns_anime = api.namespace('anime', description='Anime operations')

anime_model = api.model('Anime', {
    'anime_id': fields.Integer,
    'title': fields.String
})

@ns_anime.route('/')
class AnimeList(Resource):
    '''Shows a list of all animes'''
    def get(self):
        """List all animes"""
        animes = get_all(model=model)
        anime_list = []
        for anime in animes:
            new_anime = {
                "anime_id": anime.anime_id,
                "title": anime.title
            }
            anime_list.append(new_anime)
        resp = Response(
            response=json.dumps(anime_list),
            status=200,
            mimetype="application/json"
        )
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp


@ns_anime.route('/<int:idx>')
@ns_anime.response(404, 'Anime not found')
@ns_anime.param('idx', 'Anime identifier')
class Anime(Resource):
    '''Single anime item operations - GET, UPDATE, DELETE'''

    def get(self, idx):
        """Get a specific anime"""
        item = get_item(model=model, id=idx)
        if item is None:
            resp = render_template('error_message.html')
        else:
            item = {
                "anime_id": idx,
                "title": str(item)
            }
            resp = Response(
                response=json.dumps(item),
                status=200,
                mimetype="application/json"
            )
            resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp

    def put(self, idx):
        """Update a specific anime"""
        old_value = {
            "old": str(get_item(model=model, idx=idx))
        }
        update_value = request.args.get('anime')
        status = update_item_in_table(
            model=model, idx=idx, value=update_value
        )
        if status == 1:
            new_value = {
                "new": str(get_item(model=model, idx=idx))
            }
            data = {
                "anime_id": idx,
                "title": [old_value, new_value]
            }
        else:
            # TODO - handle the failed update status
            pass
        if data is None:
            resp = render_template('error_message.html')
        else:
            resp = Response(
                response=json.dumps(data),
                status=200,
                mimetype="application/json"
            )
            resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp


    def delete(self, idx):
        """Delete a specific anime"""
        data = delete_item(model=model, idx=idx)
        if data is None:
            resp = render_template('error_message.html')
        else:
            data = {
                "anime_id": idx,
                "title": str(data)
            }
        resp = Response(
            response=json.dumps(data),
            status=200,
            mimetype="application/json"
        )
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp


@ns_anime.route('/<int:idx>/<int:rng>')
@ns_anime.response(404, 'Anime not found')
@ns_anime.param('idx', 'Anime identifier')
@ns_anime.param('rng', 'Range of values')
class BulkAnime(Resource):
    """Bulk anime item operations - GET, DELETE"""

    def get(self, idx, rng):
        """Get a `rng` list of animes starting from id:`idx`"""
        items = get_items_from_index(model=model, idx=idx, rng=rng)
        anime_list = []
        for index, item in enumerate(items, idx):
            new_anime = {
                "anime_id": index,
                "title": str(item)
            }
            anime_list.append(new_anime)
        resp = Response(
            response=json.dumps(anime_list),
            status=200,
            mimetype="application/json"
        )
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp

    def delete(self, idx, rng):
        """Delete a `rng` list of animes starting from id:`idx`"""
        items = delete_items_from_index(model=model, idx=idx, rng=rng)
        delete_list = []
        for index, item in enumerate(items, idx):
            new_anime = {
                "anime_id": index,
                "title": str(item)
            }
            delete_list.append(new_anime)
        resp = Response(
            response=json.dumps(delete_list),
            status=200,
            mimetype="application/json"
        )
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp


@ns_anime.route('/upload')
@ns_anime.response(404, 'Anime not found')
class UploadAnime(Resource):
    """Upload anime data to database"""

    def post(self):
        """Upload list of animes using csv data"""
        if request.files:
            uploaded_file = request.files['file']
            df = pd.read_csv(uploaded_file, header=0)
            for _, item in df.iterrows():
                add_item(model=model, anime_id=item['anime_id'], title=item['title'])
            resp = Response(
                response=json.dumps({"status": "Added"}),
                status=200,
                mimetype="application/json"
            )
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4996, debug=False)
