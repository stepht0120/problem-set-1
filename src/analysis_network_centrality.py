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

# Build the graph
g = nx.Graph()

# Set up your dataframe(s) -> the df that's output to a CSV should include at least the columns 'left_actor_name', '<->', 'right_actor_name'
df_data = []

with open() as in_file:
    # Don't forget to comment your code
    for line in in_file:
        # Don't forget to include docstrings for all functions

        # Load the movie from this line
        this_movie = json.loads(line)
            
        # Create a node for every actor
        actors = this_movie.get('actors', [])
        num_actors = len(actors)

        for i in range(num_actors):
            for j in range(i + 1, num_actors):
                left_actor_id, left_actor_name = actors[i]
                right_actor_id, right_actor_name = actors[j]

                # Get the current weight, if it exists
                if g.has_edge(left_actor_name, right_actor_name):
                    g[left_actor_name][right_actor_name]['weight'] += 1
                else:
                    g.add_edge(left_actor_name, right_actor_name, weight=1)

                # Add data to the DataFrame
                df_data.append([left_actor_name, '<->', right_actor_name])

        # add the actor to the graph    
        # Iterate through the list of actors, generating all pairs
        ## Starting with the first actor in the list, generate pairs with all subsequent actors
        ## then continue to second actor in the list and repeat
        
imdb_movie_df = pd.DataFrame(df_data, columns=['left_actor_name', '<->', 'right_actor_name'])

# Print the info below
print("Nodes:", len(g.nodes))

#Print the 10 the most central nodes
print("Top 10 nodes by degree centrality:")
top_10_degree = sorted(degree_centrality.items(), key=lambda item: item[1], reverse=True)[:10]
for node, centrality in top_10_degree:
    print(f"{node}: {centrality}")

# Output the final dataframe to a CSV named 'network_centrality_{current_datetime}.csv' to `/data`
current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
output_file = f'/mnt/data/network_centrality_{current_datetime}.csv'
imdb_movie_df.to_csv(output_file, index=False)

