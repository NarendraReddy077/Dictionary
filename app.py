from flask import Flask, render_template, request, jsonify
from nltk.corpus import wordnet as wn
import nltk

# Download WordNet data if not already present
nltk.download('wordnet')
nltk.download('omw-1.4')

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/word')
def word_lookup():
    word = request.args.get('q', '').strip().lower()
    if not word:
        return jsonify({'error': 'No word provided'}), 400
    
    try:
        synsets = wn.synsets(word)
        if not synsets:
            return jsonify({'error': 'Word not found'}), 404
        
        # Get word details
        synonyms = set()
        antonyms = set()
    
        for s in synsets:
            for lemma in s.lemmas():
                synonym = lemma.name().replace('_', ' ')
                if synonym != word:
                    synonyms.add(synonym)
                
                for antonym in lemma.antonyms():
                    ant = antonym.name().replace('_', ' ')
                    antonyms.add(ant)

        definition = [synset.definition() for synset in synsets][:3]

        examples = []
        if len(synsets) > 2:
            for synset in synsets[:2]:
                examples.extend(synset.examples())

        result = {
            'word': word,
            'pos': synsets[0].pos() if synsets else 'n',
            'definition': definition,
            'synonyms': list(synonyms)[:6],
            'antonyms': list(antonyms)[:6],
            'examples': examples[:5]
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)