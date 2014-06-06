import argparse

from flask import Flask, request, jsonify

from speech_engine import YandexSpeechEngine, GoogleSpeechEngine


parser = argparse.ArgumentParser(description='Speaker')
parser.add_argument('-p', '--port', type=int, default=8080,
                    help='port to use')


app = Flask(__name__)
gse = GoogleSpeechEngine()
yse = YandexSpeechEngine()


@app.route('/speak', methods=['POST', 'GET'])
def speak():
    response = {}
    text = request.args.get("text")
    language = request.args.get("language")
    engine = request.args.get("engine")

    if text is None:
        response["code"] = 500
        response["result"] = '"text" parameter is necessary'
        return jsonify(**response)

    if language is None:
        language = "en"

    if engine == "yandex":
        engine = yse
    elif engine == "google":
        engine = gse
    else:
        engine = gse

    print text, language, engine

    engine.speak(text, language)

    response["code"] = 200
    response["result"] = 'ok'
    return jsonify(**response)


def main():
    args = parser.parse_args()
    app.run(host='0.0.0.0', port=args.port)


if __name__ == "__main__":
    main(debug=True)