'''
Created on 21/02/2013

@author: Solar
'''
#===============================================================================
# class Ploter( FigureCanvas ):
# 
#    def __init__( self, parent, y ):
#        # Se instancia el objeto figure
#        self.fig = Figure()
#        #Se define la grafica en coordenadas polares
#        self.axes = self.fig.add_subplot( 111 )
#        #Se define el limite del eje X
#        x = np.arange( 1, 1025, 1 )
#        self.axes.plot( x, y )
#        self.axes.set_xlim( [1, 1024] )
# 
#        #Se define una grilla
#        self.axes.grid( True )
#        #Se crea una etiqueta en el eje Y
#        self.axes.set_ylabel( 'Counts' )
#        self.axes.set_xlabel( '' )
# 
#        # se inicializa FigureCanvas
#        FigureCanvas.__init__( self, self.fig )
#        # se define el widget padre
#        self.setParent( parent )
#        # se define el widget como expandible
#        FigureCanvas.setSizePolicy( self,
#                QtGui.QSizePolicy.Expanding,
#                QtGui.QSizePolicy.Expanding )
#        # se notifica al sistema de la actualizacion
#        #de la politica
#        FigureCanvas.updateGeometry( self )
#        self.fig.canvas.draw()
#===============================================================================


#===============================================================================
#    def Plotear( self, y ):
#        self.statusBar().showMessage( 'Ploting...' )
#        if not self.qmc:
#            self.vbl = QtGui.QVBoxLayout( self.Plot )
# 
#            if self.chk_autobkgsus.checkState():
#                if self.le_selectedbkg.text() == '':
#                    self.le_selectedbkg.setText( QtGui.QFileDialog.getOpenFileName( parent = None, caption = 'Open Background File' ) )
#                else:
#                    background = np.genfromtxt( str( self.le_selectedbkg.text() ), skiprows = 7, useecols = 1, delimiter = '\t' )
#                    y = y - background
#            #Se instancia el Ploter con la grafica de Matplotlib
#            self.qmc = Ploter( self.Plot, y )
#            # se instancia la barra de navegacion
#            self.ntb = NavigationToolbar( self.qmc, self.Plot )
#            # se empaqueta el lienzo y 
#            #la barra de navegacion en el vbox
#            self.vbl.insertWidget( 0, self.qmc )
#            self.vbl.insertWidget( 1, self.ntb )
# 
#        else:
#            QtGui.QLayout.removeWidget( self.vbl, self.qmc )
#            QtGui.QLayout.removeWidget( self.vbl, self.ntb )
# 
#            if self.chk_autobkgsus.checkState():
# 
#                if self.le_selectedbkg.text() == '':
#                    self.le_selectedbkg.setText( QtGui.QFileDialog.getOpenFileName( parent = None,
#                                                                                    caption = 'Open Background File' ) )
#                else:
#                    background = np.genfromtxt( str( self.le_selectedbkg.text() ),
#                                                skiprows = 7,
#                                                usecols = 1,
#                                                delimiter = '\t' )
#                    y = y - background
# 
#            #Se instancia el Ploter con la grafica de Matplotlib     
#            self.qmc = Ploter( self.Plot, y )
#            # se instancia la barra de navegacion
#            self.ntb = NavigationToolbar( self.qmc, self.Plot )
#            # se empaqueta el lienzo y 
#            #la barra de navegacion en el vbox
#            self.vbl.insertWidget( 0, self.qmc )
#            self.vbl.insertWidget( 1, self.ntb )
# 
#        if np.max( y ) >= 4096 :
#            self.statusBar().showMessage( 'SATURATED AT' + str( np.argmax( y ) ) )
#        else:
#            self.statusBar().showMessage( 'Ready...' )
#===============================================================================
