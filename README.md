# 3400/6400 - Movies web application

BAIS:3400/6400 - homework using Azure App Services and Azure Database for MySQL to create a database driven web application. Connection to MySQL is made using environment variables on Azure App Service.

---

![Python badge](https://img.shields.io/static/v1?message=python&logo=python&labelColor=3776AB&color=3776AB&logoColor=white&label=%20&style=for-the-badge) ![Flask badge](https://img.shields.io/static/v1?message=Flask&logo=Flask&labelColor=000000&color=000000&logoColor=white&label=%20&style=for-the-badge) ![Bootstrap 5 badge](https://img.shields.io/static/v1?message=Bootstrap%205&logo=bootstrap&labelColor=7952B3&color=7952B3&logoColor=white&label=%20&style=for-the-badge) ![Azure badge](https://img.shields.io/badge/Microsoft_Azure-0089D6?style=for-the-badge&logo=microsoft-azure&logoColor=white) ![University of Iowa badge](https://img.shields.io/static/v1?message=Hawks!!&labelColor=000000&color=FFCD00&label=Go&style=for-the-badge)

## Installation

1. Clone this repository to local computer

2. Create a new virtual environment

   - Windows: `python -m venv ./venv`
   - Mac: `python3 -m venv ./venv`

3. Activate the new virtual environment

   - Windows: `.\venv\Scripts\activate`
   - Mac: `source ./venv/bin/activate`

4. Install the dependencies `pip install -r requirements.txt`

5. Run the application with `flask run` or `python app.py`

## Local testing and development

1. For local testing and development you will need to create a .env file that contains details about connecting to your database server.

_Example .env file_

```
HW13_DBHOSTNAME = **_paste in the hostname of your MySQL server_**
HW13_DBNAME = movie_data
HW13_DBUSERNAME = movies_app
HW13_DBPASSWORD = **_paste in the correct password from the .sql file_**
HW13_SECRET_KEY = RdzYTY0FEfLXmdTc44hcMWENtnqFlB
```

2. For local testing you may also want to set `debug=True` in the last line of code.

---

## To Do List

- [x] Create a database helper class to create a connection, execute a query and close the connection - ideas in email (11/10/2023)

https://zetcode.com/python/pymysql/  
https://www.tutorialspoint.com/python/python_database_access.htm

```
mydb = MySQLdb.connect(host=host, user=user, passwd=passwd, db=database, charset="utf8")
cursor = mydb.cursor()
query = "INSERT INTO tablename (text_for_field1, text_for_field2, text_for_field3, text_for_field4) VALUES (%s, %s, %s, %s)"
cursor.execute(query, (field1, field2, field3, field4))
mydb.commit()
cursor.close()
mydb.close()
```

- [ ] Is logging appropriate?
- [ ] Can I read other logs with /diagnostics?
- [x] Create a navbar
- [ ] Create a robots.txt
- [ ] Create an "accept" for data collection
- [ ] Create some queries and menu item for most popular, shortest, longest, etc.
- [ ] Individual movie images
- [ ] Updated movies data
- [ ] Properly constructed database tables
- [ ] Add a "no record found" if no movies are found on a search
- [ ] Add custom error pages
- [ ] Add an admin interface
- [x] Update to Flask 3
- [ ] format pagination on movies.html
- [ ] Add a footer

---

## Change log

04/21/2025 - Removed Azure Key Vault functionality. Azure Entra ID access removed by University.
11/10/2023 - Added /diagnostics  
11/10/2023 - Added logging  
11/10/2023 - Added Bootstrap 5.2 for styling including navbar  
11/10/2023 - Web app is loaded and working  
11/10/2023 - Created database class  
04/17/2024 - "All movies" results sorted ascending by title  
04/17/2024 - Added total movie results count to page  
04/17/2024 - Added page headers for "All movies" and search results  
04/17/2024 - Updated to Flask 3
