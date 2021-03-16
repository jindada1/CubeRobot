# 三阶魔方还原机器人

基于 python 和 Arduino，实现能够还原三阶魔方的机械结构



## 系统流程

1. 通过摄像头识别魔方颜色
2. 将识别结果转化成魔方求解算法的输入
3. 执行魔方求解算法，得出还原操作序列
3. 指令优化与碰撞规避处理
4. 通过wifi将序列发给硬件控制器
5. 硬件控制器按照序列，控制机械结构执行还原
6. over



## requirements

python 版本: 3.x


+ pywifi
+ pillow
+ numpy
+ opencv-python 



## 开发

### 软件部分

- [x] tkinter gui [组件](https://github.com/jindada1/CubeRobot/tree/master/components)的设计与开发

  - [x] Camera：基于cv2.VideoCapture 构造的摄像头管理类 
  
  - [x] HoverButton：基于 tk.Button 提供可带参数事件绑定接口，并做了些许美化
  
  - [x] ViewCanvas：**颜色数据采集与调试工具**中的面板，用于展示视频与图片
  
  - [x] CubeFloorPlan：用于绘制并管理魔方平面展开图，存储并管理整个魔方的色块分布，并生成魔方色块序列
  
  - [x] HSVAdjuster：**颜色数据采集与调试工具**中的面板，实时调整颜色识别中使用的 hsv 范围并保存
  
  - [x] SampleAdjuster：**颜色数据采集与调试工具**中的面板，实时调整用于颜色识别的采样范围并保存

  - [x] Console：控制台模块，用于**主控程序**运行时的状态输出

  - [x] Window：Tk 窗口的封装，提供了 update_func 接口
  
  - [x] CameraCanvas：摄像头视频展示面板，用于**主控程序**

- [x] [颜色数据采集与调试工具](https://github.com/jindada1/CubeRobot/blob/master/guiconfig.py)的开发

  - [x] [数据设置与加载模块](https://github.com/jindada1/CubeRobot/tree/master/setting)

  - [x] [计算机视觉模块](https://github.com/jindada1/CubeRobot/blob/master/vision.py)：魔方定位与颜色块的识别

    - [x] 全局二值化色块定位
  
    - [x] 形态学处理与魔方定位
  
    - [x] 手动定位，固定点采样
  
    - [x] 颜色识别

  ```
  pip install -r requirements.txt
  python3 guiconfig.py
  ```

- [x] [魔方模拟器](https://github.com/jindada1/CubeRobot/blob/master/sock/emulator.html)的开发

  - [x] 虚拟魔方的实现

  - [x] 执行还原序列

  - [x] 获取魔方状态

  - [x] twophase 求解接口的[后台服务器](https://github.com/jindada1/CubeRobot/blob/master/sock/http_server.py)


- [x] 主控程序的开发

  - [x] [计算机视觉模块](https://github.com/jindada1/CubeRobot/blob/master/vision.py)：魔方定位与颜色块的识别

  - [x] [魔方求解模块](https://github.com/jindada1/CubeRobot/tree/master/twophase)：[twophase](https://github.com/hkociemba/RubiksCube-TwophaseSolver)算法

  - [x] 指令调整与优化
    
    - [x] 机器动作指令集的设计
    
    - [x] 标准还原序列到机器动作指令序列的转化
    
    - [x] 碰撞规避处理

  - [x] [wifi模块](https://github.com/jindada1/CubeRobot/blob/master/sock/esp_client.py)

    - [x] wifi检测与连接

    - [x] 自动获取 esp8266 模块在 ap 模式下的 ip 地址
    
    - [x] 发送数据和接收数据



### 硬件部分

- [x] esp8266

  - [x] ap 模式

  - [x] 提供路由处理来自客户端的请求，并返回处理结果

- [x] 操作序列的解析

- [x] 电机控制逻辑

  - [x] 单个电机动作控制

  - [x] 多个电机同步运行

  - [x] 单个电机角度微调



## 机械结构建模

模型及装配体如下图所示，所有原文件在[sldprt](/models/sldprt)目录下

![凹槽凸轮](https://s1.ax1x.com/2020/10/07/0aR97F.png)

导出的3D打印模型在[stl](/models/stl)目录下

### 动图演示

凹槽凸轮             |  魔方翻转       
:-------------------------:|:-------------------------:
![](https://s1.ax1x.com/2020/10/07/0a21yV.gif)  |  ![](https://s1.ax1x.com/2020/10/07/0a2Yo4.gif)

|装配爆炸视图           |
|:-------------------------:|
|![](https://s1.ax1x.com/2020/10/07/0a2om8.gif)  |

### 实物照片

翻转魔方             |  魔鬼接线       
:-------------------------:|:-------------------------:
![](readme/%E7%BF%BB%E8%BD%AC%E9%AD%94%E6%96%B9.png)  |  ![](readme/%E9%AD%94%E9%AC%BC%E6%8E%A5%E7%BA%BF.png)

识别魔方色块分布             |  旋转魔方面       
:-------------------------:|:-------------------------:
![](readme/%E8%AF%86%E5%88%AB%E9%AD%94%E6%96%B9%E8%89%B2%E5%9D%97%E5%88%86%E5%B8%83.png)  |  ![](readme/%E6%97%8B%E8%BD%AC%E9%AD%94%E6%96%B9%E9%9D%A2.png)