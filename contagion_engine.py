import numpy as np

def propagate_shock(G, asset_names, shock_asset, shock_magnitude, decay, time_step):
    stress = dict.fromkeys(asset_names, 0.0)
    stress[shock_asset] = shock_magnitude
    for _ in range(time_step):                      
        new_stress = stress.copy()
        for node in G.nodes:
            for neighbor in G.neighbors(node):
                edge_weight = abs(G[node][neighbor]['weight'])
                new_stress[neighbor] += stress[node] * edge_weight * (1 - decay)
        for node in new_stress:
            new_stress[node] *= (1 - decay)
        stress = new_stress
    return stress


