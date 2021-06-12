import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import defaultdict                 # import dictionary for graph
from Dictionaries import *
from Graph import build_graph, find_edge_weight
import networkx as nx                               # to create the graph on matplotlib, kind of Node view
import plotly.express as px
import pandas as pd
import geopandas as gpd
from networkx.drawing.nx_pydot import write_dot



# PLOTTING HIST
def plot_hist(region, best_fitness, hist):
    title = "Optimizing Vaccine Distribution by Regions of Brazil"
    plt.title(title)
    plt.xlabel("Number of Generations")
    plt.ylabel("Fitness Value (minutes)")
    plt.plot(hist)

    return plt



def plot_map(graph, geo, tit):
    # GEOPANDAS
    cities_path = r'br_cities_lat_long.csv'
    df = pd.read_csv(cities_path)

    df_geo = gpd.GeoDataFrame(df, geometry= gpd.points_from_xy(df.longitude, df.latitude))

    # get built in dataset from geopandas
    brazil_data = gpd.read_file('BR_UF_2020/BR_UF_2020.shp')

    # plot Brazil's map
    axis = brazil_data.plot(color = 'lightblue', edgecolor= 'white')

    nx.draw_networkx(graph, pos=geo, node_size = 80)
    nx.draw_networkx_nodes(graph, geo, node_color='purple')
    plt.title(tit)

    plt.show()



def create_nx_graph(graph, sp, tit):
    G = nx.Graph()

    cities_path = r'br_cities_lat_long.csv'
    df = pd.read_csv(cities_path)

    # add all edges
    edges = []
    for state1, state2 in graph.items():
        for stt2, w in state2:
            G.add_edge(state1, stt2, weight=w)

    if sp:       
        # adding edges from SP to each distribution center
        edges = [("SP" , state , find_edge_weight("SP", state)) for state in distribution_center.values()]
        G.add_weighted_edges_from(edges)


    # dict of State: coordinates
    coord = list(zip(df['longitude'], df['latitude']))
    state = (df['state'])

    geo = {}
    for i in range(len(state)):
        geo[state[i]] = coord[i]
    
    plot_map(G, geo, tit)
