from flask import Blueprint, request
from src.app import Post, db
from http import HTTPStatus
from sqlalchemy import inspect
from datetime import datetime
import sqlalchemy as sa


app = Blueprint('post', __name__, url_prefix='/posts')


def _create_post():
    data = request.json
    post = Post(
        title=data["title"],
        body=data["body"],
        author_id=data["author_id"]
    )
    db.session.add(post)
    db.session.commit()

    return {'message': 'Post Created!'}, HTTPStatus.CREATED

def _list_posts():
    query = db.select(Post)
    posts = db.session.execute(query).scalars()
    return [
        {
            'id': post.id,
            'title': post.title,
            'body': post.body,
            'created': post.created,
            'author_id': post.author_id
        }
        for post in posts
    ]


@app.route('/', methods=['GET', 'POST'])
def handle_posts():
    if request.method == 'POST':
        return _create_post()
    else:
        return {'posts': _list_posts()}
    

@app.route("/<int:post_id>", methods=["GET"])
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    return {
        'id': post.id,
        'title': post.title,
        'body': post.body,
        'created': post.created,
        'author_id': post.author_id
    }
@app.route("/<int:post_id>", methods=['PATCH'])
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    data = request.json

    mapper = inspect(Post)
    for column in mapper.attrs:
        if column.key in data:
            setattr(post, column.key, data[column.key])
    db.session.commit()

    return {
        'id': post.id,
        'title': post.title,
        'body': post.body,
        'created': post.created,
        'author_id': post.author_id
    }

@app.route("/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return "", HTTPStatus.NO_CONTENT