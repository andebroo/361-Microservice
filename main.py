# source: https://jss367.github.io/getting-text-from-project-gutenberg.html

import os
from urllib import request
import nltk
import re


def text_from_gutenberg(title, author, url, path='books/texts/', return_tokens=False):
    """
    Retrieve and process a text from Project Gutenberg

    :param title: title of the desired text
    :param author:  author of the desired text
    :param url: url of the text on Project Gutenberg
    :param path: local path to store or retrieve the text file (default: 'books/texts/')
    :param return_tokens: if True, tokenize the text using NLTK and return the tokens (default: False)
    :return:  raw text content or tokens depending on the 'return_tokens' parameter
    """
    # check if the file is stored locally
    # need to have a folder named books/texts/
    filename = f'{path}{title.lower()}'

    # if the file exists in the folder, read its content
    if os.path.isfile(filename) and os.stat(filename).st_size != 0:
        with open(filename, 'r') as f:
            raw = f.read()

    # if the file does not exist in the folder, download it from Project Gutenberg
    # https://www.gutenberg.org/
    else:
        # print(f"{title} file does not already exist. Grabbing from Project Gutenberg")
        response = request.urlopen(url)
        raw = response.read().decode('utf-8-sig')
        # print(f"Saving {title} file")
        with open(filename, 'w') as outfile:
            outfile.write(raw)

    # option to return tokens
    # if specified, tokenize the text and return the tokens
    if return_tokens:
        return tokenize_text(find_beginning_and_end(raw, title, author))

    # return the raw text without tokenization
    else:
        return find_beginning_and_end(raw, title, author)


def find_beginning_and_end(raw, title, author):
    """
    Find the main text from the raw data obtained from Project Gutenberg,
    excluding the Project Gutenberg preamble and postamble.

    :param raw: raw text content from Project Gutenberg
    :param title: title of the desired text
    :param author: author of the desired text
    :return: main text content, excluding preamble and postamble
    """
    # find the position of the start pattern in the raw text
    start_regex = '\*\*\*\s?START OF TH(IS|E) PROJECT GUTENBERG EBOOK.*\*\*\*'
    draft_start_position = re.search(start_regex, raw)
    beginning = draft_start_position.end()

    # check if the title is present in the main text
    if re.search(title.lower(), raw[draft_start_position.end():].lower()):
        title_position = re.search(title.lower(), raw[draft_start_position.end():].lower())
        beginning += title_position.end()
        # If the title is present, check for the author's name as well
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
    Tokenize the input text into a list of words using NLTK.

    :param token: input text to be tokenized
    :return: list of words obtained by tokenizing the input text
    """
    return nltk.word_tokenize(token)


# example
# title = 'Romeo and Juliet'
# author = 'William Shakespeare'
# url = 'https://www.gutenberg.org/cache/epub/1513/pg1513.txt'
# path = 'corpora/canon_texts/'
# text = text_from_gutenberg(title, author, url, return_tokens=True)
# print(text)
