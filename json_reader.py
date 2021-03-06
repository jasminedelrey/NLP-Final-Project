import json
import os
import csv
import numpy as np
from nltk import *
import random
import nltk
import random
from nltk.corpus import PlaintextCorpusReader
from nltk.corpus import stopwords


def removeStopWords(wordFile):
    stopwordList = stopwords.words('english')
    content = [w for w in wordFile if w.lower() not in stopwordList]
    return content


def removePunctuation(wordFile):
    content = [w for w in wordFile if w.isalpha()]
    return content


# def stemWords(wordFile):
#     stemmer = PorterStemmer()
#     content = [stemmer.stem(w) for w in wordFile]
#     return content


def lemmatizeWords(wordFile):
    lemmatizer = WordNetLemmatizer()
    content = [lemmatizer.lemmatize(w) for w in wordFile]
    return content


def prepareText(wordFile):
    wordFile = removeStopWords(wordFile)
    wordFile = removePunctuation(wordFile)
    wordFile = np.char.lower(wordFile)
    wordFile = lemmatizeWords(wordFile)
    return wordFile


def add_character_speech(json_file, dictionary):
    # parses inputted JSON script, adding each character and their speech into a dictionary
    for block in json_file['movie_script']:
        if block['type'] == 'speech':
            character_name = block['character'].lower()

            # checks for screen directions or unnecessary additions in script
            # if present, removes them

            if '(' in character_name and ')' in character_name:
                start_index = character_name.find('(')
                character_name = character_name[:start_index - 1]

            if character_name not in dictionary:
                dictionary[character_name] = word_tokenize(block['text'])
            else:
                dictionary[character_name] = dictionary[character_name] + word_tokenize(block['text'])


def make_csv(good_speech, bad_speech):
    row_list = []

    for dialogue in good_speech:
        row_list.append([" ".join(dialogue), 0])

    for dialogue in bad_speech:
        row_list.append([" ".join(dialogue), 1])

    random.shuffle(row_list)

    with open('dialogue_data.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["text", "character role"])
        writer.writerows(row_list)


speech_by_character = {}

for subdir, dirs, files in os.walk('json-scripts'):
    for file in files:
        with open("json-scripts/" + str(file)) as f:
            data = json.load(f)
            add_character_speech(data, speech_by_character)

for character in speech_by_character:
    print(character)

print("Deckard speech: " + str(speech_by_character['deckard']))

# adding protagonist speech
good_speech = []
good_speech.append(prepareText(speech_by_character['deckard']))
good_speech.append(prepareText(speech_by_character['z']))
good_speech.append(prepareText(speech_by_character['bourne']))
good_speech.append(prepareText(speech_by_character['steve']))
good_speech.append(prepareText(speech_by_character['lydia']))

# adding antagonist speech
bad_speech = []
bad_speech.append(prepareText(speech_by_character['betelgeuse']))
bad_speech.append(prepareText(speech_by_character['mandible']))
bad_speech.append(prepareText(speech_by_character['roth']))
bad_speech.append(prepareText(speech_by_character['batty']))
bad_speech.append(prepareText(speech_by_character['conklin']))

print("Deckard speech (stopwords, punctuation removed, lowercase, words lemmatized): " + str(good_speech[0]))

# this is what makes the CSV file!
# takes both lists and adds them to CSV in randomized order
make_csv(good_speech, bad_speech)