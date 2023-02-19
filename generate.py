from datetime import date, timedelta
import os
import openai
import json
import random
import urllib
import nltk
from nltk.stem import WordNetLemmatizer
import re

openai.api_key = os.getenv("OPENAI_API_KEY")
# Takes in a word and a sentence, returns which word it is in the sentence
def find_word(word,sentence):
    wordList = sentence.lower().split()
    word = word.lower().split()[0]
    for i in range(len(wordList)):
        noWrongChar = re.sub(r'[^a-zA-Z0-9]', '', wordList[i])
        if same_word_different_tense(word,noWrongChar):
            return i
    return -1

def same_word_different_tense(word1, word2):
    word1 = word1.lower()
    word2 = word2.lower()
    lemmatizer = WordNetLemmatizer()
    noun1 = lemmatizer.lemmatize(word1)
    noun2 = lemmatizer.lemmatize(word2)
    if noun1 == noun2:
        return True
    verb1 = lemmatizer.lemmatize(word1, pos="v")
    verb2 = lemmatizer.lemmatize(word2, pos="v")
    if verb1 == verb2:
        return True

# Takes in a string, generates an AI image of it, and saves it to a file
def generate_image(words,sentence, date):
    response = openai.Image.create(
        prompt=sentence,
        n=5,
        size="512x512"
    )
    jsonObject = { "words": words, "sentence": sentence }
    make_dir(date)
    for i in words:
        jsonObject[i] = find_word(i,sentence)
    # Writes words and sentence  to a json file
    with open(f"./openai-quickstart-python/static/images/{date}/words.json", 'w') as f:
        json.dump(jsonObject, f)
    for i in range(len(response['data'])):
        url =response['data'][i]['url']
        urllib.request.urlretrieve(url,f"./openai-quickstart-python/static/images/{date}/{date}--{i}.png")

# Makes a directory in ./images/ named after today's date
def make_dir(dateString):
    os.mkdir("./openai-quickstart-python/static/images/"+dateString)
    return dateString
# Checks if directories that are older than 7 days exist, and deletes them
def check_dir():
    today = date.today()
    keepList = []
    # Create a list of directories to keep
    for i in range(-14,14):
        iDate = today - timedelta(days=i)
        d2 = iDate.strftime("%m-%d-%Y")
        keepList.append(d2)
        iDate = iDate - timedelta(days=1)
    # Iterate through all directories in ./images/
    for d3 in os.listdir("./openai-quickstart-python/static/images/"):
        # If the directory is not in the keepList, delete it
        if d3 not in keepList:
            print("deleting "+d3)
            for f in os.listdir("./openai-quickstart-python/static/images/"+d3):
                os.remove(os.path.join("./openai-quickstart-python/static/images/"+d3, f))
            os.rmdir("./openai-quickstart-python/static/images/"+d3)
# Load the JSON object from the file
with open('stuff.json', 'r') as f:
  data = json.load(f)

# Get the lists of people, actions, places, and things
people = data['people']
actions = data['actions']
places = data['places']
# things = data['things']

# Delete directories older than a week
check_dir()

# Today
now = date.today()

# Get a random element from each list
for i in range(4):
    finished = False
    while finished == False:
        try:
            future = now + timedelta(days=i)
            dirName = future.strftime("%m-%d-%Y")
            print(dirName)
            if os.path.exists(f"./openai-quickstart-python/static/images/{dirName}"):
                print("exists")
                finished = True
                continue

            person = str.lower(random.choice(people))
            action = str.lower(random.choice(actions))
            place = str.lower(random.choice(places))
            # thing1 = str.lower(random.choice(things))
            # thing2 = random.choice(things)
            # while thing1 == thing2:
            #     thing2 = random.choice(things)

            response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"Generate a very simple sentence using the following words: {person}, {action}, {place}. Also make the sentence very easy for DALL-E to draw.",
            temperature=0.5,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0  
            )
            # Print out the random elements
            sentence  = str.strip(response['choices'][0]['text']).replace('"','')
            words = [person,action,place]
            print(f'{person} {action} {place}')
            print(sentence)
            generate_image(words,sentence,dirName)
            finished = True
        except Exception as e:
            print(e)
            pass
