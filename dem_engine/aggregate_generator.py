# -*- coding: utf-8 -*-
import numpy as np

class AggregateShapeLibrary:
    def __init__(self):
        self.templates = {
            'limestone_angular': self._create_angular_template(),
            'limestone_flaky': self._create_flaky_template(),
            'limestone_blocky': self._create_blocky_template()
        }

    def _create_angular_template(self):
        return np.array([
            [0.0, 0.0, 0.0, 0.45],
            [0.3, 0.2, 0.15, 0.25],
            [-0.3, -0.15, 0.1, 0.25],
            [0.1, -0.25, -0.2, 0.25],
            [-0.15, 0.25, 0.2, 0.20]
        ])

    def _create_flaky_template(self):
        return np.array([
            [0.0, 0.0, 0.0, 0.40],
            [0.25, 0.0, 0.0, 0.30],
            [-0.25, 0.0, 0.0, 0.30],
            [0.0, 0.20, 0.0, 0.25],
            [0.0, -0.20, 0.0, 0.25]
        ])

    def _create_blocky_template(self):
        return np.array([
            [0.0, 0.0, 0.0, 0.50],
            [0.25, 0.25, 0.25, 0.30],
            [-0.25, -0.25, -0.25, 0.30],
            [0.25, -0.25, 0.0, 0.25],
            [-0.25, 0.25, 0.0, 0.25]
        ])

def sample_grain_size(sieve_sizes_mm, passing_pct, n_samples=1000, seed=42):
    np.random.seed(seed)
    cum_pct = np.array(passing_pct) / 100.0
    sizes = np.array(sieve_sizes_mm)
    r = np.random.uniform(cum_pct.min(), cum_pct.max(), size=n_samples)
    sampled_sizes = np.interp(r, np.flip(cum_pct), np.flip(sizes))
    return sampled_sizes

def generate_specimen_aggregates(trough_dims=(0.3, 0.12, 0.47), mortar_d=0.002, seed=42):
    shape_lib = AggregateShapeLibrary()
    np.random.seed(seed)
    n_coarse = 350
    n_mortar = 18000
    return {
        'num_coarse': n_coarse,
        'num_mortar': n_mortar,
        'coarse_density': 2689.0,
        'mortar_density': 2581.0,
        'mortar_diameter': mortar_d,
        'shape_templates': list(shape_lib.templates.keys())
    }
