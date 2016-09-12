'''
Created on 04/11/2011

@author: Solar
'''
import os, sys, glob
import numpy as np
from PyQt4 import QtCore, QtGui, uic

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

class SortDialog ( QtGui.QDialog ):
    def __init__( self ):
        QtGui.QDialog.__init__( self )
                # Cargamos la interfaz desde el archivo .ui
        uifile = os.path.join( 
             os.path.abspath( 
                 os.path.dirname( __file__ ) ), 'sort.ui' )
        uic.loadUi( uifile, self )

    @QtCore.pyqtSlot()
    def on_tlb_open_clicked( self ):
        self.le_path.setText( QtGui.QFileDialog.getExistingDirectory( self, 'Open Folder' ) )

#    @QtCore.pyqtSlot()
#    def on_tlb_save_pressed( self ):
#        self.le_save_path.setText( QtGui.QFileDialog.getSaveFileName( self, 'Save File', os.path.pardir ) )
    @QtCore.pyqtSlot()
    def on_btn_sort_clicked( self ):
        self.lb_status.setText( 'Iniciado' )
        dir = str( self.le_path.text() ) + '\\'
        patron = dir + '*.OMAIII'
#        print patron
        archivos = filter( os.path.isfile, glob.glob( patron ) )
        espectros = []
        for espectro in archivos:
            self.lb_status.setText( ' Listando Espectros' )
            file = str( espectro )
            if not os.path.isdir( file ):
#                print file
                fsock = open ( file, 'r' )
                exposuretime = fsock.readline()
                scansnumber = fsock.readline()
                ignoredscans = fsock.readline()
                damode = fsock.readline()
                detectortemp = fsock.readline()
                red = fsock.readline()
                counter = fsock.readline()
                fsock.close()
                espectros.append( Espectro( str( file ), exposuretime, scansnumber, ignoredscans, damode, detectortemp, counter, red ) )
        self.sort_espectros( espectros )

    def preparar_datos( self, element, data ):
        self.lb_status.setText( ' Preparando datos' )
        y = np.genfromtxt( element.name, skiprows = 7, usecols = 1, delimiter = '\t', dtype = None )
        i = 0
        for line in data:
            if i == 0:
                data[0] = line.rstrip( '\n' ) + '\t' + element.exposuretime
            elif i == 1:
                data[1] = line.rstrip( '\n' ) + '\t' + element.scansnumber
            elif i == 2:
                data[2] = line.rstrip( '\n' ) + '\t' + element.ignoredscans
            elif i == 3:
                data[3] = line.rstrip( '\n' ) + '\t' + element.damode
            elif i == 4:
                data[4] = line.rstrip( '\n' ) + '\t' + element.detectortemp
            elif i == 5:
                data[5] = line.rstrip( '\n' ) + '\t' + element.red
            elif i == 6:
                data[6] = line.rstrip( '\n' ) + '\t' + element.counter
            elif i == 7:
                data[7] = line.rstrip( '\n' ) + '\t' + os.path.basename( element.name ) + '\n'
            else:
                i2 = i - 8
                data[i] = line.rstrip( '\n' ) + '\t' + str( y[i2] ) + '\n'
            i = i + 1
#            print i
        return data

    def primera_columna( self, filename ):
        self.lb_status.setText( 'Imprimiendo priemra columna' )
        fsock = open( filename, 'w' )
        #Escritura de la primera columna del archivo
        x = np.arange( 1, 1025, 1 )
        fsock.write( 'Tiempo de exposicion:\nNumero de Scans\nScans Ignorados\nModo de Adquiquisicion\nTemperatura del detector\nRed\nPosicion del Contador\nArchivo:\n' )
        for i in np.nditer( x ):
            line = str( i ) + '\n'
            fsock.write( line )
        fsock.close()
        fsock = open( filename, 'r' )
        data = fsock.readlines()
        fsock.close()
        return data

    def sort_espectros( self, espectros ):
        self.lb_status.setText( 'Ordenando espectros' )
        posiciones = []
        current = None
        for espectro in espectros:
            if current != espectro.counter:
                if posiciones.count( espectro.counter ) == 0:
                    posiciones.append( espectro.counter )
                current = espectro.counter
#        print posiciones
        for counter in posiciones:
            self.lb_status.setText( 'Guardando archivo' )
            filename = os.path.dirname( espectro.name ) + '\\E' + counter.rstrip( '\n' ) + '.txt'
#            print filename
            filtradas = []
            for espectro in espectros:
                if counter == espectro.counter:
                    filtradas.append( espectro )
            try:
                fsock = open( filename, 'r' )
                data = fsock.readlines()
                fsock.close()
            except:
                data = self.primera_columna( filename )
#            print filtradas
            for element in sorted( filtradas, key = lambda espectro: espectro.name ):
                data = self.preparar_datos( element, data )


            #Escribimos todos los datos en el archivo
            fsock = open( filename, 'w' )
#            print 'guardando archivo: ' + filename
            for line in data:
                fsock.write( str( line ) )
            fsock.close()
        self.lb_status.setText( 'Finalizado' )

def sort():
    app = QtGui.QApplication( sys.argv )
    Sort = SortDialog()
    Sort.show()
    sys.exit( app.exec_() )
sort()
