import re

from flask import jsonify, request
from http import HTTPStatus

from . import app, db
from .models import URLMap, get_short
from .error_handlers import InvalidAPIUsage


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_url(short_id):
    url = URLMap.query.filter_by(short=short_id).first()
    if url is None:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    return jsonify({'url': url.original}), HTTPStatus.OK


@app.route('/api/id/', methods=['POST'])
def add_urlmap():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('\"url\" является обязательным полем!')

    url = data['url']

    if not (url.startswith('http://') or url.startswith('https://')):
        url = 'http://' + url

    if 'custom_id' in data and data['custom_id'] is not None:
        custom_id = data['custom_id']
        if not re.match('^[a-zA-Z0-9]*$', custom_id) or len(custom_id) > 16:
            raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
        if URLMap.query.filter_by(short=custom_id).first() is not None:
            raise InvalidAPIUsage(f'Имя "{custom_id}" уже занято.')

    urlmap = URLMap(
        original=url,
        short=get_short(data.get('custom_id'))
    )
    db.session.add(urlmap)
    db.session.commit()
    return jsonify(urlmap.to_dict()), HTTPStatus.CREATED
