# -*- coding: utf-8 -*-
'''
Created on 28 de ene. de 2016
@author: javit
'''
from PyQt4 import QtCore, QtGui
import sys, time
from uiFiles import Ui_AtmosfMainAdq
from config import SerialConfig, DatabaseConfig, ChannelConfig
from db_connector import db, Registro
from datetime import datetime

class ADcom(QtCore.QObject):
    
    def __init__(self,parent=None):
        QtCore.QObject.__init__(self, parent)
        self.exiting = True
        self.error=False
        try:
            fsock=open('db.cfg', 'r')
            datos=fsock.readlines()
            fsock.close()
        except:

            msg='['+str(datetime.now())+'] - Proceso detenido con errores, No se puede acceder al archivo db.cfg, corrija los errores para volver a iniciar.'
            self.emit(QtCore.SIGNAL ( 'msg(PyQt_PyObject)'),msg)
            self.error=True
            
        try:
            self.db_conn=db(datos)
        except:
            msg='['+str(datetime.now())+'] - Proceso detenido con errores, No se puede establecer la conexion con la base de datos. Revise la configuracion, corrija los errores para volver a iniciar.'
            self.emit(QtCore.SIGNAL ( 'msg(PyQt_PyObject)'),msg)
            self.error=True
            
    @QtCore.pyqtSlot()
    def launch(self):
        if not self.error:
            #importar serial de PySerial
            import serial
            # Obtener configuracion del puerto serie almacenada en la base de datos
            self.serial_cfg=db.get_serial_config(self.db_conn)
    
            try:
                #inicializar puerto serie con la configuracion obtenida
                self.ser = serial.Serial( port     = self.serial_cfg.port,
                                          baudrate = int(self.serial_cfg.baudrate),
                                          parity   = self.serial_cfg.parity,
                                          stopbits = int(self.serial_cfg.stopbits),
                                          bytesize = int(self.serial_cfg.bytesize),
                                          timeout  = 2
                                          )
                self.ser.close()
                
            except serial.SerialException:
                
                self.emit(QtCore.SIGNAL ( 'msg(PyQt_PyObject)'),'['+str(datetime.now())+'] - No se pudo establecer la conexion con el puerto:%s'%self.serial_cfg.port)
                self.error=True
                time.sleep(1)
                self.emit( QtCore.SIGNAL ( "finished()" ))
                return False
            
            self.ser.open()
            # Establecer tiempo de espera en segundos entre medicion y medicion,
            # utilizado para establecer la cantidad de datos almacenados por el software.
            
            self.delay=60/int(self.serial_cfg.puntos)            
            self.emit(QtCore.SIGNAL ( 'msg(PyQt_PyObject)'),'['+str(datetime.now())+'] - Entrando en bucle de adquisicion')
            
            while not self.exiting:
                self.ser.read(self.ser.in_waiting)
                data=[]
                
                self.ser.readline() # Se deacarta primer linea para evitar un dato truncado
                i=range(0,8,1)  
                for i in i:         # se leen 8 lineas consecutivas (1 por canal)
                    
                    data.append( self.ser.readline())
                    
                self.emit( QtCore.SIGNAL ( "readsignal(PyQt_PyObject)" ), data )
                for i in range(1,21,1):
                    time.sleep(self.delay/20) 
                    self.emit( QtCore.SIGNAL ( "pbar(PyQt_PyObject)" ), i*5 )
    
            self.ser.close()
            self.emit(QtCore.SIGNAL ( 'msg(PyQt_PyObject)'),'['+str(datetime.now())+'] - Finalizando proceso de adquisicion')
            msg='['+str(datetime.now())+'] - Proceso detenido correctamete, presione StartAdq para volver a iniciar.'
            self.emit(QtCore.SIGNAL ( 'msg(PyQt_PyObject)'),msg)
            self.emit( QtCore.SIGNAL ( "pbar(PyQt_PyObject)" ), 0 )
            time.sleep(1)
            self.emit( QtCore.SIGNAL ( "finished()" ))
        else:
            self.emit( QtCore.SIGNAL ( "pbar(PyQt_PyObject)" ), 0 )
            time.sleep(1)
            self.emit( QtCore.SIGNAL ( "finished()" ))
        
        
class AtmosfMainAdq(QtGui.QMainWindow, Ui_AtmosfMainAdq):
    def __init__(self,parent=None):
        
        QtGui.QMainWindow.__init__(self,parent)
        self.setupUi(self)
        try:
            fsock=open('db.cfg', 'r')
            datos=fsock.readlines()
            fsock.close()
        except:
            self.pte_logmon.setPlainText('No se puede acceder al archivo db.cfg')
        try:
            self.db_conn=db(datos)
        except:
            self.pte_logmon.setPlainText('No se puede establecer la conexion con la base de datos. Revise la configuracion')
        
        self.action_serial.triggered.connect(self.action_serial_triggered)
        self.action_database.triggered.connect(self.action_database_triggered)
        self.action_configchannels.triggered.connect(self.action_configchannels_triggered)
        
    def init_AD(self):
        
        self.adq=ADcom()
        
        self.connect( self.adq, QtCore.SIGNAL ( "readsignal(PyQt_PyObject)" ), self.save_data )
        self.connect( self.adq, QtCore.SIGNAL ('msg(PyQt_PyObject)'),self.update_log)
        self.connect( self.adq, QtCore.SIGNAL ( "pbar(PyQt_PyObject)" ), self.update_bar )
        
        self.thread=QtCore.QThread()
        self.thread.started.connect(self.adq.launch)
        self.connect( self.adq, QtCore.SIGNAL ( "finished()" ), self.thread.quit )
        
        self.adq.moveToThread(self.thread)
            
    @QtCore.pyqtSlot()
    def action_serial_triggered(self):
        
        dlg_serial=SerialConfig(self)
        dlg_result=dlg_serial.exec_()
        
        if dlg_result ==1:
            self.pte_logmon.setPlainText('['+str(datetime.now())+'] - Conexion con dispositivo configurada correctamente')
        else: 
            pass
        
    @QtCore.pyqtSlot()
    def action_database_triggered(self):
        
        dlg_serial=DatabaseConfig(self)
        dlg_result=dlg_serial.exec_()
        
        if dlg_result ==1:
            self.pte_logmon.setPlainText('['+str(datetime.now())+'] - Conexion con servidor configurada correctamente')
        else: 
            pass
        
    @QtCore.pyqtSlot()
    def action_configchannels_triggered(self):
        
        dlg=ChannelConfig(self)
        dlg_result=dlg.exec_()
        
        if dlg_result ==1:
            self.pte_logmon.setPlainText('['+str(datetime.now())+'] - Canales configurados correctamente')
        else: 
            pass
    
    def on_clb_startadq_pressed(self):
        self.init_AD()
        time.sleep(1)
        if self.adq.exiting:
            self.pte_logmon.clear()
            self.pte_logmon.setPlainText('Iniciando proceso . . .')
            self.adq.exiting=False
            self.thread.start()
            while not self.thread.isRunning():
                continue
            time.sleep(2)
            msj="Estado del Adquisidor: Iniciado\n"
            msj+="Fecha de inicio: "+str(datetime.now())+"\n"
            msj+="Intervalo de adquisicion: "+str(self.adq.serial_cfg.puntos)+' puntos por minuto\n'
            msj+="Puerto utilizado: "+str(self.adq.serial_cfg.port)+'\n'
            msj+="Servidor de la base de datos: "+self.db_conn.datos[0]+'\n'
            msj+="Base utilizada: "+self.db_conn.datos[3]+'\n'
            msj+="--------------------------------------------------------------------------------------------------------------------------"
            self.pte_config.setPlainText(msj)
  
        else:
            msj= '['+str(datetime.now())+'] - El proceso de adquisición ya fue iniciado'
    def on_clb_stopadq_pressed(self):
        self.adq.exiting=True
    @QtCore.pyqtSlot()
    def update_log(self,msj):
        self.pte_logmon.setPlainText(str(self.pte_logmon.toPlainText())+'\n'+str(msj))
    @QtCore.pyqtSlot()
    def update_bar(self, val):
        self.progressBar.setValue(val)
    @QtCore.pyqtSlot()
    def save_data(self,data):
        channel_cfg = self.db_conn.get_channel_info()
        registro=Registro()
        for dato in data:
            channel, val, unit= dato.split('  ')
            if channel_cfg.__getattribute__(channel)[2]:
                registro.__setattr__(channel, val)
            else:
                registro.__setattr__(channel,0.0)
        registro.__setattr__('datetime',datetime.now())
        self.db_conn.insert_data(registro)
        self.update_log('[Registro guardado correctamente] - '+str(registro.datetime))
        self.update_bar(0)
        
def main():
    app = QtGui.QApplication( sys.argv )
    DAQ = AtmosfMainAdq()
    DAQ.show()
    sys.exit( app.exec_() )

if __name__ == '__main__':
    main()