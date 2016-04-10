#!/usr/bin/env python2

from cowpy import cow
from flask import Flask, request, render_template, session
from graphics import hangman
import requests

app = Flask(__name__)
app.secret_key = 'random-secret-string'

def get_word():
    try:
        word = requests.get('http://randomword.setgetgo.com/get.php').text 
    except requests.exceptions.RequestException:
        word = 'hello'
    return word

def make_clue(word):
    return len(word) * ['_']

@app.route('/start', methods=['GET'])
def start():
    word = get_word()
    session['wrong_guesses'] = 0
    session['wrong_letters'] = ''
    session['word'] = word
    session['clue'] = make_clue(word)
    return render_template('start.html', clue=' '.join(make_clue(word)), hangman=hangman(0))

@app.route('/game', methods=['POST'])
def game():
    wrong_guesses = session['wrong_guesses']
    wrong_letters = session['wrong_letters']
    word = session['word']
    clue = session['clue']
    letter = request.form['letter']
    if wrong_letters.find(letter) != -1: # When a wrong letter was gussed that has already been guessed
        return render_template('game.html', letter=letter, wrong_letters=wrong_letters, clue=' '.join(clue), hangman=hangman(wrong_guesses)) 
    elif wrong_guesses >= 5: # Hangman guy has been hanged..
        return render_template('end.html', end=cow.milk_random_cow('you not so smart, the word was ' + word)) 
    else: # Something else
        letter_index = word.find(letter)
        if letter_index != -1: # Correct letter guessed
            for i in range(len(word)):
                if letter == word[i]:
                    clue[i] = letter
            if ''.join(clue) == word: # Word fully guessed
                return render_template('end.html', end=cow.milk_random_cow('you smart, the word was ' + word)) 
            else: # Word not fully guessed yet
                return render_template('game.html', letter=letter, wrong_letters=wrong_letters, clue=' '.join(clue), hangman=hangman(wrong_guesses)) 
        else: # Wrong letter guessed
            session['wrong_letters'] += letter
            session['wrong_guesses'] += 1
            wrong_guesses = session['wrong_guesses']
            wrong_letters = session['wrong_letters']
            return render_template('game.html', letter=letter, wrong_letters=wrong_letters, clue=' '.join(clue), hangman=hangman(wrong_guesses)) 

if __name__ == '__main__':
    app.debug = True
    app.run()
