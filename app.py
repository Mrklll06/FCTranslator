from flask import Flask, render_template, request, jsonify
from translate import Translator
from gtts import gTTS
import os

app = Flask(__name__)

# Ensure 'static' directory exists for saving audio files
if not os.path.exists("static"):
    os.makedirs("static")


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/translate', methods=['POST'])
def translate_text():
    data = request.json
    text = data.get('text', '')
    source_lang = data.get('source_lang', 'en')
    target_lang = data.get('target_lang', 'fr')

    if text:
        translator = Translator(from_lang=source_lang, to_lang=target_lang)
        translated_text = translator.translate(text)
        return jsonify({'translated_text': translated_text})
    return jsonify({'translated_text': ''})


@app.route('/save-audio', methods=['POST'])
def save_audio():
    data = request.json
    text = data.get('text', '')
    lang = data.get('lang', 'en')

    if not text.strip():
        return jsonify({'error': 'No text provided'})

    try:
        tts = gTTS(text=text, lang=lang)
        file_path = f"static/audio_{lang}.mp3"
        tts.save(file_path)
        return jsonify({'audio_url': f"/{file_path}"})
    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)