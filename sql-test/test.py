import sqlite3

connection = sqlite3.connect("data.db")

cursor = connection.cursor()

create_table = "CREATE TABLE users (id int, username text, password text)"

cursor.execute(create_table)

# create table users
insert_user = "INSERT INTO users VALUES (?,?,?)"

# insert users into table user
user = (1, "ely", "password")
users = [(2, "john", "password"), (3, "jane", "password")]
cursor.execute(insert_user, user)
cursor.executemany(insert_user, users)

# select users form users table
select_users = "SELECT * FROM users"
for row in cursor.execute(select_users):
    print(row)


# save the user
connection.commit()
connection.close()
