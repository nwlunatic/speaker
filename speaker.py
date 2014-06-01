import argparse

from flask import Flask, request, jsonify

from src.speech_module import SpeechEngine


parser = argparse.ArgumentParser(description='Speaker')
parser.add_argument('-p', '--port', type=int, default=8080,
                    help='port to use')


app = Flask(__name__)
se = SpeechEngine()


@app.route('/speak', methods=['POST', 'GET'])
def speak():
    response = {}
    text = request.args.get("text")
    language = request.args.get("language")

    if text is None:
        response["code"] = 500
        response["result"] = '"text" parameter is necessary'
        return jsonify(**response)

    if language is None:
        language = "en"

    se.speak(text, language)

    response["code"] = 200
    response["result"] = 'ok'
    return jsonify(**response)


if __name__ == "__main__":
    args = parser.parse_args()
    app.run(host='0.0.0.0', port=args.port)