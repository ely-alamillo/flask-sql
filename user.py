import sqlite3
from flask_restful import Resource, request, reqparse


class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username=?"
        # value always needs to be a tuple
        # otherwise braces are useless
        # (4 + 3) + 2
        result = cursor.execute(query, (username,))
        row = result.fetchone()

        if row:
            # user = cls(row[0], row[1], row[2])
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id=?"
        # value always needs to be a tuple
        # otherwise braces are useless
        # (4 + 3) + 2
        result = cursor.execute(query, (_id,))
        row = result.fetchone()

        if row:
            # user = cls(row[0], row[1], row[2])
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "username", type=str, required=True, help="Username cannot be blank"
    )
    parser.add_argument(
        "password", type=str, required=True, help="Password cannot be blank"
    )

    def post(self):
        data = UserRegister.parser.parse_args()

        if User.find_by_username(data["username"]):
            return {"message": "A user with this username already exists"}, 400

        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        user = (data["username"], data["password"])

        cursor.execute(query, user)
        connection.commit()

        connection.close()

        # 201 resource created
        return {"message": "User created successfully."}, 201
