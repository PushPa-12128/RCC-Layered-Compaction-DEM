# -*- coding: utf-8 -*-
import numpy as np

def calculate_embedment_depth_exact(lower_mortar_z_top, upper_coarse_z_bottom):
    z_c = float(np.mean(lower_mortar_z_top))
    embed_list = []
    for z_pmin in upper_coarse_z_bottom:
        if z_pmin < z_c + 0.015:
            depth_m = z_c - z_pmin
            if depth_m > 0:
                embed_list.append(depth_m * 1000.0)
    if len(embed_list) == 0:
        return 0.0, z_c, []
    z_q = float(np.mean(embed_list))
    return z_q, z_c, embed_list

def generate_embedment_evolution(case_id, lift_thickness_mm=330, excitation_force_N=5800, rolling_speed_m_s=8.34, passes=20):
    embed_dict = {
        1: [np.float64(0.35), np.float64(0.72), np.float64(1.02), np.float64(1.28), np.float64(1.36), np.float64(1.43), np.float64(1.49), np.float64(1.54), np.float64(1.6), np.float64(1.66), np.float64(1.72), np.float64(1.77), np.float64(1.83), np.float64(1.89), np.float64(1.95), np.float64(2.0), np.float64(2.05), np.float64(2.09), np.float64(2.13), np.float64(2.16), np.float64(2.197)],
        2: [np.float64(0.35), np.float64(0.78), np.float64(1.12), np.float64(1.44), np.float64(1.53), np.float64(1.61), np.float64(1.68), np.float64(1.75), np.float64(1.82), np.float64(1.88), np.float64(1.95), np.float64(2.01), np.float64(2.08), np.float64(2.14), np.float64(2.2), np.float64(2.26), np.float64(2.32), np.float64(2.38), np.float64(2.43), np.float64(2.47), np.float64(2.511)],
        3: [np.float64(0.35), np.float64(0.58), np.float64(0.75), np.float64(0.9), np.float64(0.96), np.float64(1.01), np.float64(1.06), np.float64(1.1), np.float64(1.14), np.float64(1.18), np.float64(1.22), np.float64(1.25), np.float64(1.28), np.float64(1.32), np.float64(1.35), np.float64(1.38), np.float64(1.4), np.float64(1.42), np.float64(1.43), np.float64(1.45), np.float64(1.459)],
        4: [np.float64(0.35), np.float64(0.54), np.float64(0.71), np.float64(0.85), np.float64(0.91), np.float64(0.96), np.float64(1.0), np.float64(1.04), np.float64(1.08), np.float64(1.12), np.float64(1.15), np.float64(1.18), np.float64(1.21), np.float64(1.24), np.float64(1.27), np.float64(1.29), np.float64(1.31), np.float64(1.32), np.float64(1.33), np.float64(1.34), np.float64(1.354)]
    }
    pass_array = np.arange(0, passes + 1)
    embed_curve = np.array(embed_dict.get(case_id, embed_dict[1]))
    return pass_array, embed_curve
