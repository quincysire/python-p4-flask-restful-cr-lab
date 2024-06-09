from app import app, db
from models import Plant

class TestPlant:
    '''Plant model in models.py'''

    def test_can_instantiate(self):
        '''can be instantiated with a name.'''
        p = Plant(name="Douglas Fir")
        assert p
    
    def test_can_be_created(self):
        '''can create records that can be committed to the database.'''
        with app.app_context():
            p = Plant(name="Douglas Fir")
            db.session.add(p)
            db.session.commit()
            assert p.id

            db.session.delete(p)
            db.session.commit()

    def test_can_be_retrieved(self):
        '''can be used to retrieve records from the database.'''
        with app.app_context():
            sample_plant = Plant(name="Sample Plant")
            db.session.add(sample_plant)
            db.session.commit()

            retrieved_plants = Plant.query.all()

            assert retrieved_plants

            db.session.delete(sample_plant)
            db.session.commit()

    def test_can_be_serialized(self):
        '''can create records with a to_dict() method for serialization.'''
        with app.app_context():
            p = Plant(name="Douglas Fir")
            db.session.add(p)
            db.session.commit()
            p_dict = p.to_dict()
            assert((type(p_dict) == dict) and (p_dict["name"] == "Douglas Fir"))
        
            db.session.delete(p)
            db.session.commit()