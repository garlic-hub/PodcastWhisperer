from tempfile import NamedTemporaryFile

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename

from .auth import login_required
from .database import get_db
from .transcibe import transcribe_file

bp = Blueprint('site', __name__)


@bp.route('/')
def index():
    shows = get_db().get_shows()
    return render_template('site/index.html', shows=shows)


@bp.route('/search')
def search():
    text = request.args.get('text')

    if not text or len(text) < 3:
        flash('Search text must be at least 3 characters long')
        return redirect('/')

    segments = get_db().search_transcripts(text)

    return render_template('site/search.html', segments=segments)


@bp.route('/transcribe', methods=('GET', 'POST'))
@login_required
def transcribe():
    if request.method == 'POST':
        show_name = request.form['show']
        episode_name = request.form['episode']

        if not episode_name:
            flash('Episode name cannot be empty')
            return redirect(request.url)

        show = get_db().get_show_by_name(show_name)

        if not show:
            flash('Show does not exist')
            return redirect(request.url)

        if 'file' not in request.files:
            flash('Audio file was not present in request')
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            flash('Please select a file to upload')
            return redirect(request.url)
        
        with NamedTemporaryFile() as tmp:
            file.save(tmp)
            filename = tmp.name
            result = transcribe_file(filename)
            transcription = (i['text'] for i in result['segments'])
            timestamps = (str(i['start']) for i in result['segments'])
            get_db().add_transcription(show.id, episode_name, transcription, timestamps)

        flash('Transcription added')

    shows = get_db().get_shows()
    return render_template('site/transcribe.html', shows=shows)


@bp.route('/new-show', methods=('GET', 'POST'))
@login_required
def new_show():
    if request.method == 'POST':
        db = get_db()
        show = request.form['show']
        if db.get_show_by_name(show):
            flash('A show with that name already exists')
        else:
            db.create_show(show)
            flash('Show created')

    return render_template('site/new_show.html')
