#!/usr/bin/env bash
venv/bin/twistd -n web --wsgi=speaker.speaker.app -p 5000
