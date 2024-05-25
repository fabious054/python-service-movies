from flask import Flask, render_template
import requests
import os
from dotenv import load_dotenv
from conection import DatabaseConnector
from dbConnection import DbConnection
import time
from datetime import datetime, timedelta

load_dotenv()
host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_pass = os.getenv('DB_PASS')

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/movies', methods=['GET'])
def home():
    database = DbConnection(host, db_name , db_user, db_pass)
    database.connect()
    query = """CREATE TABLE IF NOT EXISTS app_tmdb_ids (
        id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
        id_tmdb int NOT NULL
    ) COLLATE 'utf8mb3_general_ci';"""
    database.execute(query)
    database.close()

    insertItens = []
    noInsertItens = []
    totalPages = 1
    page = 1
    
    # intervaloAnos = range(2000,datetime.now().year )
    intervaloAnos = range(2000,2030)	
    for year in intervaloAnos:
        # Loop pelos meses
        for month in range(1, 13):
            # Definindo o primeiro dia do mês
            date_start = datetime(year, month, 1).strftime('%Y-%m-%d')
            
            # Definindo o último dia do mês
            last_day = (datetime(year, month, 1) + timedelta(days=31)).replace(day=1) - timedelta(days=1)
            date_end = last_day.strftime('%Y-%m-%d')
            
            # Imprimindo os resultados
            print(f"Intervalo de {date_start} até {date_end}")
            print('+=' * 30)
            url = f"https://api.themoviedb.org/3/discover/movie?language=pt-br&include_adult=false&page={page}&release_date.gte={date_start}&release_date.lte={date_end}"
            print(url)
            print('+=' * 30)

            try:
                connection = DatabaseConnector(url, os.getenv('HEADER_AUTORIZATION'))
                response = connection.connect()
                if response['results'] == []:
                    print (f'Nenhum filme encontrado para a data informada {date_start} até {date_end}')
                    break
                totalPages = response['total_pages']
            except requests.exceptions.RequestException as e:
                print('Erro ao conectar com a API')
                print(e)
                time.sleep(5)
                break

            database = DbConnection(host, db_name, db_user, db_pass)
            database.connect()

            for movie in response['results']:
                consult = f"SELECT * FROM app_tmdb_ids WHERE id_tmdb = {movie['id']}"
                result = database.execute(consult)

                if len(result) > 0:
                    noInsertItens.append('Nao foi inserido pois ja existe no banco de dados o filme informado. ID: ' + str(movie['id']) + ' - ' + movie['title'] + '.')
                    continue

                query = f"INSERT INTO app_tmdb_ids (id_tmdb) VALUES ({movie['id']})"
                database.insert(query)
                insertItens.append(movie)
                print(f"Filme inserido com sucesso: {movie['title']}")
                print(f"Page: {totalPages}")

            database.close()

    retornar = {
        'insertItens': insertItens,
        'noInsertItens': noInsertItens,
        'totalPages': totalPages,
        'totalInsertItens': len(insertItens),
        'totalNoInsertItens': len(noInsertItens)
    }

    return retornar
        
@app.route('/genres', methods=['GET'])
def genres():
    database = DbConnection(host, db_name , db_user, db_pass)
    database.connect()
    query = """CREATE TABLE IF NOT EXISTS app_genres (
        id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
        id_genre int NOT NULL,
        title varchar(40) NOT NULL
    ) COLLATE 'utf8mb3_general_ci';"""
    database.execute(query)
    database.close()

    insertItens = []
    noInsertItens = []

    url = "https://api.themoviedb.org/3/genre/movie/list?language=pt-br"
    connection = DatabaseConnector(url, os.getenv('HEADER_AUTORIZATION'))
    response = connection.connect()
    
    database = DbConnection(host, db_name, db_user, db_pass)
    database.connect()
    
    for genre in response['genres']:

        consult = f"SELECT * FROM app_genres WHERE id_genre = {genre['id']}"
        result = database.execute(consult)

        if len(result) > 0:
            noInsertItens.append('Nao foi inserido pois ja existe no banco de dados o genero informado. ID: ' + str(genre['id']) + ' - ' + genre['name'] + '.')
            continue

        query = f"INSERT INTO app_genres (id_genre, title) VALUES ({genre['id']}, '{genre['name']}')"
        database.insert(query)
        insertItens.append(genre)

    database.close()

    retornar = {
        'insertItens': insertItens,
        'noInsertItens': noInsertItens
    }

    return retornar
  

if __name__ == '__main__':
    app.run(debug=True)