from flask import Flask, request, render_template, redirect, url_for
import pymysql
import os
import logging
import platform
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

# 11/10/2023 MWC

# create logger
logging.basicConfig(
    level=logging.INFO,
    filename="log_file.log",
    filemode="a",  # append to the log file
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logging.info("Loading variables from Azure Key Vault")

AZURE_KEY_VAULT_URL = os.environ["AZURE_KEY_VAULT_URL"]

credential = DefaultAzureCredential()
client = SecretClient(vault_url=AZURE_KEY_VAULT_URL, credential=credential)

_dbhostname = client.get_secret("HW13-DBHOSTNAME")
_dbusername = client.get_secret("HW13-DBUSERNAME")
_dbpassword = client.get_secret("HW13-DBPASSWORD")
_dbname = client.get_secret("HW13-DBNAME")
_secret = client.get_secret("HW13-SECRET-KEY")

conn = pymysql.connect(
    host=_dbhostname.value,
    user=_dbusername.value,
    password=_dbpassword.value,
    db=_dbname.value,
    ssl={"ca": "./DigiCertGlobalRootCA.crt.pem"},
    cursorclass=pymysql.cursors.DictCursor,
)

logging.info("Starting Flask app")

app = Flask(__name__)
app.config["SECRET_KEY"] = _secret.value


@app.route("/", methods=["GET"])
def index():
    logging.info("Index page")
    return render_template("index.html")


@app.route("/movie/<movie_id>", methods=["GET", "POST"])
def movie_details(movie_id):
    cur = conn.cursor()
    query = "SELECT * FROM movies WHERE movieId = %s"
    cur.execute(query, movie_id)
    movie = cur.fetchone()
    return render_template("movie-details.html", movie=movie)


@app.route("/movies", methods=["GET"])
def movies():
    cur = conn.cursor()
    query = "SELECT * FROM movies"
    cur.execute(query)
    movies = cur.fetchall()
    logging.info("All movies page")
    return render_template("movies.html", movies=movies)


@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        form = request.form
        search_value = form["search_string"]
        cur = conn.cursor()
        query = "SELECT * FROM movies WHERE title LIKE %(search)s OR releaseYear LIKE %(search)s"
        param_dict = {"search": "%" + search_value + "%"}
        cur.execute(query, param_dict)
        if cur.rowcount > 0:
            results = cur.fetchall()
            logging.info("Search results page")
            return render_template("movies.html", movies=results)
        else:
            logging.info("No matches found for search")
            return render_template(
                "movies.html", no_match="No matches found for your search."
            )
    else:
        return redirect(url_for("index"))


@app.route("/diagnostics", methods=["GET"])
def diagnostics():
    # borrowed from https://github.com/balarsen/FlaskStatus
    # borrowed from https://github.com/practisec/pwnedhub/blob/master/pwnedhub/views/core.py

    platform_stats = {
        "architecture": platform.architecture(),
        "machine": platform.machine(),
        "node": platform.node(),
        "platform": platform.platform(),
        "processor": platform.processor(),
        "python_branch": platform.python_branch(),
        "python_build": platform.python_build(),
        "python_compiler": platform.python_compiler(),
        "python_implementation": platform.python_implementation(),
        "python_revision": platform.python_revision(),
        "python_version": platform.python_version(),
        "python_version_tuple": platform.python_version_tuple(),
        "release": platform.release(),
        "system": platform.system(),
        "uname": platform.uname(),
        "version": platform.version(),
        "java_ver": platform.java_ver(),
        "win32_ver": platform.win32_ver(),
        "mac_ver": platform.mac_ver(),
        "libc_ver": platform.libc_ver(),
        "load_average": os.getloadavg(),
    }

    log_stats = []
    log_files = [
        #     "/tmp/gunicorn-pwnedapi.log",
        #     "/tmp/gunicorn-pwnedhub.log",
        #     "/tmp/gunicorn-pwnedspa.log",
        #     "/tmp/gunicorn-pwnedsso.log",
        #     "/var/log/nginx/access.log",
        "./log_file.log",
    ]
    for log_file in log_files:
        if os.path.exists(log_file):
            data = {
                "name": log_file,
                "size": os.path.getsize(log_file),
                "mtime": os.path.getmtime(log_file),
                "ctime": os.path.getctime(log_file),
                "tail": [],
            }
            with open(log_file) as fp:
                data["tail"] = "".join(fp.readlines()[-20:])
            log_stats.append(data)

    return render_template(
        "diagnostics.html", platform_stats=platform_stats, log_stats=log_stats
    )

    # return render_template("diagnostics.html", platform_stats=platform_stats)


if __name__ == "__main__":
    app.run(debug=False)
