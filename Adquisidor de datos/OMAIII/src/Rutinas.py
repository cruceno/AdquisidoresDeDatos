'''
Created on 04/10/2011

@author: Solar
'''
import os, sys
from PyQt4 import QtGui, QtCore, uic
from ficheros import FileFormat

class Espectro( object ):
    def __init__( self, file, exposuretime, scansnumber, ignoredscans, damode, detectortemp, counter, red ):
        self.name = file
        self.exposuretime = exposuretime
        self.scansnumber = scansnumber
        self.ignoredscans = ignoredscans
        self.damode = damode
        self.detectortemp = detectortemp
        self.counter = counter
        self.red = red
    def __repr__( self ):
        return repr( ( self.name, self.counter, self.red ) )


class Rutinas ( QtGui.QMainWindow ):
    def __init__( self ):
        QtGui.QMainWindow.__init__( self )
        # Cargamos la interfaz desde el archivo .ui
        uifile = os.path.join( 
             os.path.abspath( 
                 os.path.dirname( __file__ ) ), 'rutinas.ui' )
        uic.loadUi( uifile, self )

    @QtCore.pyqtSlot()
    def on_open_btn_pressed( self ):
        self.folder = QtGui.QFileDialog.getExistingDirectory( self, 'Open Folder' )
        os.chdir( str( self.folder ) )
        for file in os.listdir( self.folder ):
            if os.path.isdir( file ):
                continue
            self.folderView.addItem( file )

    @QtCore.pyqtSlot()
    def on_add_btn_pressed( self ):
        self.orderList.addItem()

    @QtCore.pyqtSlot()
    def on_remove_btn_pressed( self ):
        self.orderList.removeItem()

    @QtCore.pyqtSlot()
    def on_up_btn_pressed( self ):
        self.orderList

    @QtCore.pyqtSlot()
    def on_down_btn_pressed( self ):
        pass

    @QtCore.pyqtSlot()
    def on_sort_btn_pressed( self ):

        import numpy as np
        espectros = []

        for i in range( self.orderList.count() ):

            file = self.orderList.item( i ).text()
            fsock = open ( file, 'r' )
            exposuretime = fsock.readline()
            scansnumber = fsock.readline()
            ignoredscans = fsock.readline()
            damode = fsock.readline()
            detectortemp = fsock.readline()
            red = fsock.readline()
            counter = fsock.readline()
            fsock.close()
            espectros.append( Espectro( file, exposuretime, scansnumber, ignoredscans, damode, detectortemp, counter, red ) )
        if self.cbx_order.currentText() == 'Exposure Time':

            for element in sorted( espectros, key = lambda espectro: espectro.exposuretime ):
                scansequence = [element.name, element.exposuretime, element.scansnumber, element.ignoredscans, element.damode, element.detectortemp, element.counter, element.red]
                dir, file = FileFormat( scansequence[0], '\t', '' )
                y = np.genfromtxt( file, skiprows = 7, usecols = 1, delimiter = '\t' )
                print y
    @QtCore.pyqtSlot()
    def on_save_btn_pressed( self ):
        pass


def main():
    app = QtGui.QApplication( sys.argv )
    rutina = Rutinas()
    rutina.show()

    sys.exit( app.exec_() )


main()
