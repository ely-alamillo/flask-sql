import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "price", type=float, required=True, help="Price cannot be blank."
    )

    @jwt_required
    def get(self, name):
        item = self.find_by_name(name)
        if item:
            return item
        return {"message": "item not found"}, 404

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {"item": {"name": row[0], "price": row[1]}}

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (item["name"], item["price"]))

        connection.commit()
        connection.close()

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (item["price"], item["name"]))

        connection.commit()
        connection.close()

    def post(self, name):
        if self.find_by_name(name):
            # 400 bad request
            return (
                {
                    "message": "An item with name '{}' already exists".format(
                        name
                    )
                },
                400,
            )

        data = Item.parser.parse_args()
        item = {"name": name, "price": data["price"]}

        try:
            self.insert(item)
        except:
            # 500 internal server error, not your fault ours
            return {"message": "an error occured inserting the item"}, 500

        # 201 is for created
        return item, 201

    def delete(self, name):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        return {"message": "item deleted"}, 200

    def put(self, name):
        data = Item.parser.parse_args()

        item = self.find_by_name(name)
        updated_item = {"name": name, "price": data["price"]}

        if item is None:
            try:
                self.insert(updated_item)
            except:
                return {"message": "an errro occured creating the item"}, 500
        else:
            try:
                self.update(updated_item)
            except:
                return {"message": "an error occured updating the item"}, 500
        return updated_item


class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * from items"
        result = cursor.execute(query)
        items = list()
        for row in result:
            items.append({"name": row[0], "price": row[1]})

        connection.commit()
        connection.close()

        return {"items": items}
