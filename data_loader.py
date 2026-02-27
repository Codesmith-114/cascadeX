import pandas as pd
import numpy as np

def load_data():
    
    rng = np.random.default_rng(42)

    n_assets = 20
    n_days   = 500
    asset_names = [f"Asset {i+1}" for i in range(n_assets)]

    base    = rng.normal(0, 1, (n_days, 1))
    returns = base + rng.normal(0, 0.5, (n_days, n_assets))

    return returns, asset_names





