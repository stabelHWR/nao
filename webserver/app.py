#!/usr/bin/python
# -*- coding:utf-8 -*-

import spacy
from flask import request, jsonify, Flask
from db_util import getDbConnection
from weighting import setup as weighting_setup
import traceback

import counter
import db_connector
import sentence_algorithm
from transcription import transcribe
import time

cursor = getDbConnection()
weighting_setup(cursor)
# load german spacy model
nlp = spacy.load("de_core_news_sm")
app = Flask(__name__)

def get_answer(question):
    # Question is empty, respond with default message
    if question is None or len(question) == 0:
        return "This is the server of nao."

    # Annotate question with the German Spacy model; adds tokens to words...
    processed_question = nlp(question)

    # Remove irrelevant words and punctuation from question
    found_words = sentence_algorithm.sentence_detection(processed_question)

    # Get generic form of each word
    for i, word in enumerate(found_words):
        found_words[i] = word.lower()
        wd = db_connector.get_generic_term(found_words[i], cursor)
        if wd is not None:
            found_words[i] = wd

    # Based on weight of each word, get the caseID of the most relevant answer
    caseID = counter.count_ids(found_words, cursor)
    if caseID is None:
        return "Ich habe diese Frage nicht verstanden oder ich habe dazu leider keine Antwort."

    # Get answer with caseID from database
    answer = db_connector.get_answer(caseID, cursor)
    if answer is None:
        return "-1"

    return answer


@app.route('/', methods=['POST'])
def post_request():
    try:
        # Get audio with question from POST request
        if 'file' not in request.files:
            return jsonify({'error': 'No file part in the request'}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        # Save the uploaded file
        filename = "audio"
        file.save(filename)

        # Measure time
        start = time.time()

        # Get audio transcription from transcriber
        question = transcribe(filename)

        # Measure time
        end = time.time()

        # Log time and question
        print("--------------------")
        print(f"Time: {end - start}")
        print(f"Question: {question}")
        print("--------------------")

        # Get the answer
        answer = get_answer(question) 

        # Return the response as JSON
        return jsonify({'answer': answer}), 200

    except Exception as e:
        # Log the exception and return an error response
        print(f"An error occurred: {e}")
        traceback.print_exc()
        return jsonify({'error': 'An internal error occurred'}), 500
    
@app.route('/', methods=['GET'])
def get_request():
    question = request.args.get('question')

    print("--------------------")
    print("Question: " + question)
    print("--------------------")

    return get_answer(question)