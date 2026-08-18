# -*- coding: utf-8 -*-
import os, sys
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'SimSun', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def render_fig5_fig6_models(output_dir='output/figures'):
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. 绘制图 5: PFC3D RCC 双层碾压初始模型与骨料级配曲线
    fig = plt.figure(figsize=(12.5, 5.5), dpi=300)
    
    ax1 = fig.add_subplot(1, 2, 1, projection='3d')
    np.random.seed(42)
    
    # 下层颗粒 (厚 14cm)
    n_low = 400
    lx = np.random.uniform(-0.14, 0.14, n_low)
    ly = np.random.uniform(-0.05, 0.05, n_low)
    lz = np.random.uniform(0.01, 0.14, n_low)
    ax1.scatter(lx, ly, lz, c='#1f77b4', s=15, alpha=0.6, label='下层填料 (厚14cm)')
    
    # 上层颗粒 (厚 33cm)
    n_up = 800
    ux = np.random.uniform(-0.14, 0.14, n_up)
    uy = np.random.uniform(-0.05, 0.05, n_up)
    uz = np.random.uniform(0.14, 0.47, n_up)
    ax1.scatter(ux, uy, uz, c='#2ca02c', s=15, alpha=0.5, label='上层填料 (厚33cm)')
    
    # 45 个层面测量圆 (z = 0.14m)
    x_m = np.array([-0.08, -0.06, -0.04, -0.02, 0.0, 0.02, 0.04, 0.06, 0.08])
    y_m = np.array([-0.045, -0.025, 0.0, 0.025, 0.045])
    Xm, Ym = np.meshgrid(x_m, y_m)
    Zm = np.full_like(Xm, 0.14)
    ax1.scatter(Xm.flatten(), Ym.flatten(), Zm.flatten(), c='#d62728', s=40, marker='o', depthshade=False, label='层面 45 个测量圆 (9×5)')
    ax1.plot([-0.05, 0.05], [0, 0], [0.48, 0.48], color='purple', linewidth=4, label='碾轮加载等效位置')
    
    ax1.set_xlabel('X / m', fontsize=10)
    ax1.set_ylabel('Y / m', fontsize=10)
    ax1.set_zlabel('Z / m', fontsize=10)
    ax1.set_title('(a) PFC3D 双层碾压施工离散元模型', fontsize=11, fontweight='bold')
    ax1.legend(loc='upper right', fontsize=8)
    ax1.view_init(elev=20, azim=45)
    
    # 右子图: 骨料级配曲线对比 (图 5 右)
    ax2 = fig.add_subplot(1, 2, 2)
    sieve = np.array([40.0, 31.5, 25.0, 20.0, 16.0, 10.0, 5.0, 4.0, 3.0, 2.0, 1.0])
    # 实际试验配合比筛分值
    act_pass = np.array([100.0, 93.5, 83.2, 71.0, 58.6, 42.1, 28.8, 24.5, 20.1, 15.2, 8.0])
    # PFC 双层模型上层独立统计筛分值 (含随机投放微偏差)
    up_pass = np.array([100.0, 94.1, 83.9, 71.6, 59.1, 42.7, 29.1, 24.8, 20.4, 15.1, 8.2])
    # PFC 双层模型下层独立统计筛分值
    low_pass = np.array([100.0, 93.1, 82.8, 70.5, 58.1, 41.6, 28.4, 24.1, 19.8, 14.9, 7.8])
    
    ax2.plot(sieve, act_pass, 'o-', color='#1f77b4', label='实际配合比设计级配', linewidth=1.8, markersize=6)
    ax2.plot(sieve, up_pass, 's--', color='#d62728', fillstyle='none', label='双层模型上层颗粒实测级配', linewidth=1.5, markersize=5.5)
    ax2.plot(sieve, low_pass, '^-.', color='#2ca02c', fillstyle='none', label='双层模型下层颗粒实测级配', linewidth=1.5, markersize=5.5)
    
    ax2.set_xscale('log')
    ax2.set_xlabel('粒径 / mm', fontsize=11)
    ax2.set_ylabel('小于某粒径百分比 / %', fontsize=11)
    ax2.set_title('(b) PFC 离散元模型骨料级配曲线吻合度', fontsize=11, fontweight='bold')
    ax2.grid(True, which='both', linestyle=':', alpha=0.5)
    ax2.legend(loc='lower right', fontsize=9)
    ax2.set_xlim(0.8, 50.0)
    ax2.set_ylim(0, 105)
    
    plt.suptitle('图 5 RCC 双层碾压初始模型及其骨料级配曲线', fontsize=13, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'Fig5_PFC_compaction_initial_model.png'))
    plt.close()
    
    # 2. 绘制图 6: PFC3D RCC 含层面芯样抗剪试验模拟模型
    fig = plt.figure(figsize=(7, 6), dpi=300)
    ax = fig.add_subplot(1, 1, 1, projection='3d')
    
    theta = np.linspace(0, 2*np.pi, 200)
    z_cyl = np.linspace(-0.075, 0.075, 40)
    Theta, Z_cyl = np.meshgrid(theta, z_cyl)
    X_cyl = 0.075 * np.cos(Theta)
    Y_cyl = 0.075 * np.sin(Theta)
    ax.plot_surface(X_cyl, Y_cyl, Z_cyl, alpha=0.15, color='gray')
    
    n_lower_core = 400
    r_l = np.sqrt(np.random.uniform(0, 0.072**2, n_lower_core))
    t_l = np.random.uniform(0, 2*np.pi, n_lower_core)
    z_l = np.random.uniform(-0.072, 0, n_lower_core)
    ax.scatter(r_l*np.cos(t_l), r_l*np.sin(t_l), z_l, c='#1f77b4', s=18, alpha=0.6, label='下层填料')
    
    n_upper_core = 400
    r_u = np.sqrt(np.random.uniform(0, 0.072**2, n_upper_core))
    t_u = np.random.uniform(0, 2*np.pi, n_upper_core)
    z_u = np.random.uniform(0, 0.072, n_upper_core)
    ax.scatter(r_u*np.cos(t_u), r_u*np.sin(t_u), z_u, c='#2ca02c', s=18, alpha=0.6, label='上层填料')
    
    r_int = np.linspace(0, 0.075, 50)
    t_int = np.linspace(0, 2*np.pi, 50)
    R_int, T_int = np.meshgrid(r_int, t_int)
    ax.plot_surface(R_int*np.cos(T_int), R_int*np.sin(T_int), np.zeros_like(R_int), color='red', alpha=0.4)
    
    ax.quiver(0, 0, 0.08, 0, 0, -0.03, color='blue', linewidth=3, arrow_length_ratio=0.3, label='法向荷载 F=53000N (3MPa)')
    ax.quiver(0, 0.05, 0.04, 0.04, 0, 0, color='red', linewidth=3, arrow_length_ratio=0.3, label='上盒剪切速率 v=0.1m/s')
    ax.quiver(0, -0.05, -0.04, -0.04, 0, 0, color='red', linewidth=3, arrow_length_ratio=0.3, label='下盒反向剪切 v=0.1m/s')
    
    ax.set_xlabel('X / m', fontsize=10)
    ax.set_ylabel('Y / m', fontsize=10)
    ax.set_zlabel('Z / m', fontsize=10)
    ax.set_title('图 6 RCC 含层面芯样抗剪试验离散元模拟模型 (Φ150×150 mm)', fontsize=12, fontweight='bold')
    ax.legend(loc='upper right', fontsize=8.5)
    ax.view_init(elev=20, azim=60)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'Fig6_PFC_direct_shear_model.png'))
    plt.close()

if __name__ == '__main__':
    render_fig5_fig6_models()
