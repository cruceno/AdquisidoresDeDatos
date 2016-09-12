# -*- coding: utf-8 -*-
'''
Created on 17/10/2013

@author: Cruceno Javier
    
'''
# Importar librerias necesarias
# interfaz grafica
from PyQt4 import QtCore, QtGui, uic

# Comunicacion con sistema y manejo de puerto serie
import os, sys, time

# Importar librerias para manejo de protocolos VISA
from pyvisa.vpp43 import visa_library
visa_library.load_library( "visa32.dll" )
import visa

import UniversalLibrary as UL

from StringIO import StringIO

# Manejo numerico de datos
import numpy as np

# Librerias para graficar en el ploter
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


# Clase que configura parte de las graficas de datos -----------------------------
class canvas( FigureCanvas ):

    def __init__( self, parent ):
        # Se instancia el objeto figure
        self.fig = Figure()
        # Se define la grafica en coordenadas polares
        self.axes = self.fig.add_subplot( 111 )

        # Se define una grilla
        self.axes.grid( True )

        # se inicializa FigureCanvas
        FigureCanvas.__init__( self, self.fig )
        # se define el widget padre
        self.setParent( parent )
        # se define el widget como expandible
        FigureCanvas.setSizePolicy( self,
                QtGui.QSizePolicy.Expanding,
                QtGui.QSizePolicy.Expanding )
        # se notifica al sistema de la actualizacion
        # de la politica
        FigureCanvas.updateGeometry( self )
        self.fig.canvas.draw()


# Clase que define el subproceso que va a realizar la adquisicion de datos-------------
class Test_Ciclotermico ( QtCore.QThread ):
    def __init__ ( self ):
        QtCore.QThread.__init__( self )

        self.exiting = False
    def test ( self,
               outfile,
#                s_port,
               multimeter,
               usb_temp_ai_temp_channels,
               usb_temp_ai_volt_channels,
               data_per_second,
               BoardNum ):

#         if s_port:
#             self.ser = serial.Serial( port = s_port,
#                               baudrate = 9600,
#                               parity = serial.PARITY_NONE,
#                               stopbits = 1,
#                               bytesize = 8,
#                               timeout = 2 )
#         print 'Archivo de salida:', outfile
#         print 'Multimetro:', multimeter
#         print 'Canales de temperatura en USB TEMP AI:', usb_temp_ai_temp_channels
#         print 'Canales de voltage en USB TEMP AI:', usb_temp_ai_volt_channels
#         print 'Datos por segundo', data_per_second
#         print 'Board Num:', BoardNum
        print 'inicio test'
        if multimeter:
            print 'comunico con multimetro'
            self.multimeter = visa.instrument( multimeter )
            print 'comunicado. Configuro mult.'
            print 'Reset'
            self.multimeter.write( '*RST' )
            time.sleep( 0.5 )
            print 'CONF'
            self.multimeter.write( 'CONF:VOLT:DC AUTO' )
            time.sleep( 0.5 )
            self.time_stamp = 0
        else:
            print 'no uso multimetro'
            self.multimeter = multimeter
            
        self.delay = 1. / ( float ( data_per_second ) * ( len ( usb_temp_ai_temp_channels ) + len ( usb_temp_ai_volt_channels ) ) )
        self.refresh = data_per_second
        self.BoardNum = BoardNum
        self.TempChannels = usb_temp_ai_temp_channels
        print self.TempChannels
        self.VoltChannels = usb_temp_ai_volt_channels
        print self.VoltChannels
        self.savedata = False
        self.outfile = outfile
        self.zero_time=0
        self.zero_ext=False
        self.zero_extensometer = 0
        self.zero_load=False
        self.zero_loadcell = 0
        self.start()

    def run ( self ):
        print 'corriendo'
        first = True
        TempVal = 0.0
        VoltVal = 0.0
        self.zero_time = time.time()
        count =0
        
        while not self.exiting:

            #===================================================================
            # Lectura del dispositivo USB-TEMP-IA
            #===================================================================

            TempRead = []
            VoltRead = []
            print 'leyendo bichito azul'
            for c in self.TempChannels:

                TempRead.append ( UL.cbTIn( self.BoardNum,
                                c,
                                UL.CELSIUS ,
                                TempVal,
                                UL.FILTER ) )
                time.sleep( self.delay )

            for c in self.VoltChannels:
                VoltRead.append ( UL.cbVIn( self.BoardNum,
                                            c,
                                            UL.cbGetConfig( UL.BOARDINFO,
                                                            self.BoardNum,
                                                            c,
                                                            UL.BIRANGE,
                                                            ConfigVal = 0 ),
                                            VoltVal,
                                            Option = None ) )
                time.sleep( self.delay )
            #==================================================================
            
            if self.multimeter:

                print 'tomo lecturas del multimetro'
                #self.multimeter.write( 'DISP:WIND2:TEXT "Midiendo ..."' )
                self.multimeter.write('READ?')
                time.sleep(0.02)
                X = self.multimeter.read()
                temp_data = float (X) * 1000
                # Polinomio para rango intermedio  -272 a 150 C
                print 'Polinomio de temp.'
                if temp_data < 2: 
                    
                    Y = 25.39459 * temp_data 
                    Y-= 0.44494 * temp_data ** 2 
                    Y+= 0.05652 * temp_data ** 3 
                    Y-= 0.00412 * temp_data ** 4 
                    Y+= 0.0011 * temp_data ** 5 
                    Y-= 1.39776E-4 * temp_data ** 6 
                    Y+= 4.40583E-6 * temp_data ** 7 
                    Y+= 7.709E-8 * temp_data ** 8
                    
                #Polinomio para rango positivo 0 a 500 C     
                if temp_data >=2 :
                    
                    Y = 25.26032 * temp_data
                    Y-= 0.57128 * temp_data ** 2
                    Y+= 0.13393 * temp_data ** 3
                    Y-= 0.01411 * temp_data ** 4
                    Y+= 7.7329E-4 * temp_data ** 5
                    Y-= 2.32438E-5 * temp_data ** 6
                    Y+= 3.64924E-7 * temp_data ** 7
                    Y-= 2.34283E-9 * temp_data ** 8

                temp_sample=Y
                temp_down = TempRead[0]
                temp_up = TempRead[1]
                
            else:
                temp_down = TempRead[0]
                temp_sample = TempRead[1]
                temp_up = TempRead[2]
                
            #======================================================================
            # Valor del extensometro
            #======================================================================

##            if self.zero_ext:
##                self.zero_extensometer=VoltRead[0]/10
##                self.zero_ext=False
##                self.emit( QtCore.SIGNAL ( "ext_zero(PyQt_PyObject)" ), self.zero_extensometer )
            
            extensometer = VoltRead[0]/10

            #======================================================================
            
            #======================================================================
            # Valor de la celda de carga
            #======================================================================
##            if self.zero_load:
##                self.zero_loadcell=VoltRead[1]*5
##                self.zero_load=False
##                self.emit( QtCore.SIGNAL ( "load_zero(PyQt_PyObject)" ), self.zero_loadcell*2 )
                
            loadcell = VoltRead[1]*5 
            #======================================================================
            
            timestamp = time.time() - self.zero_time

#           Creando variable (lista) para almacenar datos en un archivo

            data = [timestamp, 
                    temp_down, 
                    temp_sample, 
                    temp_up , 
                    extensometer, 
                    loadcell]

            #===================================================================
            # Guardando datos en disco duro
            #===================================================================
            if self.savedata:
                
                if first:
                    fsock = open( self.outfile, 'w' )
                    first = False
                else:
                    fsock = open( self.outfile, 'a' )
                    
                #if self.multimeter:
                 #   self.multimeter.write( 'DISP:WIND2:TEXT "Guardando..."' )
                    
                line = str ( data[0] ) + '\t' 
                line+= str ( data[1] ) + '\t' 
                line+= str ( data[2] ) + '\t' 
                line+= str ( data[3] ) + '\t' 
                line+= str ( data[4] ) + '\t' 
                line+= str ( data[5] ) + '\n'
                
                fsock.write( line )
                fsock.close()
            #====================================================================
            else:
                
                tempfsock = open( 'tempdata', 'w' )
                
                line = str ( data[0] ) + '\t' 
                line+= str ( data[1] ) + '\t' 
                line+= str ( data[2] ) + '\t' 
                line+= str ( data[3] ) + '\t' 
                line+= str ( data[4] ) + '\t' 
                line+= str ( data[5] ) + '\n'
                
                tempfsock.write( line )
                tempfsock.close()            
            
#             print 'Emitiendo se�al a main..'
            if count == self.refresh:
                
                self.emit( QtCore.SIGNAL ( "ready(PyQt_PyObject)" ), data )
                count = 0
            count+=1
        #if self.multimeter:
            #self.multimeter.write( 'DISP:WIND2:TEXT:CLEAR' )
            
        tempfsock.close() 
        fsock.close()
        self.exit()

    def __del__( self ):
        #if self.multimeter:
            #self.multimeter.write( 'DISP:WIND2:TEXT:CLEAR' )
        self.exiting = True
        self.ser.close()
        self.wait()
        
class Main( QtGui.QMainWindow ):

    def __init__( self ):

        #Inicializamos interfaz graica---------------------------
        QtGui.QMainWindow.__init__( self )

        uic.loadUi( 'CiclotermicoUI.ui', self )
        #---------------------------------------------------------------------------

        #Generamos los planos donde graficaremos los datos--------------------------
        # Inicializando base de ploteo para mainplot--------------------------------
        self.vbl_main = QtGui.QVBoxLayout( self.gb_mainplot )
        self.maincanvas = canvas( self.gb_mainplot )
        self.vbl_main.insertWidget( 0, self.maincanvas )
        #--------------------------------------------------------------------------
        # Inicializando base de ploteo para auxplot_1------------------------------
        self.vbl_aux_1 = QtGui.QVBoxLayout( self.gb_auxplot_1 )
        self.auxcanvas_1 = canvas( self.gb_auxplot_1 )
        self.vbl_aux_1.insertWidget( 0, self.auxcanvas_1 )
        #--------------------------------------------------------------------------
        # Inicializando base de ploteo para auxplot_2------------------------------
        self.vbl_aux_2 = QtGui.QVBoxLayout( self.gb_auxplot_2 )
        self.auxcanvas_2 = canvas( self.gb_auxplot_2 )
        self.vbl_aux_2.insertWidget( 0, self.auxcanvas_2 )
        #--------------------------------------------------------------------------

        #Trhead de lectura de datos-------------------------------------------------------------------------------
        self.ciclotermico = Test_Ciclotermico()
        self.read_data = False
        self.zero_extensometro=False
        #====================================================================
        # Conectamos seniales de los threads con funciones de manejo de datos

        self.connect(self.ciclotermico,
                     QtCore.SIGNAL("ready(PyQt_PyObject)" ),
                     self.show_data)

##        self.connect(self.ciclotermico,
##                     QtCore.SIGNAL("ext_zero(PyQt_PyObject)" ),
##                     self.zeroext)
##        
##        self.connect(self.ciclotermico, 
##                     QtCore.SIGNAL("load_zero(PyQt_PyObject)" ),
##                     self.zeroload)
        
        #=======================================================================

    #===========================================================================================
    # Las siguientes 4 funciones son las encargadas de ajustar la escala de la grafica principal
    # por medio de los controles proporcionados al usuario
    
    @QtCore.pyqtSlot()
    def on_sb_xmin_valueChanged( self ):
        self.maincanvas.axes.set_xlim( self.sb_xmin.value(), self.sb_xmax.value() )
        self.maincanvas.draw()
        
    @QtCore.pyqtSlot( int )
    def on_sb_xmax_valueChanged( self ):
        self.maincanvas.axes.set_xlim( self.sb_xmin.value(), self.sb_xmax.value() )
        self.maincanvas.draw()
        
    @QtCore.pyqtSlot( int )
    def on_sb_ymin_valueChanged( self ):
        self.maincanvas.axes.set_ylim( self.sb_ymin.value(), self.sb_ymax.value() )
        self.maincanvas.draw()
        
    @QtCore.pyqtSlot( int )
    def on_sb_ymax_valueChanged( self ):
        self.maincanvas.axes.set_ylim( self.sb_ymin.value(), self.sb_ymax.value() )
        self.maincanvas.draw()    
    #============================================================================================

#===============================================================================
# Funciones de los botones accionados por el usuario para controlar el inicio y el final
# del ensayo
#===============================================================================
    @QtCore.pyqtSlot()
    def on_pb_start_clicked ( self ):
        self.Ciclotermico_test()
        self.pb_start.setEnabled( False )
        self.pb_start_save_data.setEnabled(True)
    
    @QtCore.pyqtSlot()
    def on_pb_end_clicked ( self ):
        self.ciclotermico.exiting = True
        while self.ciclotermico.isRunning():
            continue
        footer = self.ptx_footer.toPlainText() + '\n'
        self.comented_footer = ''
        for line in footer.split( '\n' ):
            self.comented_footer = self.comented_footer + self.le_output_file_commentchar.text() + line + '\n'


        f = open( self.le_output_file_path.text() + '.txt' )
        s = self.comented_header + f.read() + self.comented_footer
        f.close()

        f = open( self.le_output_file_path.text() + '.txt', 'w' )
        f.write( s )
        f.close()
        self.pb_end.setEnabled(False)
        self.pb_start.setEnabled( True )
        self.pb_start_save_data.setEnabled( False )

    @QtCore.pyqtSlot ()
    def on_pb_start_save_data_clicked ( self ):
        self.ciclotermico.zero_time = time.time()
        self.maincanvas.axes.cla()
        self.maincanvas.axes.grid( True )
        self.auxcanvas_2.axes.cla()
        self.auxcanvas_2.axes.grid( True )
        self.auxcanvas_1.axes.cla()
        self.auxcanvas_1.axes.grid( True )
        self.ciclotermico.savedata = True
        self.read_data = True
    
    @QtCore.pyqtSlot()
    def on_pb_zero_clicked ( self ):
##        self.ciclotermico.zero_ext=True
##        self.ciclotermico.zero_load=True
##        self.ciclotermico.zero_time=time.time()
###         self.pb_zero.setEnabled( False )
##        self.pb_start_save_data.setEnabled( True )
        if self.read_data:
            
            f = open( self.le_output_file_path.text() + '.txt' )
            s = StringIO( f.read() )
            f.close()
            s.seek( 0 )

            extensometro = np.genfromtxt(   s,
                                            usecols = ( 4 ),
                                            deletechars = "\n",
                                            dtype = float,
                                            autostrip = True,
                                            unpack = True )
            self.zero_extensometro=extensometro[-1]
            print self.zero_extensometro
            
        else:
            f = open( 'tempdata' )
            s = StringIO( f.read() )
            f.close()
            s.seek( 0 )

            data = np.genfromtxt( s,
##                                usecols = ( 0, 1, 2, 3, 4, 5 ),
                                  deletechars = "\n",
                                  dtype = float,
                                  autostrip = True,
                                  unpack = True )
        
            self.zero_extensometro=data[4]
            print self.zero_extensometro
            
    @QtCore.pyqtSlot()
    def on_tlb_output_file_path_pressed( self ):
        # seleccionar archivo
        self.le_output_file_path.setText( QtGui.QFileDialog.getSaveFileName( parent = None ) )

##    @QtCore.pyqtSlot()
##    def zeroext(self,extensometer):
##        text=self.ptx_footer.toPlainText() 
##        text = 'Valor del exensometro al tarar (mm): ' + str ( extensometer ) + '\n'
##        self.ptx_footer.setPlainText( text )
##        
##    @QtCore.pyqtSlot()
##    def zeroload(self,loadcell):
##        text=self.ptx_footer.toPlainText()       
##        text += 'Valor de la celda de carga al tarar (Kgf): ' + str ( loadcell) + '\n'
##        self.ptx_footer.setPlainText( text )

    def Ciclotermico_test ( self ):
        # inicializar archivos leer configuraciones inicializar puerto serie
        valid = False
        if self.cbx_temperature_sample_input.currentText() == 'AG_34410A':
            i = self.cbx_temperature_sample_channel.count()
            while -1 < i:
                self.cbx_temperature_sample_channel.removeItem( i )
                i -= 1
            self.cbx_temperature_sample_channel.addItem( 'USB0::2391::1560::my50279055::0', 'USB0::2391::1560::my50279055::0' )
        if self.cbx_temperature_up_channel.currentText() != self.cbx_temperature_sample_channel.currentText():
            if self.cbx_temperature_up_channel.currentText() != self.cbx_temperature_down_channel.currentText():
                if self.cbx_temperature_down_channel.currentText() != self.cbx_temperature_sample_channel.currentText():
                    if self.cbx_extensometer_channel.currentText() != self.cbx_loadcell_channel.currentText():
                        if self.le_output_file_path.text() != '':
                            valid = True
                        else:
                            self.statusBar().showMessage( 'El campo que indica el archivo de destino no puede estar vacio' )
                            self.pb_start.setEnabled( True )
                    else:
                        self.pb_start.setEnabled( True )
                        self.statusBar().showMessage( 'El canal de entrada del extensometro no puede ser igual al de la celda de carga' )
                else:
                    self.pb_start.setEnabled( True )
                    self.statusBar().showMessage( 'El canal de temperatura inferior debe ser distinto que el canal de temperatura muestra' )
            else:
                self.pb_start.setEnabled( True )
                self.statusBar().showMessage( 'El canal de temperatura inferior debe ser distinto que el canal de temperatura superior' )
        else:
            self.pb_start.setEnabled( True )
            self.statusBar().showMessage( 'El canal de temperatura superior debe ser distinto que el canal de temperatura muestra' )

        if valid:
            self.pb_start.setEnabled( False )
            outfile = self.le_output_file_path.text()
            outfile += '.txt'
            header = 'Comentarios:' + self.ptx_header.toPlainText() + '\n'
            header += 'Largo de la muestra: ' + str ( self.dsbx_sample_heigth.value() ) + '\n'
            header += 'Ancho de la muestra: ' + str ( self.dsbx_sample_width.value() ) + '\n'
            header += 'Espesor de la muestra: ' + str ( self.dsbx_sample_thickness.value() ) + '\n'
            header += 'Dispositivos y canales utilizados: \n'
            header += '\t Temperatura de la superior: ' + str ( self.cbx_temperature_up_input.currentText() ) + '\n'
            header += '\t\tCanal: ' + str( self.cbx_temperature_up_channel.currentText() ) + '\n'
            header += '\t Temperatura de la muestra: ' + str ( self.cbx_temperature_sample_input.currentText() ) + '\n'
            header += '\t\t Canal: ' + str ( self.cbx_temperature_sample_channel.currentText() ) + '\n'
            header += '\t Temperatura inferior: ' + str ( self.cbx_temperature_down_input.currentText() ) + '\n'
            header += '\t\t Canal: ' + str ( self.cbx_temperature_down_channel.currentText() ) + '\n'
            header += '\t Extensometro: ' + str ( self.cbx_extensometer_input.currentText() ) + '\n'
            header += '\t\t Canal: ' + str ( self.cbx_extensometer_channel.currentText() ) + '\n'
            header += '\t Celda de carga: ' + str ( self.cbx_loadcell_input.currentText() ) + '\n'
            header += '\t\t Canal: ' + str ( self.cbx_loadcell_channel.currentText() ) + '\n'
            header += '\n Datos por segundo: ' + str ( self.sb_data_per_second.value() ) + '\n\n'
            header += 'Tiempo \t Temperarura inferior \t Temperatura de la muestra \t Temperatura superior \t Extensometro \t Celda de carga \n'

            self.comented_header = ''
            for line in header.split( '\n' ):
                self.comented_header = self.comented_header + self.le_output_file_commentchar.text() + line + '\n'


            if self.cbx_temperature_sample_input.currentText() != 'USB TEMP AI':

                multimeter = 'USB0::2391::1560::my50279055::0'
                usb_temp_ai_temp_channels = [int ( self.cbx_temperature_down_channel.currentText() ),
                                           int ( self.cbx_temperature_up_channel.currentText() ) ]
            else:
                multimeter = False
                usb_temp_ai_temp_channels = [int ( self.cbx_temperature_down_channel.currentText() ),
                                           int ( self.cbx_temperature_sample_channel.currentText() ),
                                           int ( self.cbx_temperature_up_channel.currentText() )]

            usb_temp_ai_volt_channels = [int ( self.cbx_extensometer_channel.currentText() ),
                                       int ( self.cbx_loadcell_channel.currentText() )]

            self.ciclotermico.test( outfile,
#                                     s_port
                                    multimeter,
                                    usb_temp_ai_temp_channels,
                                    usb_temp_ai_volt_channels,
                                    self.sb_data_per_second.value(),
                                    self.sb_board_num.value() )
            self.count = 0
            self.pb_zero.setEnabled( True )
            self.pb_end.setEnabled( True )

    @QtCore.pyqtSlot ()
    
    def show_data ( self, data ):
        del data
        if self.read_data:
            
            f = open( self.le_output_file_path.text() + '.txt' )
            s = StringIO( f.read() )
            f.close()
            s.seek( 0 )

            time_np, temp_down, temp_sample, temp_up, extensometer, loadcell = np.genfromtxt(   s,
                                                                                                usecols = ( 0, 1, 2, 3, 4, 5 ),
                                                                                                deletechars = "\n",
                                                                                                dtype = float,
                                                                                                autostrip = True,
                                                                                                unpack = True )
            if time_np[-1] < 60:
                self.lcd_time_second.display( str ( int (time_np[-1] ) ) )
            else:
                m = time_np[-1] // 60
                s = time_np[-1] % 60
                if m < 60:
                    self.lcd_time_second.display( str ( int ( s ) ) )
                    self.lcd_time_minute.display( str ( int ( m ) ) )
                else:
                    h = m // 60
                    m = m % 60
                    self.lcd_time_second.display( str ( int ( s ) ) )
                    self.lcd_time_minute.display( str ( int ( m ) ) )
                    self.lcd_time_hour.display( str ( int ( h ) ) )

            if self.zero_extensometro:    

                self.lcd_var_2.display( str (round (((float(extensometer[-1])-float(self.zero_extensometro) ) / float(self.dsbx_sample_heigth.value())) *100 , 4) ) )
            else:
                self.lcd_var_2.display( str ( ( float ( extensometer[-1] ) / float ( self.dsbx_sample_heigth.value() ) ) * 100) )

            self.lcd_var_5.display( str(float ( extensometer[-1] )))
            self.lcd_var_1.display( str ( float ( loadcell[-1] )*9.8 / ( float ( self.dsbx_sample_width.value() ) * float ( self.dsbx_sample_thickness.value() ) ) ) )
            self.lcd_var_3.display( str ( loadcell[-1] ) )
##==============================IMPORTANTE !!!!=========================================
##======================================================================================
## MODIFICA j PARA CAMBIAR CANTIDAD DE PUNTOS USADOS PARA EL CALCULO DE VELOCIDAD           
##======================================================================================
##======================================================================================
            j=50 * self.sb_data_per_second.value()
##======================================================================================
##======================================================================================
            if np.size( temp_sample) >= j:
           
                temp_a=np.polyfit(time_np[j*(-1):-1]/60, temp_sample[j*-1:-1],1)[0]
                self.lcd_var_4.display( str ( temp_a ) )
                
            self.lcd_temperature_up.display( str ( temp_up[-1] ) )
            self.lcd_temperature_sample.display( str ( temp_sample[-1] ) )
            self.lcd_temperature_down.display( str ( temp_down[-1] ) )
            
            # Ploteando en los canvas ya definidos con las funciones heredadas de la clase canvas
            # Deformacion en funcion de temperatura
            self.maincanvas.axes.cla()
            self.maincanvas.axes.grid( True )
            self.statusBar().showMessage( 'Ploteando principal...' )
            self.maincanvas.axes.set_xlim( self.sb_xmin.value(), self.sb_xmax.value() )
            self.maincanvas.axes.set_ylim( self.sb_ymin.value(), self.sb_ymax.value() )            
            self.maincanvas.axes.plot( temp_sample, extensometer, 'og' )
            
            for label in self.maincanvas.axes.get_xticklabels():
                # label is a Text instance
                label.set_rotation ( 45 )
            self.maincanvas.fig.canvas.draw()
            min5=300*self.sb_data_per_second.value()

            if np.size( time_np ) < min5:
                temp_range = np.array( [np.min( temp_down ),
                                     np.min( temp_sample ),
                                     np.min( temp_up ),
                                     np.max( temp_down ),
                                     np.max( temp_sample ),
                                     np.max( temp_up )] )

                # Temperatura en funcion de tiempo
                self.auxcanvas_2.axes.cla()
                self.auxcanvas_2.axes.grid( True )
                self.statusBar().showMessage( 'Ploteando Auxiliar 2...' )
                self.auxcanvas_2.axes.set_xlim( time_np[0], time_np[-1] )
                self.auxcanvas_2.axes.set_ylim( np.min( temp_range ) - abs (np.min( temp_range )) * 20 / 100,
                                                np.max( temp_range ) + abs (np.max( temp_range )) * 20 / 100 )
                
                self.auxcanvas_2.axes.plot( time_np, temp_down, 'b',
                                            time_np, temp_sample, 'r',
                                            time_np, temp_up, 'g' )
                
                for label in self.auxcanvas_2.axes.get_xticklabels():
                    # label is a Text instance
                    label.set_visible( False )
                self.auxcanvas_2.fig.canvas.draw()

                # Deformacion en funcion de tiempo
                self.auxcanvas_1.axes.cla()
                self.auxcanvas_1.axes.grid( True )
                self.statusBar().showMessage( 'Ploteando Auxiliar 1...' )
                self.auxcanvas_1.axes.set_xlim( time_np[0], time_np[-1] )
                
                self.auxcanvas_1.axes.set_ylim( np.min( extensometer ) - abs (np.min( extensometer )) * 20 / 100,
                                                np.max( extensometer ) + abs (np.max( extensometer )) * 20 / 100 )
                
                self.auxcanvas_1.axes.plot( time_np, extensometer, 'y' )
                
                for label in self.auxcanvas_1.axes.get_xticklabels():
                    # label is a Text instance
                    label.set_visible( False )
                self.auxcanvas_1.fig.canvas.draw()

            else:
                temp_range = np.array( [np.min( temp_down[min5*-1:-1] ),
                                     np.min( temp_sample[min5*-1:-1] ),
                                     np.min( temp_up[min5*-1:-1] ),
                                     np.max( temp_down[min5*-1:-1] ),
                                     np.max( temp_sample[min5*-1:-1] ),
                                     np.max( temp_up[min5*-1:-1] )] )

                self.auxcanvas_2.axes.cla()
                self.auxcanvas_2.axes.grid( True )
                self.statusBar().showMessage( 'Ploteando 5Auxiliar 2...' )
                self.auxcanvas_2.axes.set_xlim( time_np[min5*-1], time_np[-1] )
                
                self.auxcanvas_2.axes.set_ylim( np.min( temp_range ) - abs (np.min( temp_range )) * 20 / 100,
                                                np.max( temp_range ) + abs (np.max( temp_range )) * 20 / 100 )
                
                self.auxcanvas_2.axes.plot( time_np[min5*-1:-1], temp_down[min5*-1:-1], 'b',
                                            time_np[min5*-1:-1], temp_sample[min5*-1:-1], 'r',
                                            time_np[min5*-1:-1], temp_up[min5*-1:-1], 'g' )
                
                for label in self.auxcanvas_2.axes.get_xticklabels():
                    # label is a Text instance
                    label.set_visible( False )
                self.auxcanvas_2.fig.canvas.draw()

                # Deformacion en funcion de tiempo
                self.auxcanvas_1.axes.cla()
                self.auxcanvas_1.axes.grid( True )
                self.statusBar().showMessage( 'Ploteando Auxiliar 1...' )
                self.auxcanvas_1.axes.set_xlim( time_np[min5*-1], time_np[-1] )
                
                self.auxcanvas_1.axes.set_ylim( np.min( extensometer[min5*-1:-1] ) - abs (np.min( extensometer[min5*-1:-1] )) * 20 / 100,
                                                np.max( extensometer[min5*-1:-1] ) + abs (np.max( extensometer[min5*-1:-1] )) * 20 / 100 )
                
                self.auxcanvas_1.axes.plot( time_np[min5*-1:-1], extensometer[min5*-1:-1], 'y' )
                
                for label in self.auxcanvas_1.axes.get_xticklabels():
                    # label is a Text instance
                    label.set_visible( False )
                self.auxcanvas_1.fig.canvas.draw()

            del temp_sample, temp_down, temp_up, extensometer, time_np, temp_range, loadcell

### Antes de Inicio de registro de datos 
        else:
            f = open( 'tempdata' )
            s = StringIO( f.read() )
            f.close()
            s.seek( 0 )

            data = np.genfromtxt( s,
##                                       usecols = ( 0, 1, 2, 3, 4, 5 ),
                                       deletechars = "\n",
                                       dtype = float,
                                       autostrip = True,
                                       unpack = True )
            print data
            if data[0] < 60:
                self.lcd_time_second.display( str ( int (data[0] ) ) )
            else:
                m = data[0] // 60
                s = data[0] % 60
                if m < 60:
                    self.lcd_time_second.display( str ( int ( s ) ) )
                    self.lcd_time_minute.display( str ( int ( m ) ) )
                else:
                    h = m // 60
                    m = m % 60
                    self.lcd_time_second.display( str ( int ( s ) ) )
                    self.lcd_time_minute.display( str ( int ( m ) ) )
                    self.lcd_time_hour.display( str ( int ( h ) ) )
            if self.zero_extensometro:
                mostrame = ((data[4] - self.zero_extensometro ) / float ( self.dsbx_sample_heigth.value() ) ) *100
                mostrame= round(mostrame, 4)
                self.lcd_var_2.display( str (mostrame))

                #print data[4], '\t' ,self.zero_extensometro, '\t', self.dsbx_sample_heigth.value()
               # print float (data[4]), '\t' ,float(self.zero_extensometro), '\t', float (self.dsbx_sample_heigth.value()), '\t', mostrame
            else:
                self.lcd_var_2.display( str ( ( float ( data[4] ) / float ( self.dsbx_sample_heigth.value() ) ) *100 ) )
            self.lcd_var_5.display( str ( float ( data[4]) ))
            self.lcd_var_1.display( str ( float ( data[5] )*9.8 / ( float ( self.dsbx_sample_width.value() ) * float ( self.dsbx_sample_thickness.value() ) ) ) )
            self.lcd_var_3.display( str ( data[5] ) )
            self.lcd_temperature_up.display( str ( data[3] ) )
            self.lcd_temperature_sample.display( str ( data[2] ) )
            self.lcd_temperature_down.display( str ( data[1] ) )

def main():
    app = QtGui.QApplication( sys.argv )
    DAQ = Main()
    DAQ.show()
    sys.exit( app.exec_() )
if __name__ == '__main__':
    main()
