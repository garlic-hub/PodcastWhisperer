from setuptools import find_packages, setup

setup(
    name='podcast_whisperer',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
        'whisper @ git+https://github.com/openai/whisper.git'
    ],
)