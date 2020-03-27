# 三阶魔方还原机器人

基于 python 和 Arduino，实现能够还原三阶魔方的机械结构



## 系统流程

1. 通过摄像头识别魔方颜色
2. 将识别结果转化成魔方求解算法的输入
3. 执行魔方求解算法，得出还原操作序列
4. 通过蓝牙模块将序列发给硬件控制器
5. 硬件控制器按照序列，控制机械结构执行还原
6. over



## requirements

+ python3
+ matplotlib  
+ numpy
+ opencv-python 
+ pillow 



## 进度

### 软件部分

- [x] tkinter gui 组件设计与开发，[这里](https://github.com/jindada1/CubeRobot/tree/master/components)

  - [x] Camera：基于cv2.VideoCapture 构造的摄像头管理类 
  
  - [x] HoverButton：基于 tk.Button 提供可带参数事件绑定接口，并做了些许美化
  
  - [x] ViewCanvas：**颜色数据采集与调试工具**中的面板，用于展示视频与图片
  
  - [x] CubeFloorPlan：用于绘制并管理魔方平面展开图，存储并管理整个魔方的色块分布
  
  - [x] HSVAdjuster：**颜色数据采集与调试工具**中的面板，实时调整颜色识别中使用的 hsv 范围并保存
  
  - [x] SampleAdjuster：**颜色数据采集与调试工具**中的面板，实时调整用于颜色识别的采样范围并保存

  - [x] Console：控制台模块，用于**主控程序**运行时的状态输出

  - [x] Window：Tk 窗口的封装，提供了 update_func 接口
  
  - [x] CameraCanvas：摄像头视频展示面板，用于**主控程序**

- [x] [颜色数据采集与调试工具](https://github.com/jindada1/CubeRobot/blob/master/guiconfig.py)的开发

  ```
  pip install -r requirements.txt
  python3 guiconfig.py
  ```

- [ ] 主控程序的开发

  - [x] [计算机视觉模块](https://github.com/jindada1/CubeRobot/blob/master/cube_vision.py)：魔方颜色块的识别

  - [ ] 魔方求解模块

  - [ ] 蓝牙模块



### 硬件部分

- [ ] 蓝牙连接及操作序列的接收模块
- [ ] 电机控制逻辑