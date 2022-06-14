import sys
from threading import Thread
from types import MethodType
import cv2
import numpy as np

from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication,QMainWindow
from PyQt5.QtGui import QImage,QPixmap
from PyQt5.QtCore import pyqtSignal,pyqtSlot,Qt

from draw_window import DrawWindow

#### FUNCTION USED ##

def dragEnterEvent(self, event):
		if event.mimeData().hasImage:
			event.accept()
		else:
			event.ignore()

def dragMoveEvent(self, event):
	if event.mimeData().hasImage:
		event.accept()
	else:
		event.ignore()

def dropEvent(self,event):
	if event.mimeData().hasImage:
		event.setDropAction(Qt.CopyAction)
		filepath = event.mimeData().urls()[0].toLocalFile()
		self.set_image(filepath)
		event.accept()
	else:
		event.ignore()

def set_image(self,filepath):
	self.image = QPixmap(filepath)
	self.cvimage = cv2.imread(filepath)
	self.cvimage = cv2.cvtColor(self.cvimage,cv2.COLOR_BGR2GRAY)
	cv2.imshow('immagine',self.cvimage)
	cv2.waitKey(0)
	self.setPixmap(self.image)

# def setPixmap(self, image):
# 	super().SetPixmap(image)



class MainWindow(QMainWindow):
	
	def __init__(self):
		super(MainWindow,self).__init__()
		loadUi("main.ui",self)
		
		self.dialog_execution = False
		self._define_slots()
		self._add_method_to_label_class()
		

	def _define_slots(self):
		self.draw_window_button.clicked.connect(self._call_draw_window)
		self.execute_button.clicked.connect(self._call_pattern_detection)
	
	def update_train_image(self,image):
	
		self.train_image_label.setAlignment(Qt.AlignCenter)
		self.train_image_label.setPixmap(image)
		w = image.size().width()
		h = image.size().height()
		image = image.toImage()
		image_array = np.array(image.constBits().asarray(h*w*4)).reshape(h,w,4)
		self.cvtrainimage = cv2.cvtColor(image_array,cv2.COLOR_BGR2GRAY)
		cv2.imshow('gray_train_foto',self.cvtrainimage)
		cv2.waitKey(0)

	def _call_draw_window(self):
		if not self.dialog_execution:
			self.dialog_execution = True
			self.dialog = DrawWindow(self.image_label.image)
			self.dialog.updt_train.connect(self.update_train_image)
			self.dialog.is_closed.connect(self._change_dialog_execution)
			self.dialog.show()
			self.dialog.exec_()
	
	def _change_dialog_execution(self):
		self.dialog_execution = False

	def _call_pattern_detection(self):
		#TODO: implement the pattern recognition algorithm 
		pass

	def _add_method_to_label_class(self):
		self.image_label.setAcceptDrops(True)
		self.image_label.image = None
		self.image_label.dragEnterEvent = MethodType(dragEnterEvent,self.image_label)
		self.image_label.dragMoveEvent = MethodType(dragMoveEvent,self.image_label)
		self.image_label.dropEvent = MethodType(dropEvent,self.image_label)
		self.image_label.set_image = MethodType(set_image,self.image_label)
	


	
