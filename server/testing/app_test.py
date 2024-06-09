import json
import unittest
from app import app, db
from models import Plant

class TestPlant(unittest.TestCase):
    '''Flask application in app.py'''

    def setUp(self):
        # Set up the Flask test client
        self.app = app.test_client()

        # Ensure that the plant with ID 1 doesn't exist in the test database
        with app.app_context():
            existing_plant = db.session.query(Plant).get(1)
            if existing_plant:
                db.session.delete(existing_plant)
                db.session.commit()

        with app.app_context():
           plant = Plant(id=1, name="Test Plant", image="test_image", price=10.00)
           db.session.add(plant)
           db.session.commit()

    def tearDown(self):
        # Clean up the database after each test
        with app.app_context():
            existing_plant = db.session.query(Plant).get(1)
            if existing_plant:
                db.session.delete(existing_plant)
                db.session.commit()

    def test_plants_get_route(self):
        '''has a resource available at "/plants".'''
        response = self.app.get('/plants')
        assert response.status_code == 200

    def test_plants_get_route_returns_list_of_plant_objects(self):
        '''returns JSON representing Plant objects at "/plants".'''
        with app.app_context():
            p = Plant(name="Douglas Fir")
            db.session.add(p)
            db.session.commit()

            response = self.app.get('/plants')
            data = response.json
            assert isinstance(data, list)
            for record in data:
                assert isinstance(record, dict)
                assert record.get('id')
                assert record.get('name')

            db.session.delete(p)
            db.session.commit()

    def test_plants_post_route_creates_plant_record_in_db(self):
        '''allows users to create Plant records through the "/plants" POST route.'''
        response = self.app.post(
            '/plants',
            json={
                "name": "Live Oak",
                "image": "https://www.nwf.org/-/media/NEW-WEBSITE/Shared-Folder/Wildlife/Plants-and-Fungi/plant_southern-live-oak_600x300.ashx",
                "price": 250.00,
            }
        )

        assert response.status_code == 201  # 201 status code for successful creation

        with app.app_context():
            lo = db.session.query(Plant).filter_by(name="Live Oak").first()
            assert lo
            assert lo.name == "Live Oak"
            assert lo.image == "https://www.nwf.org/-/media/NEW-WEBSITE/Shared-Folder/Wildlife/Plants-and-Fungi/plant_southern-live-oak_600x300.ashx"
            assert lo.price == 250.00

            db.session.delete(lo)
            db.session.commit()

    def test_plant_by_id_get_route(self):
        '''has a resource available at "/plants/<int:id>".'''
        # Create a plant with ID 1 in the test database
        with app.app_context():
            plant = Plant(id=1, name="Test Plant")
            db.session.add(plant)
            db.session.commit()

        response = self.app.get('/plants/1')
        assert response.status_code == 200  # Assuming the plant with ID 1 exists

    def test_plant_by_id_get_route_returns_one_plant(self):
        '''returns JSON representing one Plant object at "/plants/<int:id>".'''
        response = self.app.get('/plants/1')
        data = response.json

        assert response.status_code == 200  # Assuming the plant with ID 1 exists
        assert "error" not in data  # Check that there is no "error" key in the JSON response

if __name__ == '__main__':
    unittest.main()