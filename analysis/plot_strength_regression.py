# -*- coding: utf-8 -*-
"""
复现图15、图16与表7 (骨料嵌入值-抗剪强度线性回归方程与参数敏感性分析)
"""
import os, sys, csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'SimSun', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def plot_fig15_and_table7_regression(output_dir='output/figures', table_dir='output/tables'):
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(table_dir, exist_ok=True)
    
    # 论文表 7 完整数据
    cases = np.array([1, 2, 3, 4, 5, 6, 7])
    z_q = np.array([2.197, 2.511, 1.459, 1.354, 1.000, 1.710, 2.009])
    disp_p = np.array([2.667, 2.684, 2.490, 2.379, 1.941, 2.605, 2.589])
    load_p = np.array([105.615, 113.950, 86.500, 83.926, 70.373, 91.052, 100.996])
    tau_p = np.array([5.977, 6.448, 4.895, 4.749, 3.982, 5.152, 5.715])
    
    # 线性回归: tau_u = slope * z_q + intercept
    slope, intercept, r_value, p_value, std_err = linregress(z_q, tau_p)
    r2 = r_value ** 2
    
    with open(os.path.join(table_dir, 'Table7_DirectShear_Results.csv'), 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(['工况序号', '层间骨料嵌入值/mm', '峰值位移/mm', '峰值剪切荷载/kN', '峰值应力/MPa'])
        for i in range(len(cases)):
            writer.writerow([cases[i], f'{z_q[i]:.3f}', f'{disp_p[i]:.3f}', f'{load_p[i]:.3f}', f'{tau_p[i]:.3f}'])
            
    # 图 15: 层间骨料嵌入值与模拟抗剪强度关系
    plt.figure(figsize=(7, 5), dpi=300)
    plt.scatter(z_q, tau_p, color='#d62728', s=60, zorder=5, label='离散元模拟数据点')
    
    z_fit = np.linspace(0.5, 3.0, 100)
    tau_fit = slope * z_fit + intercept
    formula_label = f'$\\tau_u = {slope:.3f}\\bar{{z}}_q + {intercept:.3f}$\n$R^2 = {r2:.3f}$'
    plt.plot(z_fit, tau_fit, '-', color='#1f77b4', linewidth=2.0, label=f'线性拟合: {formula_label}')
    
    plt.xlabel('平均嵌入值 / mm', fontsize=12)
    plt.ylabel('模拟抗剪强度 / MPa', fontsize=12)
    plt.title('图 15 层间骨料嵌入值与模拟抗剪强度关系', fontsize=13, fontweight='bold')
    plt.xlim(0.5, 3.0)
    plt.ylim(3.0, 7.5)
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend(loc='lower right', frameon=True, fontsize=11)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'Fig15_embedment_vs_shear_strength.png'))
    plt.close()

def plot_fig16_sensitivity_analysis(output_dir='output/figures'):
    os.makedirs(output_dir, exist_ok=True)
    
    fig, ax1 = plt.subplots(figsize=(8, 5.5), dpi=300)
    ax2 = ax1.twinx()
    
    # 嵌入值曲线 (左轴)
    l1 = ax1.plot([1.0, 1.5], [2.197, 2.511], 's-', color='#d62728', label='激振力与嵌入值', linewidth=1.8, markersize=6)
    l2 = ax1.plot([1.0, 1.5], [2.197, 1.459], 'o-', color='#1f77b4', label='行进速度与嵌入值', linewidth=1.8, markersize=6)
    l3 = ax1.plot([1.0, 1.212], [2.197, 1.354], '^-', color='#2ca02c', label='碾压厚度与嵌入值', linewidth=1.8, markersize=6)
    
    # 抗剪强度曲线 (右轴)
    l4 = ax2.plot([1.0, 1.5], [5.977, 6.448], 's--', color='#d62728', alpha=0.7, label='激振力与抗剪强度', linewidth=1.8, markersize=6)
    l5 = ax2.plot([1.0, 1.5], [5.977, 4.895], 'o--', color='#1f77b4', alpha=0.7, label='行进速度与抗剪强度', linewidth=1.8, markersize=6)
    l6 = ax2.plot([1.0, 1.212], [5.977, 4.749], '^--', color='#2ca02c', alpha=0.7, label='碾压厚度与抗剪强度', linewidth=1.8, markersize=6)
    
    ax1.set_xlabel('参数变化幅度 λ', fontsize=12)
    ax1.set_ylabel('嵌入值 / mm', fontsize=12)
    ax2.set_ylabel('模拟抗剪强度 / MPa', fontsize=12)
    
    ax1.set_xlim(0.8, 1.8)
    ax1.set_ylim(0.5, 3.5)
    ax2.set_ylim(4.0, 7.5)
    
    lines = l1 + l2 + l3 + l4 + l5 + l6
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper right', frameon=True, fontsize=9, ncol=2)
    
    plt.title('图 16 碾压参数对嵌入值和层间结合质量的影响程度分析', fontsize=13, fontweight='bold')
    ax1.grid(True, linestyle=':', alpha=0.6)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'Fig16_sensitivity_analysis.png'))
    plt.close()

if __name__ == '__main__':
    plot_fig15_and_table7_regression()
    plot_fig16_sensitivity_analysis()
    print('Strength regression & Sensitivity figures generated.')
