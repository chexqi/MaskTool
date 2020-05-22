# -*- coding:utf-8 _*-
"""
生成多边形Mask,Mask以内的区域不监测，也可以用于实现分割标签制作
左键单击：增加一个多边形点
右键单击：减少最近的一个点
左键双击：在mask上绘制当前的多边形
v，V：选择模型，True为增加前景，False为增加背景
s，S：保存绘制的mask
q，Q，esc：退出程序
@Author  : Xiaoqi Cheng
@Time    : 2020/5/22 14:39 
"""
import cv2, os
import numpy as np

mode = True  # mask操作模式，True增加mask区域，False减少区域， 按键v反转模式

# %% 读取一幅正常图像和mask图像
img= cv2.imread('test.bmp', cv2.IMREAD_COLOR)
mask_path = 'mask.bmp'
if os.path.exists(mask_path):
	mask_img = cv2.imread(mask_path, cv2.IMREAD_COLOR)
	mask_img[:,:,0:2]=0
else:
	mask_img = np.zeros_like(img)
h, w = img.shape[0:2]

# %% 定义两个点数组，一个存储已经记录的点坐标，一个存储移动过程中的点坐标
poly_ps = np.empty((0,2), dtype=np.int)     # 左键单击下的坐标
move_ps = np.empty((0,2), dtype=np.int)     # 比poly_ps多一个鼠标移动过程中的点坐标
# %% 定义回调函数，
def draw_mask(event, x, y, flags, param):
	if x < w*0.02: x=0      # 自动吸附
	if x > w*0.98: x=w-1
	if y < h*0.02: y=0
	if y > h*0.98: y=h-1
	global poly_ps, move_ps, mask_img, i_m
	if len(poly_ps)>0 and event == cv2.EVENT_MOUSEMOVE:     # 鼠标移动过程中，实时记录坐标
		move_ps = np.vstack((poly_ps, np.array([[x, y]])))
	elif event == cv2.EVENT_LBUTTONDOWN:                    # 左键按下，记录当前点
		poly_ps = np.vstack((poly_ps, np.array([[x, y]])))
		move_ps = np.vstack((poly_ps, np.array([[x, y]])))
	elif len(poly_ps)>0 and event == cv2.EVENT_RBUTTONDOWN: # 右键按下，删除最后记录的一个点
		poly_ps = poly_ps[0:-1]
		move_ps = poly_ps[0:-1]
	elif len(poly_ps)>=3 and event == cv2.EVENT_LBUTTONDBLCLK: # 左键双击，记录当前多边形
		if mode:
			cv2.fillPoly(mask_img, np.expand_dims(move_ps, axis=0), (0, 0, 255))
		else:
			cv2.fillPoly(mask_img, np.expand_dims(move_ps, axis=0), (0, 0, 0))
		poly_ps = np.empty((0, 2), dtype=np.int)  # 左键单击下的坐标
		move_ps = np.empty((0, 2), dtype=np.int)  # 比poly_ps多一个鼠标移动过程中的点坐标

cv2.namedWindow('Mask define')
cv2.setMouseCallback('Mask define', draw_mask)

# 绘制多边形，注意避免多边形累计
while 1:
	print(move_ps.shape, "Mode:", mode)
	if len(move_ps)>=2:
		if mode:
			temp = cv2.polylines(mask_img.copy(), np.expand_dims(move_ps, axis=0), 1, (0,0,255))    # 填充前景
		else:
			temp = cv2.polylines(mask_img.copy(), np.expand_dims(move_ps, axis=0), 1, (0,255,0))      # 填充背景
		show_img = cv2.add(temp, img)  # 用于显示的图像
	else:
		show_img = cv2.add(mask_img, img)  # 用于显示的图像
	cv2.imshow('Mask define', show_img)
	k = cv2.waitKey(15)
	if k in [83, 115]:      # 83:S, 115:s
		cv2.imwrite(mask_path, mask_img[:, :, -1])  # 只保存红色通道
	elif k in [86, 118]:
		mode = not mode
	elif k in [27, 81, 113]:  # 27:esc, 113:q, 81:Q
		break