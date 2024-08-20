from datetime import datetime

def parse_release_date(date_string):
    if not date_string:
        return None
    try:
        return datetime.strptime(date_string, "Released %b %d, %Y")
    except ValueError:
        try:
            return datetime.strptime(date_string, "%Y")
        except ValueError:
            return None

def parse_score(score_string):
    if score_string and score_string.endswith('%'):
        return int(score_string[:-1])
    return None

def insert_movies(db, movies_data):
    collection = db['etl-movies']
    # Drop the existing collection
    collection.drop()
    print(f"Inserting {len(movies_data)} movies into the database.")
    for movie in movies_data:
        movie['release_date'] = parse_release_date(movie.get('release_date'))
        movie['critic_score'] = parse_score(movie.get('critic_score'))
        movie['audience_score'] = parse_score(movie.get('audience_score'))
        collection.insert_one(movie)
    print(f"Inserted {len(movies_data)} movies into the database.")

def advanced_queries(db):
    collection = db['etl-movies']

    print("\nRunning advanced queries...")

    # Query 1: Top 5 movies by critic score
    print("\nTop 5 movies by critic score:")
    top_movies = list(collection.aggregate([
        {"$match": {"critic_score": {"$ne": None}}},
        {"$sort": {"critic_score": -1}},
        {"$limit": 5},
        {"$project": {"_id": 0, "title": 1, "critic_score": 1}}
    ]))
    if top_movies:
        for movie in top_movies:
            print(f"{movie['title']}: {movie['critic_score']}%")
    else:
        print("No movies found with critic scores.")

    # Query 2: Average audience score by decade
    print("\nAverage audience score by decade:")
    decade_scores = list(collection.aggregate([
        {"$match": {"audience_score": {"$ne": None}, "release_date": {"$ne": None}}},
        {"$project": {
            "decade": {"$subtract": [{"$year": "$release_date"}, {"$mod": [{"$year": "$release_date"}, 10]}]},
            "audience_score": 1
        }},
        {"$group": {
            "_id": "$decade",
            "avg_score": {"$avg": "$audience_score"}
        }},
        {"$sort": {"_id": 1}}
    ]))
    if decade_scores:
        for decade in decade_scores:
            print(f"{decade['_id']}s: {decade['avg_score']:.2f}%")
    else:
        print("No data available for audience scores by decade.")

    # Query 3: Movies with missing critic or audience scores
    print("\nMovies with missing scores:")
    missing_scores = list(collection.aggregate([
        {"$match": {"$or": [{"critic_score": None}, {"audience_score": None}]}},
        {"$project": {"_id": 0, "title": 1, "critic_score": 1, "audience_score": 1}}
    ]))
    if missing_scores:
        for movie in missing_scores[:10]:  # Limit to first 10 for brevity
            critic = f"{movie['critic_score']}%" if movie['critic_score'] is not None else "N/A"
            audience = f"{movie['audience_score']}%" if movie['audience_score'] is not None else "N/A"
            print(f"{movie['title']} - Critic: {critic}, Audience: {audience}")
        print(f"... and {len(missing_scores) - 10} more movies with missing scores.")
    else:
        print("No movies found with missing scores.")

    # Query 4: Correlation between critic and audience scores
    print("\nCorrelation between critic and audience scores:")
    correlation = list(collection.aggregate([
        {"$match": {"critic_score": {"$ne": None}, "audience_score": {"$ne": None}}},
        {"$group": {
            "_id": None,
            "critic_avg": {"$avg": "$critic_score"},
            "audience_avg": {"$avg": "$audience_score"},
            "critic_std": {"$stdDevPop": "$critic_score"},
            "audience_std": {"$stdDevPop": "$audience_score"},
            "covariance": {
                "$avg": {
                    "$multiply": [
                        {"$subtract": ["$critic_score", {"$avg": "$critic_score"}]},
                        {"$subtract": ["$audience_score", {"$avg": "$audience_score"}]}
                    ]
                }
            }
        }},
        {"$project": {
            "correlation": {
                "$divide": [
                    "$covariance",
                    {"$multiply": ["$critic_std", "$audience_std"]}
                ]
            }
        }}
    ]))
    if correlation:
        print(f"Correlation coefficient: {correlation[0]['correlation']:.2f}")
    else:
        print("Not enough data to calculate correlation.")

    # Additional query to show database stats
    print("\nDatabase stats:")
    stats = collection.count_documents({})
    print(f"Total number of documents: {stats}")
    print(f"Documents with critic scores: {collection.count_documents({'critic_score': {'$ne': None}})}")
    print(f"Documents with audience scores: {collection.count_documents({'audience_score': {'$ne': None}})}")
    print(f"Documents with release dates: {collection.count_documents({'release_date': {'$ne': None}})}")