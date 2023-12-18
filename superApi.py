from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSONB

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/pokemonDB'
db = SQLAlchemy(app)

class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    height = db.Column(db.Float)
    weight = db.Column(db.Float)
    types = db.Column(JSONB)
    abilities = db.Column(JSONB)
    hp = db.Column(db.Integer)
    attack = db.Column(db.Integer)
    defense = db.Column(db.Integer)
    special_attack = db.Column(db.Integer)
    special_defense = db.Column(db.Integer)
    speed = db.Column(db.Integer)

    def __init__(self, name, height, weight, types, abilities, hp, attack, defense, special_attack, special_defense, speed):
        self.name = name
        self.height = height
        self.weight = weight
        self.types = types
        self.abilities = abilities
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.special_attack = special_attack
        self.special_defense = special_defense
        self.speed = speed

# Создание таблицы в базе данных
with app.app_context():
    db.create_all()

@app.route('/api/pokemon', methods=['GET'])
def get_pokemon():
    pokemon_list = Pokemon.query.all()
    result = [
        {
            'id': item.id,
            'name': item.name,
            'height': item.height,
            'weight': item.weight,
            'types': item.types,
            'abilities': item.abilities,
            'hp': item.hp,
            'attack': item.attack,
            'defense': item.defense,
            'special_attack': item.special_attack,
            'special_defense': item.special_defense,
            'speed': item.speed
        }
        for item in pokemon_list
    ]
    return jsonify(result)

@app.route('/api/pokemon/<int:pokemon_id>', methods=['GET'])
def get_single_pokemon(pokemon_id):
    pokemon = Pokemon.query.get(pokemon_id)
    if pokemon:
        return jsonify({
            'id': pokemon.id,
            'name': pokemon.name,
            'height': pokemon.height,
            'weight': pokemon.weight,
            'types': pokemon.types,
            'abilities': pokemon.abilities,
            'hp': pokemon.hp,
            'attack': pokemon.attack,
            'defense': pokemon.defense,
            'special_attack': pokemon.special_attack,
            'special_defense': pokemon.special_defense,
            'speed': pokemon.speed
        })
    else:
        return jsonify({'message': 'Pokemon not found'}), 404

@app.route('/api/pokemon', methods=['POST'])
def add_pokemon():
    data = request.get_json()
    new_pokemon = Pokemon(
        name=data['name'],
        height=data['height'],
        weight=data['weight'],
        types=data['types'],
        abilities=data['abilities'],
        hp=data['hp'],
        attack=data['attack'],
        defense=data['defense'],
        special_attack=data['special_attack'],
        special_defense=data['special_defense'],
        speed=data['speed']
    )
    db.session.add(new_pokemon)
    db.session.commit()
    return jsonify({'message': 'Pokemon added successfully'})

@app.route('/api/pokemon/<int:pokemon_id>', methods=['PUT'])
def update_pokemon(pokemon_id):
    pokemon = Pokemon.query.get(pokemon_id)
    if pokemon:
        data = request.get_json()
        pokemon.name = data['name']
        pokemon.height = data['height']
        pokemon.weight = data['weight']
        pokemon.types = data['types']
        pokemon.abilities = data['abilities']
        pokemon.hp = data['hp']
        pokemon.attack = data['attack']
        pokemon.defense = data['defense']
        pokemon.special_attack = data['special_attack']
        pokemon.special_defense = data['special_defense']
        pokemon.speed = data['speed']
        db.session.commit()
        return jsonify({'message': 'Pokemon updated successfully'})
    else:
        return jsonify({'message': 'Pokemon not found'}), 404

@app.route('/api/pokemon/<int:pokemon_id>', methods=['DELETE'])
def delete_pokemon(pokemon_id):
    pokemon = Pokemon.query.get(pokemon_id)
    if pokemon:
        db.session.delete(pokemon)
        db.session.commit()
        return jsonify({'message': 'Pokemon deleted successfully'})
    else:
        return jsonify({'message': 'Pokemon not found'}), 404

@app.route('/api/pokemon/abilities/<string:ability>', methods=['GET'])
def get_pokemon_by_ability(ability):
    pokemon_list = Pokemon.query.filter(Pokemon.abilities.contains([ability])).all()
    result = [
        {
            'id': item.id,
            'name': item.name,
            'height': item.height,
            'weight': item.weight,
            'types': item.types,
            'abilities': item.abilities,
            'hp': item.hp,
            'attack': item.attack,
            'defense': item.defense,
            'special_attack': item.special_attack,
            'special_defense': item.special_defense,
            'speed': item.speed
        }
        for item in pokemon_list
    ]
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)

