import networkx as nx

def compute_metrics(G, stress_levels):
    density = nx.density(G)
    centrality = nx.degree_centrality(G)
    ranking = sorted(stress_levels.item(), key=lambda x:x[1], reverse=True)
    return {
        'Network Density' : density,
        'Centrality' : centrality,
        'Systemic importance ranking' : ranking 
    }