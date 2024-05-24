from flask import Flask
import requests
from dotenv import load_dotenv
import os

load_dotenv()
bearer = os.getenv('HEADER_AUTORIZATION')

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return "THIS API GONNA CHANGE MY LIFE"

@app.route('/movies', methods=['GET'])
def home():
    movies = []

    url = "https://api.themoviedb.org/3/discover/movie?language=pt-br&include_adult=false&page=1&append_to_response=videos&include_video=true"
    payload = {}
    headers = {
        'Authorization ': bearer
    }
    response = requests.request("GET", url, headers=headers, data = payload)
    response = response.json()

    for movie in response['results']:
        # movies.append(movie) com isso, a lista de filmes vai ser uma lista de dicionários com todas as informações do filme (id, title, etc)
        movies.append(movie['title'])
    return str(movies)
        
        
    
    
    return response['results']



    # max_pages = 25
    # movies = []
    # for i in range(1, max_pages):
    #     url = "https://api.themoviedb.org/3/discover/movie?page=" + str(i)
    #     payload = {}
    #     headers = {
    #         'Authorization ': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjMTY5ZDYyYWJmYjI3YzRkYzAzZTBmYzY0M2JkM2NlNiIsInN1YiI6IjYzMTVmYjlmNzEwODNhMDA3YjQ1NTUwNyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.KU3JoGGpWuCLvGOQUDz8V97hAHQyYv6CUuO4xtgSmS4'
    #     }
    #     response = requests.request("GET", url, headers=headers, data = payload)



        
    #     movies.append(response.text.encode('utf8'))
    # return True

if __name__ == '__main__':
    app.run(debug=True)