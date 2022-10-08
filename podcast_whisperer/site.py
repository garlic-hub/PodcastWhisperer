import os
from tempfile import NamedTemporaryFile

from flask import Blueprint, flash, redirect, render_template, request, current_app, send_from_directory
from werkzeug.utils import secure_filename

from .auth import login_required
from .database import get_db
from .transcribe import transcribe_file

# Image formats that HTML <img> tag supports
ALLOWED_IMAGE_EXTENSIONS = ('png', 'jpg', 'jpeg', 'svg')

bp = Blueprint('site', __name__)


def allowed_image_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS


@bp.route('/')
def index():
    shows = get_db().get_shows()
    print(shows)
    return render_template('site/index.html', shows=shows)


@bp.route('/search')
def search():
    text = request.args.get('text')

    if not text or len(text) < 3:
        flash('Search text must be at least 3 characters long')
        return redirect('/')

    segments = get_db().search_transcripts(text)

    return render_template('site/search.html', segments=segments)


@bp.route('/episode_list/<show_name>')
def episode_list(show_name):
    show = get_db().get_show_by_name(show_name)

    if not show:
        flash('Show does not exist. Please check spelling or select one below.')
        return redirect('/')

    episodes = get_db().get_episodes(show.id)

    return render_template('site/episode_list.html', show=show.name, episodes=episodes)


@bp.route('/transcripts/<episode_id>')
def view_transcript(episode_id):
    segments = get_db().get_transcript(episode_id)

    if not segments:
        flash('Episode does not exist')
        return redirect('/')

    transcript = ' '.join((s.text for s in segments))

    return render_template('site/transcript.html', transcript=transcript)


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
            timestamps = (int(i['start']) for i in result['segments'])
            get_db().add_transcription(show.id, episode_name, transcription, timestamps)

        flash('Transcription added')

    shows = get_db().get_shows()
    return render_template('site/transcribe.html', shows=shows)


@bp.route('/new-show', methods=('GET', 'POST'))
@login_required
def new_show():
    if request.method == 'POST':
        show_name = request.form['show']

        # Ensure show name exists and isn't empty
        if not show_name:
            flash('Show name cannot be empty')
            return redirect(request.url)

        # Ensure show with that name does not already exist
        if get_db().get_show_by_name(show_name):
            flash('A show with that name already exists')

        # Check that POST has file part
        if 'image' not in request.files:
            flash('Podcast image was not present in request')
            return redirect(request.url)

        image = request.files['image']

        # If the user does not select a file, the browser submits an empty file without a filename.
        if image.filename == '':
            flash('Please select a file to upload')
            return redirect(request.url)

        # Ensure that file type is good image format and secure the filename
        if allowed_image_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(current_app.config['UPLOAD'], filename))

            # Everything checks out, add show to database
            get_db().create_show(show_name, filename)
            flash('Show created')
        else:
            flash(f'Bad file type. Please use one of the following: {", ".join(ALLOWED_IMAGE_EXTENSIONS)}')

    return render_template('site/new_show.html')


@bp.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(current_app.config["UPLOAD"], name)
