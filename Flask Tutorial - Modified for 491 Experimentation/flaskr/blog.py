from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)


@bp.route('/')
def index():
    '''
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    '''

    cursor = get_db().cursor(dictionary=True)
    cursor.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    )
    posts = cursor.fetchall()
    cursor.close()

    return render_template('index.html', posts=posts)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            '''
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            '''

            db = get_db()
            cursor = db.cursor(dictionary=True)
            cursor.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (%s, %s, %s)',
                (title, body, g.user['id'])
            )
            g.db.commit()
            cursor.close()

            return redirect(url_for('blog.index'))

    return render_template('create.html')


def get_post(id, check_author=True):
    '''
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()
    '''

    cursor = get_db().cursor(dictionary=True)
    cursor.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = %s',
        (id,)
    )
    post = cursor.fetchone()
    cursor.close()


    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            '''
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            '''

            db = get_db()
            cursor = db.cursor(dictionary=True)
            cursor.execute(
                'UPDATE post SET title = %s, body = %s'
                ' WHERE id = %s',
                (title, body, id)
            )
            g.db.commit()
            cursor.close()

            return redirect(url_for('blog.index'))

    return render_template('update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    '''
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    '''
    
    cursor = get_db().cursor(dictionary=True)
    cursor.execute(
        'DELETE FROM post WHERE id = %s',
        (id,)
    )
    g.db.commit()
    cursor.close()

    return redirect(url_for('blog.index'))

'''
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_require
from flaskr.db import get_db

bp = Blueprint('blog',__name__)

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)

@bp.route('/create', methods=('GET', 'POST'))
@login_require     # A user must be logged in to visit these views, otherwise
                    # they will be redirected to the login page.b
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')

def get_post(id, check_author=True):    # Gets the post and calls it from each view.
    post = get_db().execute(            # Fetches a post by id and checks if the author matches the logged in user.
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")          # abort() will raise a special exception that returns an HTTP status code. It takes an
                                                            # optional message to show with the error, otherwise a default message is used. 404
    if check_author and post['author_id'] != g.user['id']:  # means "Not Found", and 403 means "Forbidden". (401 means "Unauthorized", but you
        abort(403)                                          # redirect to the login page instead of returning that status.)

                                                            # The check_author arugment is defined so that the function can be used to get a post
                                                            # without checking the author. This would be useful if you wrote a view to show an
                                                            # individual post on a page, where the user doesn't matter because they're not
                                                            # modifying the post.

    return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))      # Unlike the views you’ve written so far, the update function takes an argument, id.
@login_require                                             # That corresponds to the <int:id> in the route. A real URL will look like
def update(id):                                             # /1/update. Flask will capture the 1, ensure it’s an int, and pass it as the id
    post = get_post(id)                                     # argument. If you don’t specify int: and instead do <id>, it will be a string. To
                                                            # generate a URL to the update page, url_for() needs to be passed the id so it knows
    if request.method == 'POST':                            # what to fill in: url_for('blog.update', id=post['id']). This is also in the
        title = request.form['title']                       # index.html file above.
        body = request.form['body']
        error = None                                        # The create and update views look very similar. The main difference is that the
                                                            # update view uses a post object and an UPDATE query instead of an INSERT. With
        if not title:                                       # some clever refactoring, you could use one view and template for both actions, but
            error = 'Title is required.'                    # for the tutorial it’s clearer to keep them separate.

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))        # The delete view doesn’t have its own template, the delete button is part of
@login_require                                         # update.html and posts to the /<id>/delete URL. Since there is no template,
def delete(id):                                         # it will only handle the POST method and then redirect to the index view.
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))
'''