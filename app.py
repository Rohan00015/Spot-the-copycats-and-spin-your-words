from flask import Flask, render_template, request, jsonify
from difflib import SequenceMatcher
from transformers import pipeline
from sentence_transformers import SentenceTransformer, util
import nltk

nltk.download('punkt_tab')
from nltk.tokenize import sent_tokenize

app = Flask(__name__)

# Load text rephrasing and similarity models
rephrasing_model = pipeline("text2text-generation", model="t5-small")
similarity_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Function to calculate similarity
def calculate_similarity(text1, text2):
    embedding1 = similarity_model.encode(text1, convert_to_tensor=True)
    embedding2 = similarity_model.encode(text2, convert_to_tensor=True)
    similarity = util.cos_sim(embedding1, embedding2).item()
    return similarity

# Function to rephrase text
def rephrase_sentence(sentence):
    result = rephrasing_model(sentence, max_length=200, num_return_sequences=1)
    return result[0]['generated_text']

# Endpoint to check and rephrase text
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        input_text = request.form['text']
        sentences = sent_tokenize(input_text)

        plagiarized_sentences = []
        unique_sentences = []
        plagiarized_score = 0

        for sentence in sentences:
            # Compare with a simulated database (replace this with your text database)
            database = ["Detecting Content Copying Effectively", "Plagiarism Detection in AI systems"]
            max_similarity = max([calculate_similarity(sentence, entry) for entry in database])

            if max_similarity > 0.3:  # Threshold for plagiarism
                plagiarized_score += max_similarity
                plagiarized_sentences.append(sentence)
            else:
                unique_sentences.append(sentence)

        plagiarism_percentage = (plagiarized_score / len(sentences)) * 100
        unique_percentage = 100 - plagiarism_percentage

        # Rephrasing plagiarized sentences
        rewritten_sentences = [rephrase_sentence(sentence) for sentence in plagiarized_sentences]

        return jsonify({
            'plagiarism_percentage': plagiarism_percentage,
            'unique_percentage': unique_percentage,
            'plagiarized_sentences': plagiarized_sentences,
            'rewritten_sentences': rewritten_sentences
        })

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
