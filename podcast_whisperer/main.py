import argparse
from pprint import pprint
from transcibe import transcribe_file


def get_args():
    parser = argparse.ArgumentParser(description='PodcastWhisperer')
    subparser = parser.add_subparsers()

    transcribe = subparser.add_parser('transcribe', help='Transcribe an episode')
    transcribe.set_defaults(func=transcribe_command)
    transcribe.add_argument('podcast', help='The podcast this episode is from')
    transcribe.add_argument('name', help='The name of this episode')
    transcribe.add_argument('file', help='The audio file to transcribe')

    create = subparser.add_parser('create', help='Create a podcast listing to store transcriptions')
    create.set_defaults(func=create_command)
    create.add_argument('name', help='The name of the podcast')

    return parser


def transcribe_command(args):
    result = transcribe_file(args.file)
    pprint(result)


def create_command(args):
    pass


def main():
    args = get_args().parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
