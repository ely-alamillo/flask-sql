from security import authenticate, identity
from flask import Flask, request
from flask_restful import Resource, Api, reqparse

# from flask_jwt import JWT, jwt_required
from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    create_access_token,
    get_jwt_identity,
)


app = Flask(__name__)
api = Api(app)

app.config["JWT_SECRET_KEY"] = "secretkeyboyz"

jwt = JWTManager(app)

items = []


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "price", type=float, required=True, help="Price cannot be blank."
    )

    @jwt_required
    def get(self, name):
        item = next(filter(lambda x: x["name"] == name, items), None)

        return {"item": item}, 200 if item else 404

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


class Auth(Resource):
    def post(self):
        if not request.is_json:
            return {"message": "request malformed."}, 400

        username = request.json.get("username", None)
        password = request.json.get("password", None)

        if not username:
            return {"message": "Missing username"}, 400

        if not password:
            return {"message": "Missing password"}, 400

        user = authenticate(username, password)

        if not user:
            return {"message": "invalid login credentials"}, 401

        access_token = create_access_token(identity=user.id)
        return {"access_token": access_token}, 200


api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(Auth, "/auth")

app.run(port=5000, debug=True)
