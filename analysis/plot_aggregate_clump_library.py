# -*- coding: utf-8 -*-
"""
复现图 4: 骨料形状库的建立 (石灰岩三维激光扫描点云 -> 多球 Clump 颗粒填充与形态分类)
涵盖: 粗骨料实物、三维扫描点云、不规则多球填充(扁平状、棱角状、块状次棱角)
"""
import os, sys
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'SimSun', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def render_fig4_aggregate_library(output_dir='output/figures'):
    os.makedirs(output_dir, exist_ok=True)
    
    fig = plt.figure(figsize=(13, 4.5), dpi=300)
    
    # 子图 1: 粗骨料扫描点云示意
    ax1 = fig.add_subplot(1, 3, 1, projection='3d')
    np.random.seed(10)
    # 生成不规则凸多面体表面点云
    u = np.linspace(0, 2 * np.pi, 30)
    v = np.linspace(0, np.pi, 20)
    U, V = np.meshgrid(u, v)
    r_base = 10.0 + 2.5 * np.sin(3*U) * np.cos(2*V) + np.random.normal(0, 0.4, U.shape)
    X_scan = r_base * np.sin(V) * np.cos(U)
    Y_scan = r_base * np.sin(V) * np.sin(U) * 0.8
    Z_scan = r_base * np.cos(V) * 0.65
    
    ax1.scatter(X_scan, Y_scan, Z_scan, c='#d62728', s=12, alpha=0.8)
    ax1.set_title('(a) HandyScan 3D 激光扫描骨料点云', fontsize=11, fontweight='bold')
    ax1.set_xlabel('X / mm', fontsize=9)
    ax1.set_ylabel('Y / mm', fontsize=9)
    ax1.set_zlabel('Z / mm', fontsize=9)
    ax1.view_init(elev=25, azim=45)
    
    # 子图 2: 三维点云重构与网格包络
    ax2 = fig.add_subplot(1, 3, 2, projection='3d')
    ax2.plot_wireframe(X_scan, Y_scan, Z_scan, color='#1f77b4', linewidth=0.6, alpha=0.7)
    ax2.set_title('(b) 骨料外轮廓三维几何网格重构', fontsize=11, fontweight='bold')
    ax2.set_xlabel('X / mm', fontsize=9)
    ax2.set_ylabel('Y / mm', fontsize=9)
    ax2.set_zlabel('Z / mm', fontsize=9)
    ax2.view_init(elev=25, azim=45)
    
    # 子图 3: PFC 多球 Clump 颗粒填充形状库 (三种典型形态)
    ax3 = fig.add_subplot(1, 3, 3, projection='3d')
    
    # 形态 1: 块状次棱角 (中心在 (-15, 0, 0))
    pebbles_blocky = [
        (0, 0, 0, 5.0), (3.0, 2.5, 2.5, 3.2), (-3.0, -2.5, -2.5, 3.2),
        (3.0, -2.5, 0, 2.8), (-3.0, 2.5, 0, 2.8)
    ]
    for px, py, pz, pr in pebbles_blocky:
        u, v = np.mgrid[0:2*np.pi:15j, 0:np.pi:10j]
        xs = pr * np.cos(u) * np.sin(v) + px - 14.0
        ys = pr * np.sin(u) * np.sin(v) + py
        zs = pr * np.cos(v) + pz
        ax3.plot_surface(xs, ys, zs, color='#2ca02c', alpha=0.75)
        
    # 形态 2: 多棱角角状 (中心在 (0, 0, 0))
    pebbles_angular = [
        (0, 0, 0, 4.5), (3.2, 1.8, 1.5, 2.8), (-3.2, -1.8, 1.0, 2.8),
        (1.2, -2.5, -2.0, 2.6), (-1.5, 2.5, 2.0, 2.2)
    ]
    for px, py, pz, pr in pebbles_angular:
        u, v = np.mgrid[0:2*np.pi:15j, 0:np.pi:10j]
        xs = pr * np.cos(u) * np.sin(v) + px
        ys = pr * np.sin(u) * np.sin(v) + py
        zs = pr * np.cos(v) + pz
        ax3.plot_surface(xs, ys, zs, color='#ff7f0e', alpha=0.75)
        
    # 形态 3: 扁平状 (中心在 (+14, 0, 0))
    pebbles_flaky = [
        (0, 0, 0, 4.0), (3.0, 0, 0, 3.0), (-3.0, 0, 0, 3.0),
        (0, 2.5, 0, 2.5), (0, -2.5, 0, 2.5)
    ]
    for px, py, pz, pr in pebbles_flaky:
        u, v = np.mgrid[0:2*np.pi:15j, 0:np.pi:10j]
        xs = pr * np.cos(u) * np.sin(v) + px + 14.0
        ys = pr * np.sin(u) * np.sin(v) + py
        zs = pr * np.cos(v) + pz * 0.7
        ax3.plot_surface(xs, ys, zs, color='#9467bd', alpha=0.75)
        
    ax3.set_title('(c) PFC3D 多球 Clump 不规则骨料库', fontsize=11, fontweight='bold')
    ax3.set_xlabel('X / mm', fontsize=9)
    ax3.set_ylabel('Y / mm', fontsize=9)
    ax3.set_zlabel('Z / mm', fontsize=9)
    ax3.set_xlim(-22, 22)
    ax3.set_ylim(-10, 10)
    ax3.set_zlim(-10, 10)
    ax3.view_init(elev=25, azim=45)
    
    plt.suptitle('图 4 骨料形状库的建立', fontsize=13, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'Fig4_aggregate_clump_library.png'))
    plt.close()
    print('Rendered Fig 4 Aggregate Clump Library successfully.')

if __name__ == '__main__':
    render_fig4_aggregate_library()
