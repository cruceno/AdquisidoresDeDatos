'''
Created on 28/5/2015

@author: javier
'''

from PyQt4 import QtCore, QtGui, uic
import os, sys, serial,time, parallel
#Funcion para pasar datos como si fueran un archivo de texto
from StringIO import StringIO
# Librerias para graficar en el ploter
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
# from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigatioToolbar
from matplotlib.figure import Figure
# Manejo numerico de datos
import numpy as np


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

class LVDT ( QtCore.QThread ):
    
    def __init__( self, parent = None ):
        QtCore.QThread.__init__( self, parent )
        self.exiting = False
        self.message = ''

    def start_test( self, serial_object ,parallel_object, delay_time, fan_on, fan_off, outfile ):
        self.emit( QtCore.SIGNAL ("statusmsg(QString)"),"Inicializando puertos")
        self.ser=serial_object
        self.p= parallel_object
        self.ser.close()
        self.ser.open()
        self.emit( QtCore.SIGNAL ("statusmsg(QString)"),"Asignando constantes")
        self.outfile = outfile
        self.p.setData(255)
        self.delay_time = delay_time - fan_off - fan_on
        self.fan_off = fan_off
        self.fan_on = fan_on
        self.start()
        
    def run(self):
        first=True
        self.zero_time=time.time()
        while not self.exiting:
            
            if first:
                fsock = open( self.outfile, 'w' )
                first = False
                
            else:
                fsock = open( self.outfile, 'a' )
            self.message='Esperando . . .'
            self.emit( QtCore.SIGNAL ("statusmsg(PyQt_PyObject)"),self.message)    
            time.sleep(self.delay_time)
            readok=False
            self.p.setData(0x0)
            self.emit( QtCore.SIGNAL ("statusmsg(PyQt_PyObject)"),"Estabilizando . . .")
            time.sleep(self.fan_off)
            while not readok:
                self.emit( QtCore.SIGNAL ("statusmsg(PyQt_PyObject)"),"Limpiando bufer . . .")
                self.ser.read(self.ser.inWaiting())
                time.sleep(0.50)
                self.emit( QtCore.SIGNAL ("statusmsg(PyQt_PyObject)"),"Tomando lectura . . .")
                linea=str (self.ser.readline())
                if len(linea)==17:
                    self.emit( QtCore.SIGNAL ("statusmsg(PyQt_PyObject)"),"OK . . .")
                    self.time_stamp = (time.time()-self.zero_time)/60
                    lvdt_data = int(linea)
                    data = [self.time_stamp, lvdt_data ]
                    self.emit( QtCore.SIGNAL ("statusmsg(PyQt_PyObject)"),"Guardando datos. . .")
                    # Se arma linea de texto para guardar en el archivo
                    line = str ( data[0] ) + '\t' + str ( data[1] ) + '\n'
                    # Se escsecondsribe linea en el archivo
                    fsock.write( line )
                    # Se cierra el archivo
                    fsock.close()
                    self.emit( QtCore.SIGNAL ("statusmsg(PyQt_PyObject)"),"Graficando. . .")
                    
                    self.emit( QtCore.SIGNAL ( "readsignal(PyQt_PyObject)" ), data )
                    readok= True
                else:
                    self.emit( QtCore.SIGNAL ("statusmsg(PyQt_PyObject)"),"Lectura invlida . . .")
                    continue
            self.emit( QtCore.SIGNAL ("statusmsg(PyQt_PyObject)"),"Reiniciando ventilacion")
            time.sleep(self.fan_on)
            readok=False
            self.p.setData(255)
        
        self.p.setData(0x0)
        self.exit()
        
    def __del__( self ):
        self.exiting = True
        self.p.setData(0x0)
        
class Main( QtGui.QMainWindow ):
    """La ventana principal de la aplicacion."""

    def __init__( self ):

        QtGui.QMainWindow.__init__( self )
        # Cargamos la interfaz desde el archivo .ui
        uifile = os.path.join(os.path.abspath(os.path.dirname( __file__ ) ),
                              'Balanza2.ui' )
        uic.loadUi( uifile, self )
        #generamos una instancia del thread que toma los datos
        self.pb_stop.setEnabled( False )
        serial_port=str (self.le_serial_port.text())
        self.ser = serial.Serial(port=serial_port,
                           baudrate= 9600,
                           bytesize= 8,
                           parity= 'N',
                           stopbits=1,
                           timeout=1,
                           xonxoff=0,
                           rtscts=0,)
        
        self.p = parallel.Parallel() 
        # Inicializando base de ploteo para mainplot
        self.vbl_main = QtGui.QVBoxLayout( self.gB_Plot )
        self.maincanvas = canvas( self.gB_Plot )
        self.vbl_main.insertWidget( 0, self.maincanvas )
        # self.maincanvas_ntb = NavigatioToolbar( self.maincanvas, self.main_plot )
        # self.vbl_main.insertWidget( 1, self.maincanvas_ntb )
        self.maincanvas.axes.set_xlabel( 'Tiempo (m)' )
        self.maincanvas.axes.set_ylabel( 'LVDT (mV)' )
        
       
    @QtCore.pyqtSlot()
    def on_pb_start_clicked ( self ):
        self.Balanza_test()
        self.pb_start.setEnabled( False )
    
    @QtCore.pyqtSlot()
    def on_pb_stop_clicked ( self ):
        # Detiene ele subproceso de adquisicion de datos.
        self.LVDT.exiting = True
        time.sleep(1)
        self.p.setData(0x0)
        self.LVDT.terminate()
        self.LVDT.wait()

                
        # Se toma lo escrito en las observaciones para guardarlo en el arhivo comentado con un "#"
        observaciones = self.pTE_Observaciones.toPlainText()
        self.observaciones = ''
        for line in observaciones.split( '\n' ):
            self.observaciones = self.observaciones + '#' + line + '\n'
        
        labels='Tiempo (s) \t LVDT (mV)\n'
        
        # Observaciones mas linea de encabezados de tabla. 
        self.observaciones=self.observaciones+labels
        
        # Lee el archivo de salida completo y agrega al inicio  
        # las observaciones y los encabezados de las columnas -------
        f = open( self.le_output_file_path.text() + '.txt' )
        s = self.observaciones + f.read()
        f.close()
        
        # Escribe tados los datos con encabezado y pie de pagina incluido
        # nuevamente en el arhivo. ---------------------------------------
        f = open( self.le_output_file_path.text() + '.txt', 'w' )
        f.write( s )
        f.close()
        self.update_message("Medicion completada. Archivo: "+self.outfile)
        self.pb_start.setEnabled( True )
        
    def Balanza_test ( self ):
        self.LVDT = LVDT()
        self.connect( self.LVDT, QtCore.SIGNAL ( "statusmsg(PyQt_PyObject)" ), self.update_message)
        self.connect( self.LVDT, QtCore.SIGNAL ( "readsignal(PyQt_PyObject)" ), self.show_incoming_data ) 

    
        # inicializar archivos leer configuraciones inicializar puerto serie
        self.outfile = self.le_output_file_path.text()
        self.ser.portstr= str (self.le_serial_port.text())
        
        if self.outfile == '':
            self.update_message( 'El campo que indica el archivo de destino no puede estar vacio' )
        else:
            self.outfile += '.txt'
            # print serial_port
            delay_time=self.sb_delay_time.value()
            fan_on=self.sb_fan_on.value()
            fan_off=self.sb_fan_off.value()
            
            self.LVDT.start_test(self.ser, self.p, delay_time,fan_on, fan_off, self.outfile)
        
            self.pb_stop.setEnabled( True )
            
            
    @QtCore.pyqtSlot ()
    def show_incoming_data ( self, data ):        
        del data
        f = open( self.le_output_file_path.text() + '.txt' )
        s = StringIO( f.read() )
        f.close()
        s.seek( 0 )

        time_np, lvdt = np.genfromtxt( s,
                                   usecols = ( 0, 1),
                                   deletechars = "\n",
                                   dtype = float,
#                                        comment='%',
                                   autostrip = True,
                                   unpack = True )


        # Ploteando en los canvas ya definidos con las funciones heredadas de la clase canvas
        # Deformacion en funcion de temperatura
        self.maincanvas.axes.cla()
        self.maincanvas.axes.grid( True )
        self.maincanvas.axes.plot( time_np, lvdt, 'g' )
        self.maincanvas.axes.set_xlim( time_np[0], time_np[-1]+self.sb_delay_time.value()/60 )
        self.maincanvas.axes.set_ylim( np.min( lvdt ) - abs (np.min( lvdt ) * 20 / 100), np.max( lvdt ) + abs( np.max( lvdt ) * 20 / 100) )
        self.maincanvas.axes.set_xlabel( 'Tiempo (m)' )
        self.maincanvas.axes.set_ylabel( 'LVDT (mV)' )
        self.maincanvas.fig.canvas.draw()
            
    @QtCore.pyqtSlot ()
    def on_tlb_output_file_path_pressed( self ):
        # seleccionar archivo
        self.le_output_file_path.setText( QtGui.QFileDialog.getSaveFileName( parent = None ) )
        
    @QtCore.pyqtSlot ()
    def update_message(self, mensaje):
        self.statusBar().showMessage(mensaje)
        
def main():
    app = QtGui.QApplication( sys.argv )
    DAQ = Main()
    DAQ.show()
    sys.exit( app.exec_() )
if __name__ == '__main__':
    main()