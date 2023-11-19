# source: https://jss367.github.io/getting-text-from-project-gutenberg.html

import os
from urllib import request
import nltk
import re
from flask import Flask, request, jsonify

app = Flask(__name__)


# define a route for handling POST requests to '/get_text'
@app.route('/get_text', methods=['POST'])
def get_text():
    """
    Handle POST requests to '/get_text' endpoint

    :return: JSON response based on the processing result
    """
    try:
        data = request.get_json()

        # check if 'title', 'author', and 'url' keys are present in the data
        if not all(key in data for key in ['title', 'author', 'url']):
            return jsonify({'error': 'Invalid input data'}), 400
        title = data['title']
        author = data['author']
        url = data['url']
        tokens = text_from_gutenberg(title, author, url, return_tokens=True)

        # check if the result is a list of tokens and return it
        # otherwise return an error response
        if isinstance(tokens, list):
            return jsonify(tokens)
        else:
            error_message = f'Invalid data returned: {tokens}, type: {type(tokens)}'
            return jsonify({'error': error_message}), 500

    # handle exceptions and return an error response
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def text_from_gutenberg(title, author, url, path='books/texts/', return_tokens=False):
    """
    Retrieve and process a text from Project Gutenberg

    :param title: title of the desired text
    :param author: author of the desired text
    :param url: url of the text on Project Gutenberg
    :param path: local path to store or retrieve the text file (default: 'books/texts/')
    :param return_tokens: if True, tokenize the text using NLTK and return the tokens (default: False)
    :return: raw text content or tokens depending on the 'return_tokens' parameter
    """
    try:
        filename = f'{path}{title.lower()}'

        # check if the file is stored locally and is not empty
        if os.path.isfile(filename) and os.stat(filename).st_size != 0:
            with open(filename, 'r') as f:
                raw = f.read()

        # download the text from Project Gutenberg if the file doesn't exist locally
        # and save it as a local file
        else:
            response = request.urlopen(url)
            raw = response.read().decode('utf-8-sig')
            with open(filename, 'w') as outfile:
                outfile.write(raw)

        # option to return tokens
        if return_tokens:
            tokens = tokenize_text(find_beginning_and_end(raw, title, author))
            return tokens
        else:
            return find_beginning_and_end(raw, title, author)

    except Exception as e:
        raise


def find_beginning_and_end(raw, title, author):
    """
    Find the main text from the raw data obtained from Project Gutenberg,
    excluding the Project Gutenberg preamble and postamble

    :param raw: raw text content from Project Gutenberg
    :param title: title of the desired text
    :param author: author of the desired text
    :return: main text content, excluding preamble and postamble
    """
    # find the start pattern in the raw text
    start_regex = '\*\*\*\s?START OF TH(IS|E) PROJECT GUTENBERG EBOOK.*\*\*\*'
    draft_start_position = re.search(start_regex, raw)
    beginning = draft_start_position.end()
    if re.search(title.lower(), raw[draft_start_position.end():].lower()):
        title_position = re.search(title.lower(), raw[draft_start_position.end():].lower())
        beginning += title_position.end()
        if re.search(author.lower(), raw[draft_start_position.end() + title_position.end():].lower()):
            author_position = re.search(author.lower(), raw[draft_start_position.end() + title_position.end():].lower())
            beginning += author_position.end()

    # find the end position of the text
    end_regex = 'end of th(is|e) project gutenberg ebook'
    end_position = re.search(end_regex, raw.lower())
    text = raw[beginning:end_position.start()]

    return text


def tokenize_text(token):
    """
    Tokenize the input text into a list of words using NLTK

    :param token: input text to be tokenized
    :return: list of words obtained by tokenizing the input text
    """
    tokens = nltk.word_tokenize(token)
    return tokens


if __name__ == '__main__':
    app.run(port=3000, debug=True)
