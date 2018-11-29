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
        # data = Item.parser.parse_args()
        # item = next(filter(lambda x: x["name"] == name, items), None)
        # if item is None:
        #     item = {"name": name, "price": data["price"]}
        #     items.append(item)
        # else:
        #     item.update(data)
        # return item
        pass


class ItemList(Resource):
    def get(self):
        # return {"items": items}
        pass
