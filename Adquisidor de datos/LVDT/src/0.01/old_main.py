'''
Created on 11/01/2011

@author: Javier Marcelo Cruceno
'''
import serial
from time import sleep

if __name__ == '__main__':
    pass

while True:
    file = raw_input( 'Ingrese el nombre del archivo donde se guardaran los datos:\n' )
    path = '../Ensayos/'
    file = path + file + '.txt'
    try:
        fsock = open( file )
        print 'El archivo ingresado como parametro ya existe. Desea utilizar este archivo de todas formas?'
        print 'Ingrese:\n a) Para utilizarlo conservando los datos que contiene \n'
        print 'w) Para utilizarlo borrando el contenido existente \n'
        print 'n) Para especificar un nuevo archivo \n'
        modo = raw_input()
        if modo == 'w' or modo == 'a':
            break
        elif modo == 'n':
            continue
        else:
            while modo != 'w' or modo != 'a' or modo != 'n':
                modo = raw_input( 'El parametro ingresado no es valido ingrese su eleccion nuevamente: \n' )
            break
    except:
        modo = 'a'
        break
serial_port = raw_input( 'Ingrese el nombre del puerto a utilizar \n e.g COM1, COM2 en sistemas Windows o /dev/ttyS1 en sistemas linux \n' )

delay_time = float( raw_input( 'Ingresar el intervalo entre adquisiciones en segundos: \n' ) )

ser = serial.Serial( port = serial_port ,
                   baudrate = 9600,
                   bytesize = 8,
                   parity = 'N',
                   stopbits = 1,
                   timeout = 1,
                   xonxoff = 0,
                   rtscts = 0 )
time_stamp = 0
ser.close()
ser.open()
fsock = open( file, modo )
#esta parte es para poner un delay y descartar datos que no quiero 
while True:
    sleep( delay_time )
    time_stamp = time_stamp + delay_time
    if ser.inWaiting() > 0:
        print 'Se descartaron los siguientes datos: \n'
        descartados = ser.read( ser.inWaiting() )
        print descartados
        print'-----------------------\n'

    line = ser.readline()
    l = len( line )
# Maxi en principio si modificas a partir de aca segun el formato de los datos que te manda el sensor te deberia andar no estoy seguro
    if l == 14:
        #Esto es por que yo tenia que la salida que me mandaba el puerto era una cadena con 14 caracteres 
        print 'Se recibieron %d bytes \n' % l
        temp_data = line[0:4] # Los 5 primeros caracteres me daban un valor de temperatura 
        lvdt_data = line[6:14]#Los otros restantes un valor de voltaje 
        sep = ', '#sparaba los valores con una coma 
        linea = str( time_stamp ) + sep + str( temp_data ) + sep + str( lvdt_data ) #Armaba todo en una linea... y 
        fsock.write( linea )# La escribo en el archivo
        print linea# y la muestro por consola
        line = ''#y limpio la variable para volverla a usar
    elif len( line ) == 0:#si dejaba de recibir datos salia del programita... 
        ser.close()#cierro el puerto 
        fsock.close#cierro el archivo
        print 'Se recibieron %d bytes el programa finalizara automaticamente' % l
        break
    else:
        print 'La lectura recibida esta corrupta por error de sincronizacion y sera descartada'
