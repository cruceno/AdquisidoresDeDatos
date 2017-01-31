# -*- coding: utf-8 -*-
'''
Created on 28 de ene. de 2016

@author: javit

'''
from PyQt4 import QtCore, QtGui
from uiFiles import Ui_SerialConfig, Ui_DatabaseConfig, Ui_ChannelConfig
from db_connector import db
import serial


class SerialConfig(QtGui.QDialog   , Ui_SerialConfig):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self,parent)
        self.setupUi(self)
        fsock=open('db.cfg', 'r')
        datos=fsock.readlines()
        fsock.close()
        self.db_conn=db(datos)
        self.serial_cfg=db.get_serial_config(self.db_conn)
        
        
        # Lista puertos serie y los agrega a los menu de seleccion de puertos
        for i in range ( 50 ):
            try:
                s = serial.Serial( 'COM'+str(i) )
                self.cb_port.addItem( str(s.portstr), str(s.portstr) )
                s.close()
            except:
                pass
                #print  'No se puede comunicar con puerto:',i 
               
        # Selecciona el valor que coincide con la configuracion de la base de datos o deja vacia la selección.
        for i in range(self.cb_port.count()):   
            if self.cb_port.itemData(i)==self.serial_cfg.port:
                self.cb_port.setCurrentIndex(i) 
                break
            else:
                self.cb_port.setCurrentIndex(-1) 
        
        #Lista velocidades validas y las agrega al menu de seleccion    
        for baudrate in serial.SerialBase.BAUDRATES:
            if 2400 <= baudrate and baudrate <= 19200:
                self.cb_baudrate.addItem( str ( baudrate ), str ( baudrate ) )   
        # Selecciona el valor que coincide con la configuracion de la base de datos o deja vacia la selección.
        for i in range(self.cb_baudrate.count()):   
            if self.cb_baudrate.itemData(i)==self.serial_cfg.baudrate:
                self.cb_baudrate.setCurrentIndex(i) 
                break
            else:
                self.cb_baudrate.setCurrentIndex(-1)         
              
        #Lista valoresde paridad validos y los agrega al menu de seleccion        
        self.cb_parity.addItem('None',str(serial.PARITY_NONE))
        self.cb_parity.addItem('Odd',str(serial.PARITY_ODD))
        self.cb_parity.addItem('Even',str(serial.PARITY_EVEN))
        # Selecciona el valor que coincide con la configuracion de la base de datos o deja vacia la selección.
        for i in range(self.cb_parity.count()):   
            if self.cb_parity.itemData(i)==self.serial_cfg.parity:
                self.cb_parity.setCurrentIndex(i) 
                break
            else:
                self.cb_parity.setCurrentIndex(-1) 
        
        #Lista Valores        
        self.cb_stopbits.addItem('1',str(serial.STOPBITS_ONE))
        self.cb_stopbits.addItem('1.5',str(serial.STOPBITS_ONE_POINT_FIVE))  
        self.cb_stopbits.addItem('2',str(serial.STOPBITS_TWO))
        # Selecciona el valor que coincide con la configuracion de la base de datos o deja vacia la selección.
        for i in range(self.cb_stopbits.count()):   
            if self.cb_stopbits.itemData(i)==self.serial_cfg.stopbits:
                self.cb_stopbits.setCurrentIndex(i) 
                break
            else:
                self.cb_stopbits.setCurrentIndex(-1) 
                
        self.cb_bytesize.addItem('8',str(serial.EIGHTBITS))
        self.cb_bytesize.addItem('7',str(serial.SEVENBITS))
        self.cb_bytesize.addItem('6',str(serial.SIXBITS))
        # Selecciona el valor que coincide con la configuracion de la base de datos o deja vacia la selección.
        for i in range(self.cb_bytesize.count()):   
            if self.cb_bytesize.itemData(i)==self.serial_cfg.bytesize:
                self.cb_bytesize.setCurrentIndex(i)
                break
            else:
                self.cb_bytesize.setCurrentIndex(-1)
        self.sb_puntos.setValue(int(self.serial_cfg.puntos))    
                    
    @QtCore.pyqtSlot()    
    def on_pb_accept_pressed(self):
        try:
            
            self.serial_cfg.port=str(self.cb_port.itemData(self.cb_port.currentIndex()).toString())
            self.serial_cfg.baudrate=str(self.cb_baudrate.itemData(self.cb_baudrate.currentIndex()).toString())
            self.serial_cfg.parity=str(self.cb_parity.itemData(self.cb_parity.currentIndex()).toString())
            self.serial_cfg.stopbits=str(self.cb_stopbits.itemData(self.cb_stopbits.currentIndex()).toString())
            self.serial_cfg.bytesize=str(self.cb_bytesize.itemData(self.cb_bytesize.currentIndex()).toString())
            self.serial_cfg.puntos=str(self.sb_puntos.value())
            self.db_conn.update_serial_config(self.serial_cfg)
            self.accept()
            
        except:
            
            self.done(2)
            
    @QtCore.pyqtSlot()
    def on_pb_cancel_pressed(self):
        self.reject()  
    
                
class DatabaseConfig (QtGui.QDialog,Ui_DatabaseConfig):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self,parent)
        self.setupUi(self)

    @QtCore.pyqtSlot()    
    
    def on_pb_accept_pressed(self):
        datos= [str(self.le_server.text()),str(self.le_user.text()), str(self.le_pass.text()), str(self.le_basename.text())]
        self.db_conn=db(datos)
        if self.db_conn.test_db():
            fsock=open('db.cfg','w')
            for line in datos:
                fsock.write(line+'\n')
            fsock.close()
            self.accept()
        else:
            self.lb_info.setText('Datos erroneos. Verifique')
            pass
    @QtCore.pyqtSlot()
    def on_pb_cancel_pressed(self):
        self.reject()      
        
          
class ChannelConfig(QtGui.QDialog,Ui_ChannelConfig ):
    def __init__(self,parent=None):
        
        QtGui.QDialog.__init__(self,parent)
        self.setupUi(self)
        fsock=open('db.cfg', 'r')
        datos=fsock.readlines()
        fsock.close()
        self.db_conn=db(datos)
        
        self.channel_cfg=self.db_conn.get_channel_info()
        
        for i in range(1,9,1):
            if not self.channel_cfg.__getattribute__('C'+str(i))[2]:
                self.__getattribute__('le_ch'+str(i)+'_model').setText(self.channel_cfg.__getattribute__('C'+str(i))[0])
                self.__getattribute__('pte_ch'+str(i)+'_description').setPlainText(self.channel_cfg.__getattribute__('C'+str(i))[1])
                self.__getattribute__('le_ch'+str(i)+'_model').setEnabled(False)
                self.__getattribute__('pte_ch'+str(i)+'_description').setEnabled(False)
            else:
                self.__getattribute__('chx_channel_'+str(i)).setChecked(True)
                self.__getattribute__('le_ch'+str(i)+'_model').setText(self.channel_cfg.__getattribute__('C'+str(i))[0])
                self.__getattribute__('pte_ch'+str(i)+'_description').setPlainText(self.channel_cfg.__getattribute__('C'+str(i))[1])

    @QtCore.pyqtSlot()
    def on_chx_channel_1_clicked(self):
        if self.chx_channel_1.isChecked():
            self.le_ch1_model.setEnabled(True)
            self.pte_ch1_description.setEnabled(True)
        else:
            self.le_ch1_model.setEnabled(False)
            self.pte_ch1_description.setEnabled(False)
    
    @QtCore.pyqtSlot()
    def on_chx_channel_2_clicked(self):
        if self.chx_channel_2.isChecked():
            self.le_ch2_model.setEnabled(True)
            self.pte_ch2_description.setEnabled(True)
        else:
            self.le_ch2_model.setEnabled(False)
            self.pte_ch2_description.setEnabled(False)
    
    @QtCore.pyqtSlot()
    def on_chx_channel_3_clicked(self):
        if self.chx_channel_3.isChecked():
            self.le_ch3_model.setEnabled(True)
            self.pte_ch3_description.setEnabled(True)
        else:
            self.le_ch3_model.setEnabled(False)
            self.pte_ch3_description.setEnabled(False)
    
    @QtCore.pyqtSlot()
    def on_chx_channel_4_clicked(self):
        if self.chx_channel_4.isChecked():
            self.le_ch4_model.setEnabled(True)
            self.pte_ch4_description.setEnabled(True)
        else:
            self.le_ch4_model.setEnabled(False)
            self.pte_ch4_description.setEnabled(False)
    
    @QtCore.pyqtSlot()
    def on_chx_channel_5_clicked(self):
        if self.chx_channel_5.isChecked():
            self.le_ch5_model.setEnabled(True)
            self.pte_ch5_description.setEnabled(True)
        else:
            self.le_ch5_model.setEnabled(False)
            self.pte_ch5_description.setEnabled(False)
            
    @QtCore.pyqtSlot()
    def on_chx_channel_6_clicked(self):
        if self.chx_channel_6.isChecked():
            self.le_ch6_model.setEnabled(True)
            self.pte_ch6_description.setEnabled(True)
        else:
            self.le_ch6_model.setEnabled(False)
            self.pte_ch6_description.setEnabled(False)
            
    @QtCore.pyqtSlot()
    def on_chx_channel_7_clicked(self):
        if self.chx_channel_7.isChecked():
            self.le_ch7_model.setEnabled(True)
            self.pte_ch7_description.setEnabled(True)
        else:
            self.le_ch7_model.setEnabled(False)
            self.pte_ch7_description.setEnabled(False)
            
    @QtCore.pyqtSlot()
    def on_chx_channel_8_clicked(self):
        if self.chx_channel_8.isChecked():
            self.le_ch8_model.setEnabled(True)
            self.pte_ch8_description.setEnabled(True)
        else:
            self.le_ch8_model.setEnabled(False)
            self.pte_ch8_description.setEnabled(False)
            
    @QtCore.pyqtSlot()    
    def on_pb_accept_pressed(self):
        
        try:
            
            for i in range(1,9,1):
                self.channel_cfg.__setattr__('C'+str(i),
                                                [str(self.__getattribute__('le_ch'+str(i)+'_model').text()),
                                                 str(self.__getattribute__('pte_ch'+str(i)+'_description').toPlainText()),
                                                 int(self.__getattribute__('chx_channel_'+str(i)).isChecked())
                                                ]
                                             )
            self.db_conn.update_channel_info(self.channel_cfg)
            self.accept()
            
        except:
            self.done(2)
        
    @QtCore.pyqtSlot()
    def on_pb_cancel_pressed(self):
        self.reject()  