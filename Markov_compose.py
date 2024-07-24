import string
from Markov_graph import Graph, Vertex
import random
import re
import os

def get_words_from_text(text_path):
    with open(text_path, "r") as f:
        text = f.read()
        # Remove the text inside []
        text = re.sub(r'\[(.+)\]',' ', text)

        # Turn whitespaces into just spaces
        text = ' '.join(text.split())
        text = text.lower()

        text = text.translate(str.maketrans('', '', string.punctuation))

    words = text.split() # Split on spaces again
    return words

def make_graph(words):
    g = Graph()

    previous_word = None
    # For each word check if that word is in the graph and if not, than add it.
    # If there was a previous word, then add an edge if it does not already exist
    # in the graph, otherwise increment weight by 1. 
    # Set  our word to the previous word and iterate!

    for word in words:
        # Check if that word is in the graph and if not than add it
        word_vertex = g.get_vertex(word)

        # If there was a previous word, then add an edge if it does not already exist
        # in the graph, otherwise increment weight by 1
        if previous_word:
            previous_word.increment_edge(word_vertex)
        
        # Set our word to the previous word and iterate!
        previous_word = word_vertex
    
    # Generate probability mappings before composing
    g.generate_probability_mappings()

    return g

def compose(g, words, lenght = 50):
    composition = []
    word = g.get_vertex(random.choice(words)) # Pick a random word to start!
    for _ in range(lenght):
        composition.append(word.value)
        word = g.get_next_word(word)
    
    return composition

def main(artist):
    # Get words from the text
    # words = get_words_from_text('songs/avicii/1_Wake-me-up.txt')

    words = []
    for song_file in os.listdir(f'songs/{artist}'):
        if song_file == '.DS_Store':
            continue
        song_words = get_words_from_text(f'songs/{artist}/{song_file}')
        words.extend(song_words)
    g = make_graph(words)

    composition = compose(g, words, 100)
    # Return a string, where all the words are separated by a space
    return ' '.join(composition) 

if __name__ == '__main__':
    print(main('taylor_swift'))