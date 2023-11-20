# 361-Microservice
Microservice project for CS 361 that communicates via JSON to obtain a title from Project Gutenberg and return the formatted text if the title exists.

## Usage
To use the microservice:
1. Download the code posted under `main.py` to use locally. To run the microservice locally, execute the following command: python main.py
The microservice will be available on http://localhost:3000 by default.
3. Install dependencies using `pip install -r requirements.txt` (if applicable).
4. In your project, provide an HTTP POST request to the microservice with a JSON body that includes the title and author of the desired book, as well as the Plain Text UTF-8 URL link.
   JSON body example:
       {
          "title": "Romeo and Juliet",
          "author": "William Shakespeare",
          "url": "https://www.gutenberg.org/cache/epub/1112/pg1112.txt"
       }
5. The microservice returns the text data in the form of a list of strings.
   Example:
      ["Contents", "THE", "PROLOGUE", ".", "ACT", "I", "Scene", "I", ".", "A", "public", "place", ".", "Scene", "II", ".", "A", "Street", ".", "Scene", "III", ".", "Room", "in", "Capulet"]

6. If the title doesn't exist on Project Gutenberg or there is an issue with the request, the microservice will return an appropriate error response.


