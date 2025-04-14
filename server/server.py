from flask import Flask, request, jsonify
from flask_cors import CORS
from translator import translate
import json

app = Flask(__name__)
CORS(app)

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, tuple):
            return list(obj)  # Convert tuples to lists for JSON serialization
        return super().default(obj)

app.json_encoder = CustomJSONEncoder

@app.route('/api/translate', methods=['POST'])
def translate_lyrics():
    try:
        # Get the lyrics from the request body
        data = request.get_json(force=True)  # force=True to ensure UTF-8 parsing
        
        if not data or 'lyrics' not in data:
            return jsonify({
                'error': 'No lyrics provided',
                'status': 400
            }), 400
            
        lyrics_text = data['lyrics']
        
        # Validate lyrics format
        if not isinstance(lyrics_text, str):
            return jsonify({
                'error': 'Lyrics must be provided as a string',
                'status': 400
            }), 400
            
        # Split the lyrics into lines and remove empty lines
        lyrics_lines = [line.strip() for line in lyrics_text.splitlines() if line.strip()]
            
        # Translate the lyrics
        translated = translate(lyrics_lines)
        
        # Process the translation to ensure it's in the right format for the frontend
        processed_translation = []
        for line in translated:
            if isinstance(line, list):
                processed_line = []
                for item in line:
                    if isinstance(item, tuple) and len(item) == 3:
                        # This is already in the right format (chinese, pinyin, english)
                        processed_line.append(item)
                    elif isinstance(item, list):
                        # This is a nested list of tuples
                        processed_line.append(item)
                    else:
                        # This is a string or something else
                        processed_line.append(item)
                processed_translation.append(processed_line)
            else:
                processed_translation.append(line)
        
        response = jsonify({
            'status': 200,
            'translation': processed_translation
        })
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 500
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)