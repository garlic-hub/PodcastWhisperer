import argparse
from transcibe import transcribe_file

from database import Database


def get_args():
    parser = argparse.ArgumentParser(description='PodcastWhisperer')
    subparser = parser.add_subparsers()

    transcribe = subparser.add_parser('transcribe', help='Transcribe an episode')
    transcribe.set_defaults(func=transcribe_command)
    transcribe.add_argument('show', help='The show this episode is from')
    transcribe.add_argument('name', help='The name of this episode')
    transcribe.add_argument('file', help='The audio file to transcribe')

    create = subparser.add_parser('create', help='Create a podcast listing to store transcriptions')
    create.set_defaults(func=create_command)
    create.add_argument('name', help='The name of the podcast')

    shows = subparser.add_parser('shows', help='List all shows')
    shows.set_defaults(func=shows_command)

    return parser


def transcribe_command(args):
    result = transcribe_file(args.file)
    transcription = [i['text'] for i in result['segments']]
    timestamps = [str(i['start']) for i in result['segments']]
    Database().add_transcription(args.show, args.name, transcription, timestamps)


def create_command(args):
    Database().create_show(args.name)


def shows_command(_):
    shows = Database().get_shows()

    if not shows:
        print('No shows in database. Try adding some.')
        return

    print('Show ID | Show Name')
    print('-------------------')
    for (show_id, name) in shows:
        print(f'{show_id}\t| {name}')


def main():
    args = get_args().parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
