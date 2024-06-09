from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api, Resource, reqparse
from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    def get(self):
        plants = Plant.query.all()
        formatted_plants = [{
            'id': plant.id,
            'name': plant.name,
            'image': plant.image,
            'price': plant.price
        } for plant in plants]
        return formatted_plants

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help='Name is required')
        parser.add_argument('image', type=str, required=True, help='Image URL is required')
        parser.add_argument('price', type=float, required=True, help='Price is required')
        args = parser.parse_args()

        new_plant = Plant(
            name=args['name'],
            image=args['image'],
            price=args['price']
        )
        db.session.add(new_plant)
        db.session.commit()
        return {
            'id': new_plant.id,
            'name': new_plant.name,
            'image': new_plant.image,
            'price': new_plant.price
        }, 201

class PlantByID(Resource):
    def get(self, plant_id):
        session = db.session
        plant = session.query(Plant).get(plant_id)
        if plant:
            return {
                'id': plant.id,
                'name': plant.name,
                'image': plant.image,
                'price': plant.price
            }
        else:
            return {'error': 'Plant not found'}, 404

api.add_resource(Plants, '/plants')
api.add_resource(PlantByID, '/plants/<int:plant_id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)