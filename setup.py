from setuptools import find_packages, setup


setup(
    name='speaker',
    version='0.1',
    description='Speaker with google speech engine',
    long_description='',
    author='Igor Pavlov',
    author_email='nwlunatic@yandex.ru',
    zip_safe = False,
    packages=find_packages(),
    install_requires=[
        "PyAudio==0.2.8",
        "pydub==0.9.2",
        "flask==0.10"
    ],
    entry_points = {
        'console_scripts': [
            'speaker = speaker.speaker:main'
        ],
    },
)