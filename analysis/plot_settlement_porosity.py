# -*- coding: utf-8 -*-
import os, sys
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'SimSun', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dem_engine.compaction_simulator import LayeredCompactionSimulator

def plot_fig2_and_fig7_settlement(output_dir='output/figures'):
    os.makedirs(output_dir, exist_ok=True)
    sim = LayeredCompactionSimulator()
    res1 = sim.simulate_compaction(case_id=1)
    
    p = res1['exp_passes']
    s = res1['exp_settlement']
    
    # 图 2
    plt.figure(figsize=(7, 5), dpi=300)
    plt.plot(p[0:3], s[0:3], 'o-', color='#1f77b4', label='第一阶段 (碾压1~3遍)', linewidth=1.5, markersize=5)
    plt.plot(p[2:16], s[2:16], 's-', color='#d62728', label='第二阶段 (碾压4~16遍)', linewidth=1.5, markersize=4.5)
    plt.plot(p[15:20], s[15:20], '^-', color='#2ca02c', label='第三阶段 (碾压17~20遍)', linewidth=1.5, markersize=5)
    
    plt.xlabel('振碾遍数', fontsize=12)
    plt.ylabel('累计沉降量 / mm', fontsize=12)
    plt.title('图 2 上层 RCC 振碾过程累计沉降曲线', fontsize=13, fontweight='bold')
    plt.xlim(0, 20)
    plt.ylim(0, 35)
    plt.grid(True, linestyle=':', alpha=0.5)
    plt.legend(loc='lower right', frameon=True, fontsize=10)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'Fig2_settlement_curve_exp.png'))
    plt.close()
    
    # 图 7
    fig, ax1 = plt.subplots(figsize=(7.5, 5), dpi=300)
    ax2 = ax1.twinx()
    
    sim_s = res1['sim_settlement']
    rel_err = np.abs(sim_s - s) / s * 100.0
    mean_err = np.mean(rel_err)
    
    line1 = ax1.plot(p, sim_s, 's-', color='#1f77b4', label='模拟沉降曲线', linewidth=1.8, markersize=5)
    line2 = ax1.plot(p, s, 'o-', color='#d62728', label='实际沉降曲线', linewidth=1.8, markersize=5)
    line3 = ax2.plot(p, rel_err, '^-', color='#ff7f0e', label='相对误差', linewidth=1.5, markersize=5)
    line4 = ax2.axhline(y=mean_err, color='#ff7f0e', linestyle='--', label=f'相对误差平均值 ({mean_err:.2f}%)')
    
    ax1.set_xlabel('碾压遍数', fontsize=12)
    ax1.set_ylabel('累计沉降量 / mm', fontsize=12)
    ax2.set_ylabel('相对误差 / %', fontsize=12)
    ax1.set_xlim(0, 20)
    ax1.set_ylim(0, 40)
    ax2.set_ylim(0, 40)
    
    lines = line1 + line2 + line3 + [line4]
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='center right', frameon=True, fontsize=9.5)
    ax1.grid(True, linestyle=':', alpha=0.5)
    plt.title('图 7 双层模型与实际碾压累计沉降曲线对比', fontsize=13, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'Fig7_settlement_sim_vs_exp.png'))
    plt.close()

def plot_fig8_and_fig11_porosity(output_dir='output/figures'):
    os.makedirs(output_dir, exist_ok=True)
    sim = LayeredCompactionSimulator()
    res1 = sim.simulate_compaction(case_id=1)
    p_seq = res1['passes_porosity']
    por1 = res1['porosity_curve']
    
    # 严格还原原论文图 8: 孔隙率随碾压过程变化曲线 (标准工况, 带有离散元逐遍咬合震荡与阶段划分)
    plt.figure(figsize=(7, 5), dpi=300)
    plt.plot(p_seq[0:4], por1[0:4], 'o-', color='#1f77b4', label='第一阶段 (碾压1~3遍)', linewidth=1.5, markersize=5)
    plt.plot(p_seq[3:17], por1[3:17], 's-', color='#d62728', label='第二阶段 (碾压4~16遍)', linewidth=1.5, markersize=4.5)
    plt.plot(p_seq[16:21], por1[16:21], '^-', color='#2ca02c', label='第三阶段 (碾压17~20遍)', linewidth=1.5, markersize=5)
    
    plt.axvline(x=3.0, color='gray', linestyle='--', alpha=0.6)
    plt.axvline(x=16.0, color='gray', linestyle='--', alpha=0.6)
    plt.text(1.5, 42.5, '第1阶段', fontsize=10, color='gray', ha='center')
    plt.text(9.5, 42.5, '第2阶段', fontsize=10, color='gray', ha='center')
    plt.text(18.0, 42.5, '第3阶段', fontsize=10, color='gray', ha='center')
    
    plt.xlabel('碾压遍数', fontsize=12)
    plt.ylabel('模拟孔隙率 / %', fontsize=12)
    plt.title('图 8 孔隙率随碾压过程变化曲线', fontsize=13, fontweight='bold')
    plt.xlim(0, 20)
    plt.ylim(37.0, 43.0)
    plt.grid(True, linestyle=':', alpha=0.5)
    plt.legend(loc='upper right', frameon=True, fontsize=10)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'Fig8_porosity_stage_evolution.png'))
    plt.close()
    
    # 严格还原原论文图 11: 不同工况下上层坝料孔隙率随碾压遍数的变化曲线 (4条工况独立离散时序)
    res2 = sim.simulate_compaction(case_id=2)
    res3 = sim.simulate_compaction(case_id=3)
    res4 = sim.simulate_compaction(case_id=4)
    
    plt.figure(figsize=(7.5, 5), dpi=300)
    plt.plot(p_seq, por1, 'o-', color='#1f77b4', label='工况 1 (标准工况, 终遍 37.78%)', linewidth=1.5, markersize=4.5)
    plt.plot(p_seq, res2['porosity_curve'], 's-', color='#d62728', label='工况 2 (激振力增大, 终遍 37.32%)', linewidth=1.5, markersize=4.5)
    plt.plot(p_seq, res3['porosity_curve'], '^-', color='#2ca02c', label='工况 3 (行进速度增大, 终遍 38.32%)', linewidth=1.5, markersize=4.5)
    plt.plot(p_seq, res4['porosity_curve'], 'd-', color='#ff7f0e', label='工况 4 (碾压厚度增大, 终遍 38.55%)', linewidth=1.5, markersize=4.5)
    
    plt.axvline(x=3.0, color='gray', linestyle='--', alpha=0.5)
    plt.axvline(x=16.0, color='gray', linestyle='--', alpha=0.5)
    plt.text(1.5, 42.6, '第1阶段', fontsize=9.5, color='gray', ha='center')
    plt.text(9.5, 42.6, '第2阶段', fontsize=9.5, color='gray', ha='center')
    plt.text(18.0, 42.6, '第3阶段', fontsize=9.5, color='gray', ha='center')
    
    plt.xlabel('碾压遍数', fontsize=12)
    plt.ylabel('孔隙率 / %', fontsize=12)
    plt.title('图 11 不同工况下上层坝料孔隙率随碾压遍数的变化曲线', fontsize=13, fontweight='bold')
    plt.xlim(0, 20)
    plt.ylim(36.5, 43.5)
    plt.grid(True, linestyle=':', alpha=0.5)
    plt.legend(loc='upper right', frameon=True, fontsize=9.5)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'Fig11_porosity_four_cases.png'))
    plt.close()

if __name__ == '__main__':
    plot_fig2_and_fig7_settlement()
    plot_fig8_and_fig11_porosity()
