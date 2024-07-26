'''
PART 1: NETWORK CENTRALITY METRICS

Using the imbd_movies dataset
- Guild a graph and perform some rudimentary graph analysis, extracting centrality metrics from it. 
- Below is some basic code scaffolding that you will need to add to. 
- Tailor this code scaffolding and its stucture to however works to answer the problem
- Make sure the code is line with the standards we're using in this class 
'''

import json
import numpy as np
import pandas as pd
import networkx as nx
from datetime import datetime

def build_graph_and_extract_metrics(file_path):
    """
    builds a graph from the IMDb movie dataset and extracts centrality metrics.

    parameters:
    file_path (str): Path to the IMDb movie dataset JSON file.

    returns:
    pd.DataFrame: DataFrame containing the centrality metrics.
    """
    # Build the graph
    g = nx.Graph()

    # prepare the DataFrame for output
    df_data = []

    # read the JSON file and build the graph
    with open(file_path, 'r') as in_file:
        for line in in_file:
            # load the movie from this line
            this_movie = json.loads(line)

            # create a node for every actor and add edges between them
            actors = this_movie.get('actors', [])
            num_actors = len(actors)
            for i in range(num_actors):
                for j in range(i + 1, num_actors):
                    left_actor_id, left_actor_name = actors[i]
                    right_actor_id, right_actor_name = actors[j]

                    # get the current weight, if it exists
                    if g.has_edge(left_actor_name, right_actor_name):
                        g[left_actor_name][right_actor_name]['weight'] += 1
                    else:
                        g.add_edge(left_actor_name, right_actor_name, weight=1)

                    # add data to the DataFrame
                    df_data.append([left_actor_name, '<->', right_actor_name])

    # convert the data to a DataFrame
    imdb_movie_df = pd.DataFrame(df_data, columns=['left_actor_name', '<->', 'right_actor_name'])

    # compute centrality metrics
    degree_centrality = nx.degree_centrality(g)
    betweenness_centrality = nx.betweenness_centrality(g)
    closeness_centrality = nx.closeness_centrality(g)

    # print the information
    print("Nodes:", len(g.nodes))

    # print the 10 most central nodes
    print("Top 10 nodes by degree centrality:")
    top_10_degree = sorted(degree_centrality.items(), key=lambda item: item[1], reverse=True)[:10]
    
    for node, centrality in top_10_degree:
        print(f"{node}: {centrality}")

    # output the final DataFrame to a CSV
    current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f'/mnt/data/network_centrality_{current_datetime}.csv'
    imdb_movie_df.to_csv(output_file, index=False)

    return imdb_movie_df

# call the function with the path to your JSON file
file_path = 'imbd_movie_data.json'  # Replace with your file path
imdb_movie_df = build_graph_and_extract_metrics(file_path)

# display the DataFrame
imdb_movie_df.head()
