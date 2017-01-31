'''
Created on 29/11/2011

@author: Javier Cruceno
'''
import os, sys, serial
from PyQt4 import QtCore, QtGui, uic

class RS232Setup( QtGui.QDialogButtonBox ):

    def __init__( self ):
        QtGui.QDialogButtonBox.__init__( self )
        uifile = os.path.join( 
             os.path.abspath( 
                 os.path.dirname( __file__ ) ), 'r232.ui' )
        uic.loadUi( uifile, self )

    def scan( self ):

        #-- Lista de los dispositivos serie. Inicialmente vacia
        dispositivos_serie = []
        num_ports = 20
        #-- Escanear num_port posibles puertos serie
        for i in range( num_ports ):

            try:
                #-- Abrir puerto serie
                s = serial.Serial( i )
                #-- Si no hay errores, anadir el numero y nombre a la lista
                dispositivos_serie.append( ( i, s.portstr ) )
                #-- Cerrar puerto
                s.close()
                #-- Si hay un error se ignora      
            except:
                pass
        #-- Devolver la lista de los dispositivos serie encontrados    
        return dispositivos_serie
    def read_setup( self ):
        fsock = open( 'serial.cfg', 'r' )
        rs232_config = fsock.readlines()
        fsock.close()

    def set_setup( self ):
        fsock = open( 'serial.cfg', 'w' )
        fsock.write( self.cbx_port.currentText() )
        fsock.write( '\n' )
        fsock.write( self.cbx_baudrate.currentTex() )
        fsock.write( '\n' )
        fsock.write( self.cbx_parity.currentTex() )
        fsock.write( '\n' )
        fsock.write( self.cbx_stopbits.currentTex() )
        fsock.write( '\n' )
        fsock.write( self.cbx_bytesize.currentTex() )
        fsock.write( '\n' )
        fsock.write( self.cbx_timeout.currentTex() )


def rs232():
    app = QtGui.QApplication( sys.argv )
    rs232Setup = RS232Setup()
    rs232Setup.show()
    sys.exit( app.exec_() )
