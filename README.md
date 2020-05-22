# MaskTool
MaskTool: Generate mask image based on opencv 基于opencv绘制多边形，进而生成mask图像

### 使用方法
生成多边形Mask,Mask以内的区域不监测，也可以用于实现分割标签制作
左键单击：增加一个多边形点
右键单击：减少最近的一个点
左键双击：在mask上绘制当前的多边形
v，V：选择模型，True为增加前景，False为增加背景
s，S：保存绘制的mask
q，Q，esc：退出程序

![image](https://github.com/chexqi/MaskTool/blob/master/1.png)

![image](https://github.com/chexqi/MaskTool/blob/master/2.png)