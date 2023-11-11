# HW12-BAIS3400

BAIS:3400/6400 - homework using App Services, MySQL, Active Directory, and Key Vault to create a database driven web application.

- [ ] Create a database class to create a connection, execute a query and close the connection

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
- [ ] Create a navbar
- [ ] Create a robots.txt
- [ ] Create an "accept" for data collection
- [ ] Create some queries and menu item for most popular, shortest, longest, etc.
