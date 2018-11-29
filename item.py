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
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {"item": {"name": row[0], "price": row[1]}}

        return {"message": "item not found"}, 404

    def post(self, name):
        if next(filter(lambda x: x["name"] == name, items), None):
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
        price = data["price"]
        item = {"name": name, "price": price}
        items.append(item)
        # 201 is for created
        return item, 201

    def delete(self, name):
        # fixes scoping of item from local -> global

        global items
        items = list(filter(lambda x: x["name"] != name, items))
        return {"message": "item deleted"}, 200

    def put(self, name):
        data = Item.parser.parse_args()
        item = next(filter(lambda x: x["name"] == name, items), None)
        if item is None:
            item = {"name": name, "price": data["price"]}
            items.append(item)
        else:
            item.update(data)
        return item


class ItemList(Resource):
    def get(self):
        return {"items": items}
