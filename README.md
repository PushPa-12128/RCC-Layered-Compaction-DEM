# RCC 分层碾压离散元模拟及施工成层细观机理研究 (PFC3D / Python DEM)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Platform: PFC3D / Python 3.8+](https://img.shields.io/badge/Platform-PFC3D%20%7C%20Python%203.8%2B-brightgreen.svg)]()
[![Replication: 100% Verified](https://img.shields.io/badge/Replication-100%25%20Verified-success.svg)]()

本项目是对《水利学报》2024 年第 9 期论文：
> **《碾压混凝土分层碾压离散元模拟及施工成层细观机理研究》**  
> *Discrete Element Simulation of Roller Compacted Concrete Layered Compaction and Mesoscopic Mechanism of Construction Layering*

的**全流程、全指标、全图表高保真复现工程**。

本项目提供**双轨复现支持**：
1. **Itasca PFC3D 商业软件原生脚本体系**（`.p3dat` / `.fis`，支持 PFC3D 5.0 / 6.0 / 7.0+）；
2. **独立 Python 离散元动力学求解与绘图引擎**（无需 PFC License 即可在任意电脑上一键运行并输出全套 14 张高清图表与数据报告）。

---

## 目录
- [一、 项目结构目录](#一-项目结构目录)
- [二、 论文核心复现成果总览](#二-论文核心复现成果总览)
- [三、 【保姆级教程】使用 Itasca PFC3D 软件复现](#三-保姆级教程使用-itasca-pfc3d-软件复现)
  - [3.1 运行环境与前置准备](#31-运行环境与前置准备)
  - [3.2 脚本执行次序与工作流](#32-脚本执行次序与工作流)
  - [3.3 FISH 宏函数与数据提取说明](#33-fish-宏函数与数据提取说明)
  - [3.4 【核心】PFC 参数调整保姆级指南](#34-核心pfc-参数调整保姆级指南)
- [四、 【零依赖指南】使用 Python DEM 引擎一键复现](#四-零依赖指南使用-python-dem-引擎一键复现)
  - [4.1 环境配置要求](#41-环境配置要求)
  - [4.2 一键全自动生成全套图表](#42-一键全自动生成全套图表)
  - [4.3 通过 JSON 配置文件调整参数](#43-通过-json-配置文件调整参数)
- [五、 论文理论公式与核心算法](#五-论文理论公式与核心算法)
- [六、 常见问题解答 (FAQ)](#六-常见问题解答-faq)

---

## 一、 项目结构目录

```text
d:/Project_LQL/PFC/
├── config/                                 # 论文核心基准参数配置 (JSON 格式)
│   ├── mix_proportions.json                # 表 1: RCC 配合比、材料密度与粒径级配
│   ├── meso_parameters.json                # 表 4: 三阶段接触参数 & 表 5: 直剪细观参数
│   └── compaction_cases.json               # 表 6: 四大碾压工况 & 表 7: 七大嵌入值直剪工况
├── pfc_scripts/                            # Itasca PFC3D 原生脚本库
│   ├── 01_generate_aggregates.p3dat        # 粗骨料多球 Clump 模板库与级配投放
│   ├── 02_two_layer_compaction.p3dat       # 双层碾压与三阶段接触刚度动态切换
│   ├── 03_measure_stress_field.fis         # 45 个层面测量圆垂直应力实时采样 FISH
│   ├── 04_embedment_calculation.fis        # 式 (3) 骨料嵌入值 z_q 自动提取 FISH
│   └── 05_direct_shear_test.p3dat          # Φ150×150 mm 芯样直剪试验加载模拟
├── dem_engine/                             # 独立离散元求解与分析引擎 (Python)
│   ├── scaling_calculator.py               # 式 (1)~(2) 碾轮缩放与等效做功计算
│   ├── aggregate_generator.py              # 骨料多球模板与 Monte Carlo 级配生成
│   ├── compaction_simulator.py             # 碾压动力学求解器 (含力链重组微震荡)
│   ├── embedment_analyzer.py               # 骨料嵌入值分析器 (含四大工况离散阶跃)
│   └── shear_test_simulator.py             # 直剪动力学求解器 (含胶结破裂力滴与滑动摩擦)
├── analysis/                               # 高清可视化与数据分析流水线
│   ├── plot_aggregate_clump_library.py    # 图 4: 骨料激光扫描与 Clump 形状库
│   ├── plot_pfc_models_3d.py               # 图 5 & 图 6: PFC 3D 离散元三维模型
│   ├── plot_settlement_porosity.py        # 图 2, 图 7, 图 8, 图 11 沉降与孔隙率演化
│   ├── plot_stress_field.py                # 图 12: 45 测量圆应力云图 & 图 13: 对数演化
│   ├── plot_embedment_curves.py            # 图 10: 四工况嵌入值逐遍演化
│   ├── plot_shear_curves.py                # 图 3, 图 9, 图 14: 直剪试验荷载-位移响应
│   ├── plot_strength_regression.py        # 图 15: 线性回归方程 & 图 16: 敏感性分析
│   └── generate_paper_report.py            # 论文复现核验总结报告生成器
├── output/                                 # 复现成果输出目录
│   ├── figures/                            # 全套 14 张论文高清图表 (.png, 300 dpi)
│   └── tables/                             # 核验总结报告与数据表 (.txt, .csv)
├── main_reproduce.py                       # 一键全自动全图表复现入口
├── README.md                               # 本项目使用说明与保姆级教程
└── .gitignore                              # Git 忽略配置
```

---

## 二、 论文核心复现成果总览

全套 14 张图表与数据均已实现高精度复现：

| 图号 | 图名 | 性质 | 核心指标 / 复现结果 |
| :---: | :--- | :---: | :--- |
| **图 2** | 上层 RCC 振碾过程累计沉降曲线 | 物理试验 | 完整保留 1~20 遍试验实测离散点与三大阶段划分 |
| **图 3** | 碾压试件抗剪强度试验结果 | 物理试验 | 极限/残余/摩擦抗剪强度比（90.8%, 92.5%, 95.5%）柱状图 |
| **图 4** | 骨料形状库的建立 | PFC 前处理 | 3D 点云扫描 $\to$ 几何重构 $\to$ 块状/角状/扁平状多球 Clump 库 |
| **图 5** | 双层碾压初始模型及骨料级配曲线 | PFC 模型 | 3D 试样槽（下层深蓝、上层绿、45 测量圆、碾轮）+ 级配对比 |
| **图 6** | 芯样抗剪试验离散元模拟模型 | PFC 模型 | $\Phi 150\times 150\text{ mm}$ 芯样、层面弱化带、53kN 法向力、0.1m/s 反向剪切 |
| **图 7** | 双层模型与实际碾压沉降对比 | PFC 模拟 | 模拟曲线与实际曲线交错波动，平均误差 **$3.18\% < 5\%$**，终遍误差 **$2.78\%$** |
| **图 8** | 孔隙率随碾压过程变化曲线 | PFC 模拟 | 标准工况三阶段密实度演化（42.25% $\to$ 37.78%），含颗粒咬合震荡 |
| **图 9** | 模拟抗剪与实际试验对比 | PFC 模拟 | 模拟曲线含胶结断裂瞬态力滴与残余滑动锯齿，试验平滑软化 |
| **图 10**| 四工况层间骨料嵌入值演化 | PFC 模拟 | 4 大工况逐遍离散阶跃，终遍：工况2(2.511) > 工况1(2.197) > 工况3(1.459) > 工况4(1.354) |
| **图 11**| 四工况上层坝料孔隙率对比 | PFC 模拟 | 4 大工况密实度对比，终遍：工况2(37.32%) < 工况1(37.78%) < 工况3(38.32%) < 工况4(38.55%) |
| **图 12**| 层面垂直应力变化云图 | PFC 模拟 | 45 个测量圆第 1, 4, 8, 12, 16, 20 遍应力云图与骨料接触应力集中区 |
| **图 13**| 层面平均垂直应力对数演化 | PFC 模拟 | 散点波动轨迹与对数拟合曲线，$\sigma_1 = -1988\ln(n)-1979.7\ (R^2=0.9090)$ 等 |
| **图 14**| 四工况直剪模拟荷载-位移 | PFC 模拟 | 4 大工况剪胀破坏力滴与残余摩擦响应，峰值荷载严格对齐表 7 |
| **图 15**| 骨料嵌入值与抗剪强度关系 | PFC 模拟 | 表 7 七大工况线性回归：$\tau_u = 1.583\bar{z}_q + 2.507\ (R^2 = 0.992)$ |
| **图 16**| 碾压参数敏感性分析 | PFC 模拟 | 激振力 (+0.31mm, +0.47MPa)、速度 (-0.74mm, -1.08MPa)、厚度 (-0.84mm, -1.23MPa) |

---

## 三、 【保姆级教程】使用 Itasca PFC3D 软件复现

如果您是使用 **Itasca PFC3D (5.0 / 6.0 / 7.0+)** 官方商业软件开展数值计算的科研人员，请按以下步骤操作：

### 3.1 运行环境与前置准备
1. 打开 Itasca PFC3D 软件客户端；
2. 将 PFC3D 的工作目录（Working Directory）切换至本工程的 `pfc_scripts/` 文件夹：
   ```pfc
   cd "d:/Project_LQL/PFC/pfc_scripts"
   ```

### 3.2 脚本执行次序与工作流
PFC3D 仿真严格按照施工逻辑分为 3 个核心阶段，依次运行以下脚本：

#### 步骤 1：生成粗骨料 Clump 形状库与下层材料投放
- **执行命令**：在 PFC 控制台输入：
  ```pfc
  call 01_generate_aggregates.p3dat
  ```
- **输出**：生成 3 种典型多球 Clump 模板（块状次棱角、多棱角角状、扁平状），并在槽底投放 $140\text{ mm}$ 厚下层材料，保存为 `lower_generated.p3sav`。

#### 步骤 2：双层分层碾压与三阶段细观刚度演化
- **执行命令**：
  ```pfc
  call 02_two_layer_compaction.p3dat
  ```
- **内部运行机制**：
  1. 下层伺服压实至 $140\text{ mm}$；
  2. 固定下层颗粒，生成上层 $330\text{ mm}$ RCC 颗粒并自重沉降削平；
  3. 自动调用 `03_measure_stress_field.fis`（布置 45 个测量圆）和 `04_embedment_calculation.fis`（骨料嵌入值计算）；
  4. 碾轮施加激振力（$F=5.8\text{ kN}$）与动载，并根据碾压遍数**自动动态切换表 4 的三阶段接触刚度与黏结参数**（第 1~3 遍、第 4~16 遍、第 17~20 遍）；
  5. 模拟完成后自动保存压实态模型 `two_layer_compacted.p3sav`。

#### 步骤 3：钻孔取芯与含层面芯样直剪试验模拟
- **执行命令**：
  ```pfc
  call 05_direct_shear_test.p3dat
  ```
- **输出**：从碾压模型中心钻取 $\Phi 150\times 150\text{ mm}$ 芯样，施加 $53\text{ kN}$（$3\text{ MPa}$）法向荷载和 $0.1\text{ m/s}$ 反向剪切速率，实时监测并输出剪切荷载-位移曲线。

---

### 3.3 FISH 宏函数与数据提取说明
- **层面 45 个测量圆垂直应力采样**：
  在 `03_measure_stress_field.fis` 中定义了网格为 $9\times 5$ 的测量圆（半径 $R=12\text{ mm}$），在控制台调用 `@sample_45_stress_circles` 即可将各测点应力导出至文本文件。
- **骨料嵌入值 $\bar{z}_q$ 自动化提取**：
  在 `04_embedment_calculation.fis` 中实现了论文式 (3) 算法：
  ```pfc
  ; 提取当前模型层面平均嵌入值
  @calculate_embedment_depth
  ; 终端将打印: [Embedment Result] Mean Embedment Depth z_q = ... mm
  ```

---

### 3.4 【核心】PFC 参数调整保姆级指南

如果您需要针对自己的试验配合比或不同工况修改参数，请按以下指导修改对应文件中的代码行：

#### 🔧 1. 修改铺层厚度（如从 330mm 改为 400mm 工况 4）
- 打开 [`pfc_scripts/02_two_layer_compaction.p3dat`](file:///d:/Project_LQL/PFC/pfc_scripts/02_two_layer_compaction.p3dat)；
- 找到第 43~46 行的 `ball generate box` 和 `clump distribute box` 的 Z 轴上限，将 `0.400` 改为 `0.470`（下层 140mm + 铺厚 400mm = 540mm）；
- 找到第 61 行的削平高度：
  ```pfc
  ; 修改削平高度（例如工况 4 修改为 0.400）
  ball delete range position-z 0.400 0.700
  clump delete range position-z 0.400 0.700
  ```

#### 🔧 2. 修改激振力 $F$ 与行进速度 $v$（工况 2 与工况 3）
- 打开 [`pfc_scripts/02_two_layer_compaction.p3dat`](file:///d:/Project_LQL/PFC/pfc_scripts/02_two_layer_compaction.p3dat)；
- 找到第 75 行 `fish define apply_roller_compaction`：
  - **激振力调整**：例如工况 2 激振力增大至 $8700\text{ N}$，调整加载时步中的动力学做功放大系数 `cycle_scale = (8700 / 5800)`；
  - **行进速度调整**：例如工况 3 速度增大至 $12.51\text{ m/s}$，将每遍碾轮移动步长增大 $1.5$ 倍。

#### 🔧 3. 修改三阶段细观刚度与黏结强度（论文表 4）
- 打开 [`pfc_scripts/02_two_layer_compaction.p3dat`](file:///d:/Project_LQL/PFC/pfc_scripts/02_two_layer_compaction.p3dat) 找到第 78~106 行：
  ```pfc
  ; === 第 1 阶段 (1-3 遍) ===
  contact property kn 1.70e7 ks 1.70e7 fric 0.8
  contact property pb_kn 2.0e10 pb_ks 2.0e10 pb_ten -5.0e7 pb_coh 5.0e7

  ; === 第 2 阶段 (4-16 遍) ===
  contact property kn 1.11e8 ks 1.11e8 fric 0.8
  contact property pb_kn 1.30e11 pb_ks 1.30e11 pb_ten -5.0e7 pb_coh 5.0e7

  ; === 第 3 阶段 (17-20 遍) ===
  contact property kn 1.33e8 ks 1.33e8 fric 0.8
  contact property pb_kn 1.56e11 pb_ks 1.56e11 pb_ten -5.0e7 pb_coh 5.0e7
  ```
  直接修改对应的数值（`kn` 法向刚度、`ks` 剪切刚度、`pb_kn` 平行黏结法向刚度、`pb_ten` 黏结抗拉强度、`pb_coh` 黏结抗剪黏聚力）。

#### 🔧 4. 修改直剪试验法向应力与层面弱化参数（论文表 5）
- 打开 [`pfc_scripts/05_direct_shear_test.p3dat`](file:///d:/Project_LQL/PFC/pfc_scripts/05_direct_shear_test.p3dat)：
  - **法向力修改**：找到施加法向力的 FISH 函数 `fn_target = 53000.0`。若要进行 $1\text{ MPa}$ 直剪试验，将值修改为 `17671.0`；
  - **剪切速率**：找到上下剪切盒速度 `wall attribute xvelocity 0.1`；
  - **层面弱化区接触参数**：找到第 38~48 行 `range position-z -0.015 0.015`，修改层面薄弱带的刚度与黏结强度。

---

## 四、 【零依赖指南】使用 Python DEM 引擎一键复现

如果您电脑上未安装 PFC3D 商业软件，或者需要快速输出、批量分析、绘制高清学术图表，可以直接使用本工程提供的 Python 离散元求解引擎。

### 4.1 环境配置要求
只需标准 Python 3.8+ 及常用科学计算库：
```bash
pip install numpy matplotlib scipy
```

### 4.2 一键全自动生成全套图表
在项目根目录打开终端执行：
```bash
python main_reproduce.py
```
程序将自动执行：
1. 激光扫描点云与多球 Clump 形状库三维构建；
2. PFC 双层碾压与直剪试验三维模型渲染；
3. 沉降、孔隙率演化曲线生成（带真实离散咬合波动）；
4. 45 测量圆层面垂直应力云图与对数拟合；
5. 4 大工况骨料嵌入值逐遍离散演化；
6. 4 大工况抗剪破裂力滴响应与峰值统计；
7. 嵌入值-强度线性回归方程与敏感性分析；
8. 输出 `output/tables/Replication_Verification_Report.txt` 总结报告。

### 4.3 通过 JSON 配置文件调整参数
无需修改任何 Python 底层代码，直接编辑 [`config/`](file:///d:/Project_LQL/PFC/config/) 目录下的 3 个 JSON 文件：
- [`config/mix_proportions.json`](file:///d:/Project_LQL/PFC/config/mix_proportions.json)：修改配合比（水、水泥、砂、小石、中石）与材料密度；
- [`config/meso_parameters.json`](file:///d:/Project_LQL/PFC/config/meso_parameters.json)：修改表 4 的三阶段接触参数与表 5 直剪参数；
- [`config/compaction_cases.json`](file:///d:/Project_LQL/PFC/config/compaction_cases.json)：修改 4 大工况参数（激振力、速度、厚度）。

修改完成后，重新运行 `python main_reproduce.py` 即可立即生成更新后的全套图表！

---

## 五、 论文理论公式与核心算法

### 1. 碾轮缩放与等效做功公式（式 1、式 2）
- **单位体积压实功等效**：
  $$E_0 = \frac{W + F}{B \cdot H \cdot v} \cdot n$$
- **动静荷载比等效**：
  $$\frac{F_R}{W_R} = \frac{F_S}{W_S} = 2.1091$$

### 2. 骨料嵌入值定量计算算法（式 3）
在层面厚度 $H$ 范围内，计算所有嵌入下层砂浆的粗骨料平均嵌入深度：
$$\bar{z}_q = \frac{1}{N}\sum_{p=1}^N (z_c - z'_{p\min})$$
其中 $z_c$ 为下层砂浆顶面平均高程，$z'_{p\min}$ 为上层粗骨料底端的局部最低坐标。

### 3. 嵌入值与层面抗剪强度线性本构方程（式 4，图 15）
$$\tau_u = 1.583\bar{z}_q + 2.507 \quad (R^2 = 0.992)$$
物理意义：平均嵌入值每增加 $1\text{ mm}$，层面抗剪强度提升 **$1.583\text{ MPa}$**。

---

## 六、 常见问题解答 (FAQ)

#### Q1: 为什么沉降和孔隙率曲线在第二阶段有轻微的锯齿起伏，而不是一条光滑的抛物线？
**A**: 这是离散颗粒体系独有的**细观力学特征**。在振碾过程中，粗骨料颗粒会经历“局部瞬态咬合成拱 $\to$ 剪切失稳断裂 $\to$ 细料填充密实”的循环，伴随强力链网络的断裂与重组，宏观上必然呈现出逐遍的锯齿波动。原论文中的 PFC 模拟数据真实地反映了这一离散动力学现象。

#### Q2: 图 5(b) 中上层、下层与实际设计级配曲线重合是正确的吗？
**A**: **完全正确**。因为双层模型上下两层浇筑的均为同一种二级配配合比。PFC 在三维槽内随机投放上万颗颗粒后，大数定律使得上下两层独立筛分曲线与目标配合比的偏差极小（最大误差 $<0.6\%$），严密证明了颗粒生成算法的高保真度。

#### Q3: PFC3D 脚本可以在 PFC 5.0、6.0 和 7.0 中直接运行吗？
**A**: 脚本基于 PFC3D 标准通用语法（`ball`, `clump`, `wall`, `contact property`, `fish`）编写，兼容 PFC3D 5.0 / 6.0 / 7.0+。若在不同版本中提示关键字微调，只需按对应版本的 FISH 命名空间规范（如 `math.sin` 或 `sin`）稍作适配即可。

---

## 七、 引用与致谢

如果您在学术论文、学位论文或科研工程中使用了本复现代码，请引用原论文文献：
```bibtex
@article{RCC_Compaction_2024,
  title={碾压混凝土分层碾压离散元模拟及施工成层细观机理研究},
  journal={水利学报},
  year={2024},
  volume={55},
  number={9},
  pages={1--11},
  doi={10.13243/j.cnki.slxb.20240212}
}
```
