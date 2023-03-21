from datetime import timedelta
import datetime
import os
import json
from flask_login import LoginManager, UserMixin, current_user, login_user
from flask_sqlalchemy import SQLAlchemy
import openai
import nltk
from werkzeug.security import check_password_hash, generate_password_hash
from nltk.stem import WordNetLemmatizer
from flask_bootstrap import Bootstrap
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from flask_wtf import FlaskForm

from flask import Flask, make_response, redirect, render_template, request, url_for, session, flash


def read_json(json_file, field):
  with open(json_file, 'r') as f:
    data = json.load(f)
  ret = data[field]
  return ret

# Takes in a string and a word list and uses check word for each word in the list


def check_sentence(guess, words):
    for i in words:
        if check_word(i, guess):
            return True
    return False

# Takes in two strings and checks if the first string is the second string with any of the following endings: s, ed, ing, y, es, ies, ied


def check_word(word, guess):
    word1 = word.lower().strip()
    word2 = guess.lower().strip()
    lemmatizer = WordNetLemmatizer()
    noun1 = lemmatizer.lemmatize(word1, pos="n")
    noun2 = lemmatizer.lemmatize(word2, pos="n")
    if noun1 == noun2:
        return True
    verb1 = lemmatizer.lemmatize(word1, pos="v")
    verb2 = lemmatizer.lemmatize(word2, pos="v")
    if verb1 == verb2:
        return True

# Takes tuples of (word, number) and returns a list of the words ordered by number


def order_words(words):
    words = sorted(words, key=lambda x: x[1])
    return [i[0] for i in words]

#Takes in a string and index list and replaces the words at the index with "___________"


def replace_words(string, index_list):
    words = string.split()
    for i in index_list:
        if i == "":
            continue
        words[i[1]] = "___________"
        for j in range(i[1]+1, i[1]+len(i[0].split())):
            words[j] = ""
    for i in words:
        if i == "":
            words.remove(i)
    return " ".join(words)

# Takes in a word list and returns the json object of the word


def get_words_json(word_list, today):
    words = []
    for i in word_list:
        words.append(
            (i, read_json("./static/images/" + today + "/words.json", i)))
    return words


app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")
app.secret_key = os.getenv("SECRET_KEY")
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
db = SQLAlchemy(app)
bootsrap = Bootstrap(app)



# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

from models import User
from forms import RegistrationForm, LoginForm

@app.before_first_request
def create_tables():
    db.drop_all()
    db.create_all()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('landing'))

@app.route('/landing')
def landing():
    return render_template('landing.html')


@app.route("/", methods=("GET", "POST"))
def index():
    #convert from utc to         mst
    today = datetime.datetime.now()
    today = today - timedelta(hours=7)
    today = today.strftime("%m-%d-%Y")
    # Iterate through 4 times and add it to the end of the today string
    sentence = read_json("./static/images/" + today +
                         "/words.json", "sentence")
    words = read_json("./static/images/" + today + "/words.json", "words")
    ordered_words = order_words(
        [(str.lower(i), read_json("./static/images/" + today + "/words.json", i)) for i in words])
    if 'day' not in session:
        session['day'] = today
    elif session['day'] != today:
        temp = session['stats']
        session.clear()
        session['stats'] = temp
        session['day'] = today
    if 'stats' not in session:
        if "stats" in request.cookies:
            cookieString = request.cookies['stats']
            # Make cookie string a list
            cookieString = cookieString[1:-1]
            cookieString = cookieString.split(",")
            # Convert each element in the list to an int
            cookieString = [int(i) for i in cookieString]
            session['stats'] = cookieString
        else:
            session['stats'] = [0, 0, 0, 0, 0, 0]
    if 'full_sentence' not in session:
        session['full_sentence'] = sentence
    if 'guesses' not in session:
        session['guesses'] = []
    if 'images' not in session:
        session['images'] = []
    if 'done' not in session:
        session['done'] = False
    if 'correct' not in session:
        session['correct'] = []
        for i in ordered_words:
            session['correct'].append("")
    if 'wordlLen' not in session:
        session['wordLen'] = len(ordered_words)
    if not session['done']:
        session['images'] = ['images/'+today+"/"+today +
                             "--" + str(i) + ".png" for i in range(min(len(session['guesses'])+1, 5))]
    else:
        session['images'] = ['images/'+today+"/"+today +
                             "--" + str(i) + ".png" for i in range(5)]
    wordIndexes = get_words_json(ordered_words, today)
    # Get indexs that aren't empty in session['correct']
    indexes = [i for i, x in enumerate(session['correct']) if x != ""]
    # Removes indexes from wordIndexes
    for i in indexes:
        wordIndexes[i] = ""
    session['replaced_sentence'] = replace_words(sentence, wordIndexes)
    if request.method == "POST":
        print(list(request.form.listvalues()))
        # Set cookies to the words that were guessed
        valueList = list(request.form.listvalues())
        # If any value in valueList is empty, return an error
        for i in range(len(valueList)):
            if valueList[i][0] == "":
                return redirect(url_for("index"))

        guessList = []
        for i in range(len(valueList)):
            response = valueList[i][0]
            if check_word(ordered_words[i], response):
                session['word' + str(i)] = "C"
                guessList.append((ordered_words[i], "C"))
                session['correct'][i] = ordered_words[i]
                print("word" + str(i) + " set to C")
            elif check_sentence(response, ordered_words):
                session['word' + str(i)] = "P"
                print("word" + str(i) + " set to P")
                guessList.append((response, "P"))
            else:
                session['word' + str(i)] = "F"
                print("word" + str(i) + " set to F")
                guessList.append((response, "F"))
        print(guessList)
        print(session['stats'])
        session['guesses'].append(guessList)
        # if all the words are guessed correctly, set session['done'] to True
        if all(i != "" for i in session['correct']):
            session['done'] = True
            session['stats'][len(session['guesses'])-1] += 1
        elif len(session['guesses']) == 5:
            session['stats'][5] += 1
        returnVal = make_response(redirect(url_for("index")))
        returnVal.set_cookie("stats", str(session['stats']))
        return returnVal
    if all(i != "" for i in session['correct']):
        session['done'] = True
    return render_template('main.html')
