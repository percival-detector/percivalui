#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

import numpy as np


from PyQt5 import QtWidgets, QtGui, QtCore, uic

import pyqtgraph as pg
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')
pg.setConfigOption('imageAxisOrder','row-major')

from pyqtgraph.graphicsItems.GradientEditorItem import Gradients
Gradients['grey2'] = {'ticks': [(0.0, (255, 255, 255, 255)), (0.25,(192,192,192,255)), (0.5, (128,128,128,255)), (0.75, (64,64,64,255)),(1.0, (0, 0, 0, 255))], 'mode': 'rgb'}
Gradients['rainbow'] = {'ticks': [(0.0, (0,0,143,255)), (0.2, (0,0,255,255)), (0.4, (0,255,255,255)), (0.6, (255,255,0,255)), (0.8, (255,0,0,255)), (1, (128,0,0,255))], 'mode': 'rgb'}
Gradients['blue2'] = {'ticks' :[(0.0, (0x31, 0x82, 0xbd)), (0.5, (0x9e,0xca,0xe1)), (1.0, (0xde,0xeb,0xf7))], 'mode': 'rgb'}
Gradients['purple2'] = {'ticks' :[(0.0, (0x75, 0x6b, 0xb1)), (0.5, (0xbc,0xbd,0xdc)), (1.0, (0xef,0xed,0xf5))], 'mode': 'rgb'}
Gradients['rainbow2'] = {'ticks': [(0.0, (255,255,255,255)), (0.001, (0,0,143,255)), (0.2, (0,0,255,255)), (0.4, (0,255,255,255)), (0.6, (255,255,0,255)), (0.8, (255,0,0,255)), (1, (128,0,0,255))], 'mode': 'rgb'}

class PG_ImageView2(pg.GraphicsView):
	def __init__(self, parent = None, invertY = False, invertX = False):
		super(PG_ImageView2, self).__init__(parent)

		# Main image 
		self.mgv_vbm = pg.ViewBox(invertY=invertY, invertX=invertX)
		self.mgv_vbm.setAspectLocked()

		# X-Y axis of Main image
		self.mgv_vbm_xaxis = pg.AxisItem(orientation='bottom', linkView=self.mgv_vbm)
		self.mgv_vbm_yaxis = pg.AxisItem(orientation='left', linkView=self.mgv_vbm)

		# Color scale bar of Main Image
		self.mgv_hist = pg.HistogramLUTItem(image = None, fillHistogram = True)
		self.mgv_hist.gradient.loadPreset('rainbow')


		# Grid Layout in mgv
		self.mgv_gvl = QtWidgets.QGraphicsGridLayout()
		self.mgv_gvl.setHorizontalSpacing(0)
		self.mgv_gvl.setVerticalSpacing(0)

		#******************************************
		self.centralWidget.setLayout(self.mgv_gvl)
		#******************************************

		self.mgv_gvl.addItem(self.mgv_vbm_yaxis, 0, 0)
		self.mgv_gvl.addItem(self.mgv_vbm      , 0, 1)
		self.mgv_gvl.addItem(self.mgv_hist     , 0, 2)

		self.mgv_gvl.addItem(self.mgv_vbm_xaxis, 1, 1)

		self.mgv_gvl.setColumnMinimumWidth(1, 200)

		self.mgv_gvl.setRowMinimumHeight(0, 200)

		self.mgv_vbm_item = pg.ImageItem(name='ImgData')

		self.mgv_vbm.addItem(self.mgv_vbm_item)
		self.mgv_hist.setImageItem(self.mgv_vbm_item)

		self.Data = None

		self.setImage(np.random.rand(1484,1408).astype(np.float32)*5 + 5.0, update_hist = True)


	def setImage(self, Data, update_hist = False):
		self.Data = Data.astype(np.float32)
		self.mgv_vbm_item.setImage(self.Data, autoLevels=False)
		#self.mgv_vby_item.setData(x=self.Data.mean(axis=1), y=np.arange(self.Data.shape[0]))
		#self.mgv_vbx_item.setData(x=np.arange(self.Data.shape[1]), y = self.Data.mean(axis=0))
		#self.mgv_hist.setImageItem(self.mgv_vbm_item)
		if update_hist:
			self.mgv_hist.setLevels(self.Data.min(), self.Data.max())
			self.mgv_hist.setHistogramRange(self.Data.min(), self.Data.max())

	def setHistRange(self, level_min_value, level_max_value, range_min_value = None, range_max_value = None):
		self.mgv_hist.setLevels(level_min_value, level_max_value)
		if (range_min_value is None) or (range_max_value is None) : 
			self.mgv_hist.setHistogramRange(level_min_value, level_max_value)
		else:
			self.mgv_hist.setHistogramRange(range_min_value, range_max_value)
