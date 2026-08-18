# -*- coding: utf-8 -*-
import os, sys
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'SimSun', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dem_engine.embedment_analyzer import generate_embedment_evolution

def plot_fig10_embedment_curves(output_dir='output/figures'):
    os.makedirs(output_dir, exist_ok=True)
    
    p1, e1 = generate_embedment_evolution(case_id=1)
    p2, e2 = generate_embedment_evolution(case_id=2)
    p3, e3 = generate_embedment_evolution(case_id=3)
    p4, e4 = generate_embedment_evolution(case_id=4)
    
    plt.figure(figsize=(8, 5.5), dpi=300)
    plt.plot(p1, e1, 'o-', color='#1f77b4', label='工况 1 (标准工况, 终遍 2.197 mm)', linewidth=1.5, markersize=4.5)
    plt.plot(p2, e2, 's-', color='#d62728', label='工况 2 (激振力增大, 终遍 2.511 mm)', linewidth=1.5, markersize=4.5)
    plt.plot(p3, e3, '^-', color='#2ca02c', label='工况 3 (行进速度增大, 终遍 1.459 mm)', linewidth=1.5, markersize=4.5)
    plt.plot(p4, e4, 'd-', color='#ff7f0e', label='工况 4 (碾压厚度增大, 终遍 1.354 mm)', linewidth=1.5, markersize=4.5)
    
    plt.axvline(x=3.0, color='gray', linestyle='--', alpha=0.5)
    plt.axvline(x=16.0, color='gray', linestyle='--', alpha=0.5)
    plt.text(1.5, 2.75, '第1阶段', fontsize=10, color='gray', ha='center')
    plt.text(9.5, 2.75, '第2阶段', fontsize=10, color='gray', ha='center')
    plt.text(18.0, 2.75, '第3阶段', fontsize=10, color='gray', ha='center')
    
    plt.xlabel('碾压遍数', fontsize=12)
    plt.ylabel('嵌入值 / mm', fontsize=12)
    plt.title('图 10 不同工况下层间骨料嵌入值随碾压遍数的变化曲线', fontsize=13, fontweight='bold')
    plt.xlim(0, 20)
    plt.ylim(0, 3.0)
    plt.grid(True, linestyle=':', alpha=0.5)
    plt.legend(loc='lower right', frameon=True, fontsize=9.5)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'Fig10_embedment_curves_four_cases.png'))
    plt.close()

if __name__ == '__main__':
    plot_fig10_embedment_curves()
