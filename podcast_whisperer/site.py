from tempfile import NamedTemporaryFile

from flask import Blueprint, flash, redirect, render_template, request

from .auth import login_required
from .database import get_db
from .transcribe import transcribe_file

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
        db = get_db()
        show = request.form['show']
        if db.get_show_by_name(show):
            flash('A show with that name already exists')
        else:
            db.create_show(show)
            flash('Show created')

    return render_template('site/new_show.html')
