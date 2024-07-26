'''
PART 2: SIMILAR ACTROS BY GENRE
Using the imbd_movies dataset:
- Create a data frame, where each row corresponds to an actor, each column represents a genre, and each cell captures how many times that row's actor has appeared in that column’s genre 
- Using this data frame as your “feature matrix”, select an actor (called your “query”) for whom you want to find the top 10 most similar actors based on the genres in which they’ve starred 
- - As an example, select the row from your data frame associated with Chris Hemsworth, actor ID “nm1165110”, as your “query” actor
- Use sklearn.metrics.DistanceMetric to calculate the euclidean distances between your query actor and all other actors based on their genre appearances
- - https://scikit-learn.org/stable/modules/generated/sklearn.metrics.DistanceMetric.html
- Output a CSV continaing the top ten actors most similar to your query actor using cosine distance 
- - Name it 'similar_actors_genre_{current_datetime}.csv' to `/data`
- - For example, the top 10 for Chris Hemsworth are:  
        nm1165110 Chris Hemsworth
        nm0000129 Tom Cruise
        nm0147147 Henry Cavill
        nm0829032 Ray Stevenson
        nm5899377 Tiger Shroff
        nm1679372 Sudeep
        nm0003244 Jordi Mollà
        nm0636280 Richard Norton
        nm0607884 Mark Mortimer
        nm2018237 Taylor Kitsch
- Describe in a print() statement how this list changes based on Euclidean distance
- Make sure your code is in line with the standards we're using in this class
'''

#Write your code below
import json
import pandas as pd
from sklearn.metrics import DistanceMetric
from sklearn.metrics.pairwise import cosine_distances
from datetime import datetime

def build_genre_feature_matrix(file_path):
    """
    builds a feature matrix where rows correspond to actors and columns represent genres.

    parameters:
    file_path (str): Path to the IMDb movie dataset JSON file.

    returns:
    pd.DataFrame: feature matrix of actors and their genre appearances.
    """
    # read the JSON file and extract actors and genres
    actors_genres = {}

    with open(file_path, 'r') as in_file:
        for line in in_file:
            this_movie = json.loads(line)
            genres = this_movie.get('genres', [])
            actors = this_movie.get('actors', [])

            for actor_id, actor_name in actors:
                if actor_id not in actors_genres:
                    actors_genres[actor_id] = {'actor_name': actor_name}
                
                for genre in genres:
                    if genre not in actors_genres[actor_id]:
                        actors_genres[actor_id][genre] = 0
                    actors_genres[actor_id][genre] += 1

    # convert to DataFrame
    genre_feature_matrix = pd.DataFrame.from_dict(actors_genres, orient='index').fillna(0)

    return genre_feature_matrix

def find_similar_actors(genre_feature_matrix, query_actor_id, query_actor_name):
    """
    finds the top 10 actors most similar to the query actor based on genre appearances.

    parameters:
    genre_feature_matrix (pd.DataFrame): Feature matrix of actors and their genre appearances.
    query_actor_id (str): Actor ID of the query actor.
    query_actor_name (str): Actor name of the query actor.

    returns:
    pd.DataFrame: DataFrame of the top 10 similar actors.
    """
    # select the query actor's row
    query_actor_row = genre_feature_matrix.loc[query_actor_id].values.reshape(1, -1)

    # calculate cosine distances
    distances = cosine_distances(query_actor_row, genre_feature_matrix.values).flatten()

    # create a DataFrame for distances
    distances_df = pd.DataFrame({
        'actor_id': genre_feature_matrix.index,
        'actor_name': genre_feature_matrix['actor_name'],
        'distance': distances
    }).set_index('actor_id')

    # sort by distance and select top 10
    top_10_similar_actors = distances_df.nsmallest(11, 'distance').iloc[1:11]

    return top_10_similar_actors

# build the genre feature matrix
file_path = 'imbd_movie_data.json'
genre_feature_matrix = build_genre_feature_matrix(file_path)

# find similar actors to Chris Hemsworth
query_actor_id = 'nm1165110'  # Chris Hemsworth's actor ID
query_actor_name = 'Chris Hemsworth'
top_10_similar_actors = find_similar_actors(genre_feature_matrix, query_actor_id, query_actor_name)

# print the top 10 similar actors
print(top_10_similar_actors)

# output the top 10 similar actors to a CSV
current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
output_file = f'/mnt/data/similar_actors_genre_{current_datetime}.csv'
top_10_similar_actors.to_csv(output_file, index=False)

print(f"Top 10 similar actors based on cosine distance saved to {output_file}")
