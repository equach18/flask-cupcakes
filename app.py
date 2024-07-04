"""Flask app for Cupcakes"""
from flask import Flask, request, render_template, redirect, jsonify
from models import db, connect_db, Cupcake


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///cupcakes"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'shhhheeecret'

connect_db(app)

@app.route('/')
def root():
    """Renders the homepage."""
    return render_template("index.html")


@app.route('/api/cupcakes')
def list_cupcakes():
    """Return data of all cupcakes in JSON"""
    cupcakes = [cupcake.serialize_cupcake() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=cupcakes)

@app.route('/api/cupcakes/<int:cupcake_id>')
def get_cupcake(cupcake_id):
    """Returns the data of the single cupcake in JSON"""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    return jsonify(cupcake=cupcake.serialize_cupcake())

@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    """Creates a cupcake with flavor, size, rating, and img from the body of the request. Returns the data of the new cupcake in JSON"""
    data = request.json
    cupcake = Cupcake(flavor = data['flavor'],
                      size = data['size'],
                      rating = data['rating'],
                      image = data['image'] or None)
    db.session.add(cupcake)
    db.session.commit()
    return (jsonify(cupcake=cupcake.serialize_cupcake()),201)

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['PATCH'])
def update_cupcake(cupcake_id):
    """Updates a cupcake from the body of the request. Returns the updated cookie data in JSON"""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    
    cupcake.flavor = request.json['flavor']
    cupcake.size = request.json['size']
    cupcake.rating = request.json['rating']
    cupcake.image = request.json['image']
    
    db.session.add(cupcake)
    db.session.commit()
    return jsonify(cupcake=cupcake.serialize_cupcake())

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['DELETE'])
def delete_cupcake(cupcake_id):
    """Deletes the cupcake"""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message="Deleted")

