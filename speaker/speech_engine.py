import sys
import re
import urllib
import urllib2
import requests
import wave
from cStringIO import StringIO

import pyaudio
from pydub import AudioSegment


class _SpeechEngine(object):
    CHUNK = 1024

    def _text_to_chunks(self, text):
        #process text into chunks
        text = text.replace('\n', '')
        text_list = re.split('(,|\.)', text)
        combined_text = []
        for idx, val in enumerate(text_list):
            if idx % 2 == 0:
                combined_text.append(val)
            else:
                joined_text = ''.join((combined_text.pop(), val))
                if len(joined_text) < 100:
                    combined_text.append(joined_text)
                else:
                    subparts = re.split('( )', joined_text)
                    temp_string = ""
                    temp_array = []
                    for part in subparts:
                        temp_string += part
                        if len(temp_string) > 80:
                            temp_array.append(temp_string)
                            temp_string = ""
                    #append final part
                    temp_array.append(temp_string)
                    combined_text.extend(temp_array)
        return combined_text

    def _text_to_mp3(self, text, language):
        """
        :rtype: StringIO
        """
        pass

    def _mp3_to_wav(self, mp3):
        sound = AudioSegment.from_mp3(StringIO(mp3))
        wav = sound.export(StringIO(), format="wav").getvalue()
        return wav

    def _play(self, wav):
        p = pyaudio.PyAudio()

        wf = wave.open(StringIO(wav))

        stream = p.open(
            format=p.get_format_from_width(wf.getsampwidth()),
            channels=wf.getnchannels(),
            rate=wf.getframerate(),
            output=True
        )

        data = wf.readframes(self.CHUNK)
        while data:
            stream.write(data, self.CHUNK)
            data = wf.readframes(self.CHUNK)

        stream.stop_stream()
        stream.close()
        p.terminate()

    def speak(self, text, language="en"):
        mp3 = self._text_to_mp3(text, language)
        wav = self._mp3_to_wav(mp3)
        self._play(wav)


class GoogleSpeechEngine(_SpeechEngine):
    def _text_to_mp3(self, text, language):
        output = StringIO()

        combined_text = self._text_to_chunks(text)
        #download chunks and write them to the output file
        for idx, val in enumerate(combined_text):
            mp3url = "http://translate.google.com/translate_tts?tl=%s&q=%s&total=%s&idx=%s" % (
                language, urllib.quote(val.encode("utf-8")), len(combined_text), idx
            )
            headers = {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.114 Safari/537.36"
            }
            print mp3url

            if len(val) > 0:
                response = requests.get(mp3url, headers=headers)
                output.write(response.content)

        mp3 = output.getvalue()
        output.close()

        return mp3


class YandexSpeechEngine(_SpeechEngine):
    def _text_to_mp3(self, text, language):
        output = StringIO()

        combined_text = self._text_to_chunks(text)
        #download chunks and write them to the output file
        for idx, val in enumerate(combined_text):
            mp3url = "http://tts.voicetech.yandex.net/tts?format=mp3&quality=hi&platform=web&application=translate&lang=%s&text=%s" % (
                language, urllib.quote(val.encode("utf-8"))
            )
            headers = {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.114 Safari/537.36"
            }
            print mp3url

            if len(val) > 0:
                response = requests.get(mp3url, headers=headers)
                output.write(response.content)

        mp3 = output.getvalue()
        output.close()
        # with open("test.mp3", "bw") as f:
        #     f.write(mp3)

        return mp3
