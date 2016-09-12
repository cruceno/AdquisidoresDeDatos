'''
Created on 22/08/2012
Progrma de adquisicion de datos para Dilatometro
version grafica
<
@author: Javito
'''
# Importar librerias necesarias
# interfaz grafica y comunicacion con sistema y puerto serie
from PyQt4 import QtCore, QtGui, uic
import os, sys, serial
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

    '''Con esta clase que herada las propiedades de hilos Qt vamos a crear un hilo que se va a encargar
       de tomar los datos del dispositivo. '''

    def __init__( self, parent = None ):
        QtCore.QThread.__init__( self, parent )
        self.exiting = False
        self.message = ''

    def read( self, port, baudrate, delay_time ):
        self.ser = serial.Serial( port = port,
                          baudrate = baudrate,
                          parity = serial.PARITY_NONE,
                          stopbits = 1,
                          bytesize = 8,
                          timeout = 2 )

        self.delay_time = delay_time

        self.start()

    def run( self ):

        """Proceso de Scan"""

        from time import sleep
        self.ser.close()
        self.ser.open()
        self.time_stamp = 0
        while not self.exiting:

            sleep( self.delay_time )
            self.time_stamp = self.time_stamp + self.delay_time
            if self.ser.inWaiting() > 0:
                self.ser.read( self.ser.inWaiting() )
            line = self.ser.readline()
            l = len( line )

            if l == 14:
                # La salida que me manda el puerto es una cadena con 14 caracteres
                print line
                temp_data = line[0:4]  # Los 5 primeros caracteres me daban un valor de temperatura
                lvdt_data = line[6:12]  # Los otros restantes un valor de voltaje
                data = [self.time_stamp, temp_data, lvdt_data]
                self.emit( QtCore.SIGNAL ( "readsignal(PyQt_PyObject)" ), data )

            elif len( line ) == 0:  # si deja de recibir datos sale? del programita...
                self.ser.close()  # cierro el puerto
                self.exiting = True
            else:
                pass
        self.ser.close()
        self.exit()
    def __del__( self ):
        self.exiting = True
        self.wait()


class Main( QtGui.QMainWindow ):
    """La ventana principal de la aplicacion."""

    def __init__( self ):

        QtGui.QMainWindow.__init__( self )
        # Cargamos la interfaz desde el archivo .ui
        uifile = os.path.join( 
             os.path.abspath( 
                 os.path.dirname( __file__ ) ), 'main.ui' )
        uic.loadUi( uifile, self )
        self.LVDT = LVDT()

        for i in range ( 50 ):
            try:
                s = serial.Serial( i )
                self.cb_port.addItem( s.portstr, s.portstr )
                s.close()
            except:
                pass


        # Inicializando base de ploteo para mainplot
        self.vbl_main = QtGui.QVBoxLayout( self.main_plot )
        self.maincanvas = canvas( self.main_plot )
        self.vbl_main.insertWidget( 0, self.maincanvas )
        # self.maincanvas_ntb = NavigatioToolbar( self.maincanvas, self.main_plot )
        # self.vbl_main.insertWidget( 1, self.maincanvas_ntb )
        self.maincanvas.axes.set_xlabel( 'Temp' )
        self.maincanvas.axes.set_ylabel( 'LVDT Signal' )

        # Inicializando base de ploteo para aux1
        self.vbl_aux1 = QtGui.QVBoxLayout( self.aux1_plot )
        self.aux1canvas = canvas( self.aux1_plot )
        self.vbl_aux1.insertWidget( 0, self.aux1canvas )
#        self.aux1canvas.axes.set_xlabel( 'Time' )
#        self.aux1canvas.axes.set_ylabel( 'Temp' )

        # Inicializando base de ploteo para aux2
        self.vbl_aux2 = QtGui.QVBoxLayout( self.aux2_plot )
        self.aux2canvas = canvas( self.aux2_plot )
        self.vbl_aux2.insertWidget( 0, self.aux2canvas )
#        self.aux2canvas.axes.set_xlabel( 'Time' )
#        self.aux2canvas.axes.set_ylabel( 'LVDT Signal' )

        # Variables (listas) para contener la informacion que se va recolectando... cuanto mas tiempo se tenga en funcionameinto mas grande va a ser la variable ?
        # se puede evitar  si el tamao de la variable trae problemas el ploteo de datos se podria realizar levantando los mismos desde el archivo
        # de salida abriendo este como solo lectura
        self.lvdt = list()
        self.temp = list()
        self.time_stamp = list()
        self.savedata = False
        self.actionQuit.triggered.connect( QtGui.qApp.quit )
        self.connect( self.reader, QtCore.SIGNAL( "readsignal(PyQt_PyObject)" ), self.save_data )
        self.connect( self.reader, QtCore.SIGNAL( "readsignal(PyQt_PyObject)" ), self.show_data )
#----------------------------------------------------------------------------------
# Las siguientes 4 funciones son las encargadas de ajustar la escala de la grafica principal
# por medio de los controles proporcionados al usuario
    @QtCore.pyqtSlot( int )
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
#------------------------------------------------------------------------------------

    @QtCore.pyqtSlot()
    def on_pb_start_clicked( self ):
        # inicializar archivos leer configuraciones inicializar puerto serie
        self.pb_startsave.setEnabled( True )
        outfile = self.le_file.text()
        if outfile == '':
            self.statusBar().showMessage( 'El campo que indica el archivo de destino no puede estar vacio' )
        else:
            outfile += '.txt'
            self.file = open( outfile, 'w' )
            header = 'User:' + self.le_user.text() + '\n' + 'Material:' + self.le_material.text() + '\n' + 'Observaciones:\n' + self.te_header.toPlainText() + '\n'
            self.file.write ( header )
#             self.savedata = True
            port = str ( self.cb_port.currentText() )
            baudrate = str ( self.cb_baudrate.currentText() )
            delay_time = self.dsb_step.value()
            self.reader.read( port, baudrate, delay_time )

    @QtCore.pyqtSlot()
    def on_pb_end_clicked( self ):
        # detener todo (reader)
        self.reader.exiting = True

    @QtCore.pyqtSlot()
    def on_tlb_open_pressed( self ):
        # seleccionar archivo
        self.le_file.setText( QtGui.QFileDialog.getSaveFileName( parent = None ) )
    @QtCore.pyqtSlot()
    def on_pb_startsave_clicked( self ):
        self.savedata = True
        self.reader.time_stamp = 0
        self.maincanvas.axes.cla()
        self.aux1canvas.axes.cla()
        self.aux2canvas.axes.cla()

    @QtCore.pyqtSlot()
    def save_data( self, data ):
        if self.savedata:
            self.statusBar().showMessage( 'Escribiendo al archivo...' )
            line = str ( data[0] ) + '\t' + str ( data[1] ) + '\t' + str ( data[2] ) + '\n'
            self.file.write( line )

    @QtCore.pyqtSlot()
    def show_data( self, data ):
        self.time_stamp.append( data[0] )
        self.temp.append( data[1] )
        self.lvdt.append( data[2] )
        self.speed = []
#       Display de tiempo transcurrido
        if data[0] < 60:
            self.lcd_time_seg.display( str ( int ( data[0] ) ) )
#            print data[0]
        else:
            m = data[0] // 60
            s = data[0] % 60
            if m < 60:
                self.lcd_time_seg.display( str ( int ( s ) ) )
                self.lcd_time_min.display( str ( int ( m ) ) )
#                print str ( m ) + ':' + str ( s )
            else:
                h = m // 60
                m = m % 60
                self.lcd_time_seg.display( str ( int ( s ) ) )
                self.lcd_time_min.display( str ( int ( m ) ) )
                self.lcd_time_hour.display( str ( int ( h ) ) )
#                print str ( h ) + ':' + str ( m ) + ':' + str ( s )
#       Controlar numeros negativos y float punto decimal y demases de los display
        self.lcd_temp.display( str ( data[1] ) )
        self.lcd_lvdt.display( str ( data[2] ) )

        time = np.array( self.time_stamp, dtype = float )
        temp = np.array( self.temp, dtype = float )
        lvdt = np.array( self.lvdt , dtype = float )

        if np.size( lvdt ) == 1:
            speed = lvdt[-1] / time[-1]
            print speed
            self.lcd_speed.display( str ( speed ) )
        if np.size( lvdt ) == 2:
            speed = ( lvdt[-1] - lvdt[-2] ) / ( time[-1] - time[-2] )
            self.lcd_speed.display( str ( speed ) )
        if np.size( lvdt ) == 3:
            speed = ( lvdt[-1] - lvdt[-3] ) / ( time[-1] - time[-3] )
            self.lcd_speed.display( str ( speed ) )
        if np.size ( lvdt ) == 4:
            speed = ( lvdt[-1] - lvdt[-4] ) / ( time[-1] - time[-4] )
            self.lcd_speed.display( str ( speed ) )
        if np.size( lvdt ) == 5:
            speed = ( lvdt[-1] - lvdt[-5] ) / ( time[-1] - time[-5] )
            self.lcd_speed.display( str ( speed ) )

#        self.speed.append(speed)
#        temp_speed=np.array(self.speed)


        # Ploteando en los canvas ya definidos con las funciones heredadas de la clase canvas

        # Deformacion en funcion de temperatura
        self.statusBar().showMessage( 'Ploteando principal...' )
        # self.maincanvas.axes.set_xlim( np.min( temp ), np.max( temp ) )
        # self.maincanvas.axes.set_ylim( np.min( lvdt ) - np.min( lvdt ) * 20 / 100, np.max( lvdt ) + np.max( lvdt ) * 20 / 100 )
        self.maincanvas.axes.plot( temp, lvdt, 'green' )
        self.maincanvas.fig.canvas.draw()

        # Temperatura en funcion de tiempo
        self.statusBar().showMessage( 'Ploteando Auxiliar 1...' )
        self.aux1canvas.axes.set_xlim( 0, time[-1] )
        self.aux1canvas.axes.set_ylim( np.min( temp ) - np.min( temp ) * 20 / 100, np.max( temp ) + np.max( temp ) * 20 / 100 )
        self.aux1canvas.axes.plot( time, temp, 'blue' )
        self.aux1canvas.fig.canvas.draw()

        # Deformacion en funcion de tiempo
        self.statusBar().showMessage( 'Ploteando Auxiliar 2...' )
        self.aux2canvas.axes.set_xlim( time[0], time[-1] + time[-1] * 10 / 100 )
        self.aux2canvas.axes.set_ylim( np.min( lvdt ) - np.min( lvdt ) * 20 / 100, np.max( lvdt ) + np.max( lvdt ) * 20 / 100 )
        self.aux2canvas.axes.plot( time, lvdt, 'red' )
        self.aux2canvas.fig.canvas.draw()



def main():
    app = QtGui.QApplication( sys.argv )
    LVDT = Main()
    LVDT.show()
    sys.exit( app.exec_() )

if __name__ == "__main__":
    main()
