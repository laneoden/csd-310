import mysql.connector

# Database configuration
db_config = {
    "user": "movies_user",
    "password": "popcorn",
    "host": "127.0.0.1",
    "database": "movies",
    "raise_on_warnings": True
}

# Define the function to display film information
def show_films(cursor, title):
    cursor.execute("""
        SELECT
            film.film_name AS Name,
            film.film_director AS Director,
            genre.genre_name AS Genre,
            studio.studio_name AS 'Studio Name'
        FROM film
        INNER JOIN genre ON film.genre_id = genre.genre_id
        INNER JOIN studio ON film.studio_id = studio.studio_id
    """)

    films = cursor.fetchall()

    print("\n  -- {} --".format(title))

    for film in films:
        print("Film Name: {}\nDirector: {}\nGenre: {}\nStudio: {}\n".format(film[0], film[1], film[2], film[3]))

# Function to insert a new film record
def insert_film(cursor):
    film_name = input("Enter Film Name: ")
    film_director = input("Enter Director Name: ")
    genre_id = int(input("Enter Genre ID (1: Horror, 2: SciFi, 3: Drama): "))
    studio_id = int(input("Enter Studio ID (1: 20th Century Fox, 2: Blumhouse Productions, 3: Universal Pictures): "))
    release_year = input("Enter Release Year (YYYY, optional): ")
    film_runtime = int(input("Enter Film Runtime (in minutes): "))  # Prompt for film runtime

    insert_query = """
    INSERT INTO film (film_name, film_director, genre_id, studio_id, film_releaseDate, film_runtime)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    insert_data = (film_name, film_director, genre_id, studio_id, release_year, film_runtime)
    cursor.execute(insert_query, insert_data)
    print("Inserted new film record: {}".format(film_name))

# Function to update a film's genre
def update_film_genre(cursor, film_name, new_genre_id):
    update_query = """
    UPDATE film
    SET genre_id = %s
    WHERE film_name = %s
    """
    update_data = (new_genre_id, film_name)
    cursor.execute(update_query, update_data)
    print("Updated genre of film '{}' to new genre ID: {}".format(film_name, new_genre_id))

# Function to delete a film record
def delete_film(cursor, film_name):
    delete_query = """
    DELETE FROM film
    WHERE film_name = %s
    """
    delete_data = (film_name,)
    cursor.execute(delete_query, delete_data)
    print("Deleted film record: {}".format(film_name))

# Connect to MySQL database
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# Display films before any modifications
show_films(cursor, "-- DISPLAYING FILMS --")

# Insert a new film with user input
insert_film(cursor)

# Display films after insertion
show_films(cursor, "-- DISPLAYING FILMS AFTER INSERT --")

# Update film 'Alien' to Horror genre
update_film_genre(cursor, 'Alien', 1)  # Assuming genre ID 1 is Horror

# Display films after updating genre
show_films(cursor, "-- DISPLAYING FILMS AFTER UPDATE--")

# Delete film 'Gladiator'
delete_film(cursor, 'Gladiator')

# Display films after deletion
show_films(cursor, "-- DISPLAYING FILMS AFTER DELETE --")

# Commit changes and close connection
conn.commit()
cursor.close()
conn.close()

