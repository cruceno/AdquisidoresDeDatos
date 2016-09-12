'''
Created on 21/02/2013

@author: Solar
'''
from PyQt4 import QtGui, QtCore, uic
import os, sys, glob
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
#from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure
import numpy as np

class canvas( FigureCanvas ):
    def __init__( self, parent ):
# Se instancia el objeto figure
        self.fig = Figure()
#Se define la grafica en coordenadas polares  
        self.axes = self.fig.add_subplot( 111 )
#Se define limite del eje x, en este caso va a ser siempre el mismo   
        self.axes.set_xlim( [1, 1024] )
#Se define una grilla    
        self.axes.grid( True )
#Se agregan etiquetas a los ejes     
        self.axes.set_ylabel( 'Counts' )
#Se agregan etiquetas a los ejes
        self.axes.set_xlabel( 'Pixel' )
# se inicializa FigureCanvas
        FigureCanvas.__init__( self, self.fig )
# se define el widget padre que fue pasado como parametro a la clase   
        self.setParent( parent )
# se define el widget como expandible
        FigureCanvas.setSizePolicy( self, QtGui.QSizePolicy.Expanding,
                                     QtGui.QSizePolicy.Expanding )
# se notifica al sistema de la actualizacion de la politica       
        FigureCanvas.updateGeometry( self )
#Se dibuja la grafica en el widget asignado
        self.fig.canvas.draw()

class Main( QtGui.QMainWindow ):
    """La ventana principal de la aplicacion."""

    def __init__( self ):
        QtGui.QMainWindow.__init__( self )
        # Cargamos la interfaz desde el archivo .ui
        uifile = os.path.join( 
             os.path.abspath( 
                 os.path.dirname( __file__ ) ), 'ploter.ui' )
        uic.loadUi( uifile, self )
#        self.actionQuit.triggered.connect( QtGui.qApp.quit )
#        self.connect( self.scaner, QtCore.SIGNAL( "scansignal(PyQt_PyObject)" ), self.data_show_and_save )
#        self.connect( self.scaner, QtCore.SIGNAL( "msgsignal(PyQt_PyObject)" ), self.change_messagge )
#        self.connect( self.scaner, QtCore.SIGNAL( "finished()" ), self.update_ui )
#        self.connect( self.scaner, QtCore.SIGNAL( "terminated()" ), self.update_ui )

        #Inicializando base de ploteo para mainplot
        self.vbl_main = QtGui.QVBoxLayout( self.pl_main_plot )
        self.pl_maincanvas = canvas( self.pl_main_plot )
        self.vbl_main.insertWidget( 0, self.pl_maincanvas )
#        self.da_mainntb = NavigationToolbar( self.da_maincanvas, self.da_main_plot )
#        self.vbl_main.insertWidget( 1, self.da_mainntb )

    def plot( self, y ):
        self.statusBar().showMessage( 'Ploting...' )

#        if self.chk_autobkgsus.checkState():
#            if self.le_selectedbkg.text() == '':
#                self.le_selectedbkg.setText( QtGui.QFileDialog.getOpenFileName( parent = None, caption = 'Open Background File' ) )
#            else:
#                background = np.genfromtxt( str( self.le_selectedbkg.text() ),
#                                            skiprows = 7,
#                                            useecols = 1,
#                                            delimiter = '\t' )
#                y = y - background
        #Dibujar Curva
        self.da_maincanvas.axes.set_ylim( np.min( y ) - np.min( y ) * 20 / 100, np.max( y ) + np.max( y ) * 20 / 100 )
        self.da_maincanvas.axes.plot( self.x, y, 'blue' )
        self.da_maincanvas.fig.canvas.draw()
    @QtCore.pyqtSlot()
    def on_pl_btn_open_folder_clicked ( self ):
        self.lb_folder_path.setText( QtGui.QFileDialog.getExistingDirectory( parent = None, caption = "Select folder..." ) )
        dir = str ( self.lb_folder_path.text() ) + '\\'
        files = filter( os.path.isfile, glob.glob( dir + '*.OMAIII' ) )
        j = 0
        for file in files:
            print file
            if os.path.isdir( file ):
                continue
            newitem = os.path.basename( file )
            self.file_list.insertItem( j, newitem )
            j += 1

def main():
    app = QtGui.QApplication( sys.argv )
    OMAIII = Main()
    OMAIII.show()
    sys.exit( app.exec_() )

if __name__ == "__main__":
    main()
