'''
Pull down the imbd_movies dataset here and save to /data as imdb_movies_2000to2022.prolific.json
You will run this project from main.py, so need to set things up accordingly
'''

import json
import analysis_network_centrality
import analysis_similar_actors_genre

def main():
    # download and save the IMDb movies dataset
    import urllib.request
    url = "https://github.com/cbuntain/umd.inst414/blob/main/data/imdb_movies_2000to2022.prolific.json?raw=true"
    save_path = '/mnt/data/imdb_movies_2000to2022.prolific.json'
    urllib.request.urlretrieve(url, save_path)

    # call functions from the analysis scripts
    analysis_network_centrality.build_graph_and_extract_metrics(save_path)
    query_actor_id = 'nm1165110'  # Chris Hemsworth's actor ID
    query_actor_name = 'Chris Hemsworth'
    analysis_similar_actors_genre.save_similar_actors(save_path, query_actor_id, query_actor_name)

if __name__ == "__main__":
    main()
