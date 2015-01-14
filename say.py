#!/usr/bin/env python
# coding: utf-8
import sys
import urllib
import requests
import argparse


URL = "http://uk-nettop-03.2gis.local"
#URL = "http://localhost"
PORT = 8080


def say(text, lang, engine="google"):
  text = urllib.quote(text.encode('utf-8'))
  requests.get(u"%s:%s/speak?text=%s&language=%s&engine=%s" % (URL, PORT, text, lang, engine))


parser = argparse.ArgumentParser()
parser.add_argument("text", type=str)
args = parser.parse_args()
text = args.text.decode("utf-8")

say(text, "ru_RU", "yandex")
