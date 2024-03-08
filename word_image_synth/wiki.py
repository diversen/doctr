import json
import logging
import os

import requests
from bs4 import BeautifulSoup


def get_random_words(lang="da", vocab=None):
    """
    Get a random page from Wikipedia
    vacob is a list of allowed chars to be used
    """
    url = requests.get(f"https://{lang}.wikipedia.org/wiki/Special:Random")
    soup = BeautifulSoup(url.content, "html.parser")

    # get article text
    article_text = soup.find_all("p")

    # Remove all html tags
    p_content = [tag.get_text() for tag in article_text]

    # remove all newlines
    p_content = [word.replace("\n", "") for word in p_content]

    # trim all words
    p_content = [word.strip() for word in p_content]

    # split list of p tag content into words
    words = " ".join(p_content).split(" ")

    # remove all non-allowed chars
    if vocab:
        words = [word for word in words if all(char in vocab for char in word)]

    # remove empty words
    words = [word for word in words if word]



    return words


def generate_num_words(json_file, max_words, vocab):
    """
    Generate a number of words from Wikipedia
    and saving them to a json file
    The json file will keep track of all words generated
    """
    # if words.json exists then open it
    if os.path.exists(json_file):
        with open("words.json", "r", encoding="utf-8") as f:
            words = json.load(f)
    else:
        words = []

    while True:
        wiki_words = get_random_words("da", vocab)
        words.extend(wiki_words)

        # save words to words.json
        with open(json_file, "w", encoding="utf-8") as f:
            # only save unique words
            words = list(set(words))

            # Sort 
            words.sort()
            json.dump(words, f, ensure_ascii=False, indent=4)

        logging.info(f"Saved {len(words)} words to words.json")

        # break if max words is reached
        if len(words) >= max_words:
            break
