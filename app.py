from flask import Flask, request, render_template, redirect, url_for 
import pymysql
import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

#11/29/2021 MWC

AZURE_KEY_VAULT_URL = os.environ["AZURE_KEY_VAULT_URL"]

credential = DefaultAzureCredential()
client = SecretClient(vault_url=AZURE_KEY_VAULT_URL, credential=credential)

_dbhostname = client.get_secret('HW12-DBHOSTNAME')
_dbusername = client.get_secret('HW12-DBUSERNAME')
_dbpassword = client.get_secret('HW12-DBPASSWORD')
_dbname = client.get_secret('HW12-DBNAME')
_secret = client.get_secret('HW12-SECRET-KEY')

conn = pymysql.connect(
        host = _dbhostname.value, 
        user = _dbusername.value, 
        password = _dbpassword.value, 
        db = _dbname.value, 
        ssl={'ca': './DigiCertGlobalRootCA.crt.pem'},
        cursorclass = pymysql.cursors.DictCursor)  

app = Flask(__name__)
app.config['SECRET_KEY'] = _secret.value

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/movie/<movie_id>', methods=['GET', 'POST'])
def movie_details(movie_id):
    cur = conn.cursor()
    query = "SELECT * FROM movies WHERE movieId = %s"
    cur.execute(query, movie_id)
    movie = cur.fetchone()
    return render_template('movie-details.html', movie=movie)

@app.route('/movies', methods=['GET'])
def movies():
    cur = conn.cursor()
    query = "SELECT * FROM movies"
    cur.execute(query)
    movies = cur.fetchall()
    return render_template('movies.html', movies=movies)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        form = request.form
        search_value = form['search_string']
        cur = conn.cursor()
        query = "SELECT * FROM movies WHERE title LIKE %(search)s OR releaseYear LIKE %(search)s"
        param_dict = { "search": '%' + search_value + '%' }
        cur.execute(query, param_dict)
        if cur.rowcount > 0:
            results = cur.fetchall()
            return render_template('movies.html', movies=results)
        else:
            return render_template('movies.html', no_match="No matches found for your search.")
    else:
        return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)

