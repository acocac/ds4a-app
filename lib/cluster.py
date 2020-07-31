import pandas as pd
from sqlalchemy import create_engine
from scipy.spatial.distance import pdist, jaccard
from scipy.spatial.distance import squareform
import networkx as nx
import numpy as np
import plotly.graph_objects as go
from decouple import config


def get_network_data():
    engine = create_engine(config('DATABASE_URL'))
    sim_df = pd.read_sql('select interno, delito, fecha_ingreso from reincidentes', engine)

    col_list = ['interno', 'delito_x', 'delito_y', 'fecha_ingreso_x', 'fecha_ingreso_y']
    df_merge = sim_df.merge(sim_df, on='interno')[col_list]
    df_merge = df_merge[df_merge['fecha_ingreso_x'] < df_merge['fecha_ingreso_y']][col_list].drop_duplicates()

    df_merge_x = df_merge[['interno', 'delito_x', 'fecha_ingreso_x']]
    df_merge_y = df_merge[['interno', 'delito_y', 'fecha_ingreso_y']]
    df_merge_x.columns, df_merge_y.columns = ['interno', 'delito', 'fecha_ingreso'], ['interno', 'delito',
                                                                                      'fecha_ingreso']

    df_to_incidence = pd.concat([df_merge_x, df_merge_y]).drop_duplicates()

    incidence_df = pd.crosstab(df_to_incidence['delito'], df_to_incidence['interno'])
    res = pdist(incidence_df, 'cosine')
    distance = pd.DataFrame(squareform(res), index=incidence_df.index, columns=incidence_df.index)
    distance.values[[np.arange(distance.shape[0])] * 2] = 0
    distance.index = distance.index.rename('delito_1')
    distance.columns = distance.columns.rename('delito_2')

    return distance


def make_blue(alpha):
    invalpha = 1 - alpha
    scaled = int(255 * invalpha)
    return (scaled, scaled, 255)


def network_plot(cluster, complete_graph):
    isolates = list(nx.isolates(complete_graph))
    complete_graph.remove_nodes_from(isolates)
    msp_graph = nx.algorithms.tree.mst.minimum_spanning_tree(complete_graph, weight='weight')
    greedy_communities = nx.algorithms.community.modularity_max.greedy_modularity_communities(msp_graph,
                                                                                              weight='weight')

    community = greedy_communities[cluster]
    subgraph_gc = msp_graph.subgraph(community)

    pos = nx.spring_layout(subgraph_gc, weight='weight')

    G = subgraph_gc
    for n in pos:
        G.nodes[n]['pos'] = pos[n]

    weights = list()
    blue_scale = list()
    for i in subgraph_gc.edges:
        weights.append(1 - subgraph_gc.edges[i]['weight'])

    for j in weights:
        vals = make_blue((j - min(weights)) / (max(weights) - min(weights)))
        blue_scale.append('rgb{}'.format(vals))

    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = G.nodes[edge[0]]['pos']
        x1, y1 = G.nodes[edge[1]]['pos']
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    edges_list = [go.Scatter(x=[pos[e[0]][0], pos[e[1]][0]],
                             y=[pos[e[0]][1], pos[e[1]][1]],
                             mode='lines',
                             line=dict(width=2, color=blue_scale[k])) for k, e in enumerate(subgraph_gc.edges)]

    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = G.nodes[node]['pos']
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=15,
            line_width=2))

    node_trace.text = list(pos.keys())
    traces = edges_list + [node_trace]

    layout = go.Layout(
        # title='<br>Redes de Reincidencia',
        # titlefont_size=16,
        # template='plotly_white',
        paper_bgcolor="#2c2f38",
        plot_bgcolor='#2c2f38',
        showlegend=False,
        hovermode='closest',
        margin=dict(b=20, l=5, r=5, t=40),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))

    return dict(data=traces, layout=layout)

distance = get_network_data()
complete_graph = nx.from_pandas_adjacency(distance)

def get_nplot(cluster):
    fig = go.Figure(network_plot(cluster, complete_graph))
    return fig