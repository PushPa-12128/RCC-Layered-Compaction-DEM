# -*- coding: utf-8 -*-
import numpy as np

def calculate_compaction_energy(A, W, F, N, f, B, H, v):
    work_per_cycle = 2.0 * A * W + (np.pi * F / 4.0)
    total_cycles = N * f
    swept_volume_rate = B * H * v
    E_0 = work_per_cycle * total_cycles / swept_volume_rate
    return E_0

def verify_scaling_rules(real_params, model_params):
    E0_R = calculate_compaction_energy(
        A=real_params['A'], W=real_params['W'], F=real_params['F'],
        N=1, f=real_params['f'], B=real_params['B'], H=real_params['H'], v=real_params['v']
    )
    E0_S = calculate_compaction_energy(
        A=model_params['A'], W=model_params['W'], F=model_params['F'],
        N=1, f=model_params['f'], B=model_params['B'], H=model_params['H'], v=model_params['v']
    )
    ratio_R = real_params['F'] / real_params['W']
    ratio_S = model_params['F'] / model_params['W']
    return {
        'E0_Real_J_m3': float(E0_R),
        'E0_Model_J_m3': float(E0_S),
        'E0_Relative_Error_Pct': float(abs(E0_S - E0_R) / E0_R * 100.0),
        'Dynamic_Static_Ratio_Real': float(ratio_R),
        'Dynamic_Static_Ratio_Model': float(ratio_S),
        'Ratio_Relative_Error_Pct': float(abs(ratio_S - ratio_R) / ratio_R * 100.0)
    }

if __name__ == '__main__':
    real_p = {'A': 0.7e-3, 'W': 27.5e3, 'F': 58.0e3, 'f': 42.0, 'B': 1.0, 'H': 0.33, 'v': 1.5 / 3.6}
    model_p = {'A': 0.7e-3, 'W': 2.75e3, 'F': 5.8e3, 'f': 42.0, 'B': 0.1, 'H': 0.33, 'v': 1.5 / 3.6}
    res = verify_scaling_rules(real_p, model_p)
    print('--> 碾轮尺度缩放与等效荷载验证结果:')
    for k, v in res.items():
        print(f'    {k}: {v:.4f}')
