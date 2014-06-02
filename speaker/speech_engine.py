import sys
import re
import urllib
import urllib2
import requests
import wave
from cStringIO import StringIO

import pyaudio
from pydub import AudioSegment


class SpeechEngine(object):
    CHUNK = 1024

    def _text_to_mp3(self, text, language):
        """
        :rtype: StringIO
        """
        # output = open("out.mp3", "w")
        output = StringIO()

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
        #download chunks and write them to the output file
        for idx, val in enumerate(combined_text):
            mp3url = "http://translate.google.com/translate_tts?tl=%s&q=%s&total=%s&idx=%s" % (
                language, urllib.quote(val.encode("utf-8")), len(combined_text), idx
            )
            headers = {
                "Host": "translate.google.com",
                "Referer": "http://www.gstatic.com/translate/sound_player2.swf",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.163 Safari/535.19"
            }
            req = urllib2.Request(mp3url, '', headers)
            sys.stdout.write('.')
            sys.stdout.flush()
            print requests.get(mp3url)
            if len(val) > 0:
                try:
                    response = urllib2.urlopen(req)
                    output.write(response.read())
                except urllib2.HTTPError as e:
                    print ('%s' % e)

        mp3 = output.getvalue()
        output.close()

        return mp3

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