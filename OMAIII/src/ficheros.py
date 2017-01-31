import os
def FileFormat( file, delimiter, miles ):
    """
    La funcion FileFormat() reescribe arcvhivos de texto con datos tabulares
    poniendo como defecto el salto de linea con \n y el separador con \t
    el fin de esta funcion es evitar incompatibilidad con algunas funciones por ser
    archivos con distintos formatos de salto de linea (MAC \r , Linux, \n Windows, \r\n)
    y unificar todos los trabajos con un mismo delimitador estandar en este caso \t
    
    """
    home = os.getcwd()
    #convertir a string los parametros pasados a la funcion
    str( file )
    str( delimiter )
    str( miles )
    #Guardar los datos en memoria
    fsock = open( file, 'rU' )
    fichero = fsock.readlines()
    fsock.close

    temp = os.path.join( home, 'temp' )
    if not os.path.isdir( temp ):
        os.mkdir( temp )
    os.chdir( temp )
    salida = 'Conv' + file
    try:
        fsock = open( salida )
        modo = 'w'
        fsock = open( salida, modo )
        fsock.close
        modo = 'a'
    except:
        modo = 'a'
    #Comprobar si el delimitador que tiene el fichero es 
    #distinto al tabulador y de ser asi lo cambiar
    if delimiter != '\t':
        fsock = open( salida, modo )
        for line in fichero:
            #Cambiamos el delimitador por tabulador
            if line.count( delimiter ) != 0:
                line = line.replace( delimiter, '\t' )
            #eliminamos punto como separador de miles
            if miles:
                while line.count( miles ) != 0:
                    posicion = line.index( miles )
                    line.pop( posicion )
            #Cambiamos coma por punto
            if line.count( ',' ):
                line = line.replace( ',', '.' )
            #escribimos las lineas en el nuevo archivo
            fsock.write( line )
        fsock.close()
    else:
        fsock = open( salida, modo )
        for line in fichero:
            #eliminamos punto como separador de miles
            if miles:
                while line.count( miles ) != 0:
                    posicion = line.index( miles )
                    line.pop( posicion )
            #Cambiamos coma por punto
            if line.count( ',' ):
                line = line.replace( ',', '.' )
            #escribimos las lineas en el nuevo archivo
            fsock.write( line )
        fsock.close()
    os.chdir( home )
    return temp, salida
