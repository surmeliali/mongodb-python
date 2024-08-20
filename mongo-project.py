from modules import db, movies, json_util # include csv_util if you have csv files.
# Read the config
config = db.getConfig()
# Connect to the database
conn = db.connect(config)


# List the movies, in the database
# movies.listMovies(conn)

# read the CSV file if there is
# csvContent = csv_util.readCSVFile(config)

# List the movies in the csv file
# csv_util.showCSVFile(csvContent)

json_data = json_util.readJSONFile(config)
# json_util.showJsonFile(json_data)


# Insert the movies into the database
movies.insert_movies(conn, json_data)


# Run the advanced queries
movies.advanced_queries(conn)
