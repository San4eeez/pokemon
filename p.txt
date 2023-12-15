import requests
import psycopg2
from psycopg2 import extras
import json

def create_database_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pokemon (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            height DECIMAL,
            weight DECIMAL,
            base_experience INTEGER,
            types JSONB,
            abilities JSONB,
            stats JSONB
        )
    """)
    print("[+] created `pokemon` table")

def fetch_pokemon_data(url):
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()['results']
    else:
        print("Ошибка при получении данных:", response.status_code)
        return []
    
def get_pokemon_details(url):
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json(parse_float=lambda x: float(x) if '.' in x else int(x))
        name = data['name']
        height = data['height']
        weight = data['weight']
        base_experience = data['base_experience']
        
        types_data = data['types']
        types = [t['type']['name'] for t in types_data]

        abilities_data = data['abilities']
        abilities = [t['ability']['name'] for t in abilities_data]
        
        stats_data = data['stats']
        stats = [f'"{t['stat']['name']}":"{t['base_stat']}' for t in stats_data]

        return name, height, weight, base_experience, types, abilities, stats
    else:
        print("Ошибка при получении данных о покемоне:", response.status_code)
        return None



def insert_pokemon_data(cursor, name, height, weight, base_experience, types, abilities, stats):
    cursor.execute("""
        INSERT INTO pokemon (name, height, weight, base_experience, types, abilities, stats)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (name, height, weight, base_experience, json.dumps(types), json.dumps(abilities), json.dumps(stats)))
    print(f"[+] Inserted `{name}`")


def main():
    
    conn = psycopg2.connect(
    host="localhost",
    database="pokemonDB",
    user="postgres",
    password="admin"
   
)
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    # Создание таблицы в базе данных PostgreSQL
    create_database_table(cursor)

    # Запрос к API для получения информации о покемонах
    url = "https://pokeapi.co/api/v2/pokemon/?limit=10"
    pokemon_list = fetch_pokemon_data(url)

    # Обработка данных и сохранение в базу данных
    for pokemon in pokemon_list:
        name, height, weight, base_experience, types, abilities, stats = get_pokemon_details(pokemon['url'])

        # Вставка данных в базу данных
        if name is not None:
            insert_pokemon_data(cursor, name, height, weight, base_experience, types, abilities, stats)

    # Закрытие соединения с базой данных
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
