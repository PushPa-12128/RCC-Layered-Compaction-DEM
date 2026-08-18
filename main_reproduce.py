# -*- coding: utf-8 -*-
"""
《水利学报 2024》RCC 分层碾压离散元模拟及施工成层细观机理研究 - 全流程全图表一键复现主入口
涵盖论文全部图表:
- 图 2: 上层 RCC 振碾过程累计沉降曲线 (物理试验)
- 图 3: 碾压试件抗剪强度试验结果 (物理试验)
- 图 4: 骨料形状库的建立 (PFC 前处理激光扫描与 Clump 不规则骨料生成)
- 图 5: RCC 双层碾压初始模型及其骨料级配曲线 (PFC 离散元三维模型 + 级配对比)
- 图 6: RCC 含层面芯样抗剪试验离散元模拟模型 (PFC 直剪试验三维模型)
- 图 7: 双层模型与实际碾压累计沉降曲线对比 (PFC 离散动力学沉降 vs 试验实测)
- 图 8: 孔隙率随碾压过程变化曲线 (PFC 颗粒密实度三阶段演化与逐遍咬合震荡)
- 图 9: 模拟抗剪测试与实际试验的荷载-位移关系对比 (PFC 胶结断裂力滴 vs 试验)
- 图 10: 不同工况下层间骨料嵌入值随碾压遍数的变化曲线 (PFC 4 大工况式 3 提取演化)
- 图 11: 不同工况下上层坝料孔隙率随碾压遍数的变化曲线 (PFC 4 大工况密实度对比)
- 图 12: 不同碾压遍数下坝料层面垂直应力变化云图 (PFC 第 1, 4, 8, 12, 16, 20 遍 45 测量圆云图)
- 图 13: 不同工况下层面平均垂直应力随碾压遍数的变化曲线 (PFC 4 大工况对数演化拟合)
- 图 14: 不同工况下抗剪模拟荷载-位移曲线结果统计 (PFC 4 大工况直剪破裂响应)
- 图 15: 层间骨料嵌入值与模拟抗剪强度关系 (PFC 表 7 线性回归方程)
- 图 16: 碾压参数对嵌入值和层间结合质量的影响程度分析 (PFC 参数敏感性分析)
"""
import os, sys

def main():
    print('\n' + '='*80)
    print('   正在启动论文《水利学报 2024》RCC 双层碾压离散元全流程高保真复现程序...')
    print('='*80 + '\n')
    
    from analysis.plot_aggregate_clump_library import render_fig4_aggregate_library
    from analysis.plot_pfc_models_3d import render_fig5_fig6_models
    from analysis.plot_settlement_porosity import plot_fig2_and_fig7_settlement, plot_fig8_and_fig11_porosity
    from analysis.plot_stress_field import plot_fig12_stress_contour, plot_fig13_stress_evolution
    from analysis.plot_embedment_curves import plot_fig10_embedment_curves
    from analysis.plot_shear_curves import plot_fig3_shear_comparison, plot_fig9_and_fig14_shear_curves
    from analysis.plot_strength_regression import plot_fig15_and_table7_regression, plot_fig16_sensitivity_analysis
    from analysis.generate_paper_report import generate_replication_summary
    
    print('--> [1/8] 正在生成 PFC 骨料形状库激光扫描点云与多球 Clump 模型图 (Fig 4)...')
    render_fig4_aggregate_library()
    
    print('--> [2/8] 正在生成 PFC3D 双层碾压与直剪试验三维模型图 (Fig 5, Fig 6)...')
    render_fig5_fig6_models()
    
    print('--> [3/8] 正在生成沉降曲线与孔隙率演化对比图 (Fig 2, Fig 7, Fig 8, Fig 11)...')
    plot_fig2_and_fig7_settlement()
    plot_fig8_and_fig11_porosity()
    
    print('--> [4/8] 正在生成45个测量圆层面垂直应力场云图与对数演化拟合图 (Fig 12, Fig 13)...')
    plot_fig12_stress_contour()
    plot_fig13_stress_evolution()
    
    print('--> [5/8] 正在生成四种工况下层间骨料嵌入值逐遍离散演化曲线 (Fig 10)...')
    plot_fig10_embedment_curves()
    
    print('--> [6/8] 正在生成抗剪试验破裂力滴荷载-位移曲线与强度柱状图 (Fig 3, Fig 9, Fig 14)...')
    plot_fig3_shear_comparison()
    plot_fig9_and_fig14_shear_curves()
    
    print('--> [7/8] 正在生成嵌入值-抗剪强度线性回归方程与敏感性分析图 (Fig 15, Fig 16, Table 7)...')
    plot_fig15_and_table7_regression()
    plot_fig16_sensitivity_analysis()
    
    print('--> [8/8] 正在输出论文复现核验总结报告...')
    generate_replication_summary()
    
    print('\n' + '='*80)
    print('   【复现成功】全套 14 张论文图表与数据已全部输出至 output/ 目录下!')
    print('='*80 + '\n')

if __name__ == '__main__':
    main()
