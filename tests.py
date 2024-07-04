from unittest import TestCase

from app import app
from models import db, Cupcake
app.app_context().push()

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

db.drop_all()
db.create_all()


CUPCAKE_DATA = {
    "flavor": "TestFlavor",
    "size": "TestSize",
    "rating": 5,
    "image": "http://test.com/cupcake.jpg"
}

CUPCAKE_DATA_2 = {
    "flavor": "TestFlavor2",
    "size": "TestSize2",
    "rating": 10,
    "image": "http://test.com/cupcake2.jpg"
}


class CupcakeViewsTestCase(TestCase):
    """Tests for views of API."""

    def setUp(self):
        """Make demo data."""

        Cupcake.query.delete()

        cupcake = Cupcake(**CUPCAKE_DATA)
        db.session.add(cupcake)
        db.session.commit()

        self.cupcake = cupcake

    def tearDown(self):
        """Clean up fouled transactions."""

        db.session.rollback()

    def test_list_cupcakes(self):
        with app.test_client() as client:
            resp = client.get("/api/cupcakes")

            self.assertEqual(resp.status_code, 200)

            data = resp.json
            self.assertEqual(data, {
                "cupcakes": [
                    {
                        "id": self.cupcake.id,
                        "flavor": "TestFlavor",
                        "size": "TestSize",
                        "rating": 5,
                        "image": "http://test.com/cupcake.jpg"
                    }
                ]
            })

    def test_get_cupcake(self):
        with app.test_client() as client:
            url = f"/api/cupcakes/{self.cupcake.id}"
            resp = client.get(url)

            self.assertEqual(resp.status_code, 200)
            data = resp.json
            self.assertEqual(data, {
                "cupcake": {
                    "id": self.cupcake.id,
                    "flavor": "TestFlavor",
                    "size": "TestSize",
                    "rating": 5,
                    "image": "http://test.com/cupcake.jpg"
                }
            })

    def test_create_cupcake(self):
        with app.test_client() as client:
            url = "/api/cupcakes"
            resp = client.post(url, json=CUPCAKE_DATA_2)

            self.assertEqual(resp.status_code, 201)

            data = resp.json

            # don't know what ID we'll get, make sure it's an int & normalize
            self.assertIsInstance(data['cupcake']['id'], int)
            del data['cupcake']['id']

            self.assertEqual(data, {
                "cupcake": {
                    "flavor": "TestFlavor2",
                    "size": "TestSize2",
                    "rating": 10,
                    "image": "http://test.com/cupcake2.jpg"
                }
            })

            self.assertEqual(Cupcake.query.count(), 2)

    def test_update_cupcake(self):
        """Tests that the status code is 200 and correct json is being returned for the updated cookie"""
        with app.test_client() as client:
            updated_cupcake={
                "flavor": "Rainbow",
                "size": "TestCreate",
                "rating": 10,
                "image": "http://test.com/cupcake2.jpg"
            }
            resp = client.patch(f'/api/cupcakes/{self.cupcake.id}', json=updated_cupcake)
            
            # makes sure the request was successfully sent
            self.assertEqual(resp.status_code, 200)
            
            # get the json resp
            data = resp.get_json()
            
            # makes sure that the changes are correct 
            self.assertEqual(data['cupcake']['flavor'], "Rainbow")
            self.assertEqual(data['cupcake']['size'], "TestCreate")
            self.assertEqual(data['cupcake']['rating'], 10)
            self.assertEqual(data['cupcake']['image'], "http://test.com/cupcake2.jpg")
            
            # makes sure that the changes were done and corrent in the database.
            cupcake = Cupcake.query.get(self.cupcake.id)
            self.assertEqual(cupcake.flavor, "Rainbow")
            self.assertEqual(cupcake.size, "TestCreate")
            self.assertEqual(cupcake.rating, 10)
            self.assertEqual(cupcake.image, "http://test.com/cupcake2.jpg")
    
    def test_delete_cupcake(self):
        """Tests that the cupcake is deleted from the API and database"""
        with app.test_client() as client:
            resp = client.delete(f'/api/cupcakes/{self.cupcake.id}')
            
            self.assertEqual(resp.status_code, 200)
            
            data = resp.get_json()
            self.assertEqual(data,{'message': 'Deleted'})
            
            cupcake = Cupcake.query.get(self.cupcake.id)
            self.assertIsNone(cupcake)