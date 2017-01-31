'''
Created on 27/09/2011

@author: Solar
'''
import serial
import numpy as np

ser = serial.Serial( port = 'COM14', baudrate = 9600, parity = serial.PARITY_NONE, stopbits = 1, bytesize = 8, timeout = 10 )

ser.close()
ser.open()
oma = ''
comando = 'ET 6\r\n'
ser.write( comando )
while oma != '*':
    oma = ser.read()
    print 'esperando oma'
    if oma == '?':
        print comando, 'OMA III Error'
        oma = ''
        break
ser.write( 'I 10\r\n' )
print 'Scans', ser.read()
ser.write( 'ET\r\n' )
print ser.readline()
print ser.read()
comando = 'RUN\r\n'
ser.write( comando )
oma = ''
while oma != '*':
    oma = ser.read()
    print 'esperando oma'
    if oma == '?':
        print comando, 'OMA III Error'
        oma = ''
        break

ser.write( 'DC 1,1,1024\r\n' )
while ser.inWaiting < 4096:
    continue
espectro = ser.readline().rstrip( '\r\n' )
y = np.fromstring( espectro, sep = ',' )
print ser.read()
print ser.inWaiting()
print y, np.size( y, 0 )
