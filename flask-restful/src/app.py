from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'KIJOASDJKIASJFN4684684#Q$$#$@#%'
api = Api(app)

jwt = JWT(app, authenticate, identity)

items = []

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    @jwt_required()
    def get(self, name):
        item = next(filter(lambda i: i['name'] == name, items), None)
        return {'item': item}, 200 if item else 404

    def post(self, name):
        if next(filter(lambda i: i['name'] == name, items), None):
            return {'message': "An item witg name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()

        item = {'name': name, 'price': data['price']}
        items.append(item)

        return item, 201

    def delete(self, name):
        global items
        items = list(filter(lambda i: i['name'] != name, items))
        return {'message': 'Item deleted'}

    def put(self, name):
        item = next(filter(lambda i: i['name'] == name, items), None)

        data = Item.parser.parse_args()

        if not item:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)
        return item

class ItemList(Resource):
    def get(self):
        return {'items': items}

api.add_resource(ItemList, '/items')
api.add_resource(Item, '/item/<string:name>')

app.run(port=3000, debug=True)
