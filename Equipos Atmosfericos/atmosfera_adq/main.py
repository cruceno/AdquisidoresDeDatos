#!/home/sistemas/atmosfera_adq/env/bin/python

import time, sys, logging
time.sleep(20)
from daemon import Daemon
import db_connector as db

class ADQ(Daemon):
            
    def run (self):
	
        logging.basicConfig(filename='/home/sistemas/atmosfera_adq/atmosfera_adq.log', level=logging.WARNING)
        self.error=False
        
        try:
            fsock=open('home/sistemas/atmosfera_adq/db.cfg', 'r')
            datos=fsock.readlines()
            fsock.close()
        except:
            msg='Proceso detenido con errores, No se puede acceder al archivo db.cfg, corrija los errores para volver a iniciar.'
            logging.error(msg)
            sys.exit(2)
        #self.db_conn=db.db(datos) 
        try:
            self.db_conn=db.db(datos)
        except:
            msg='Proceso detenido con errores: '+str(sys.exc_info()[0])
            logging.debug('Datos utilizados para la configuracion:'+str(datos))
	    logging.error( msg)
	    raise
            sys.exit(2)
            
        if not self.error:
            #importar serial de PySerial
            import serial
            
            # Obtener configuracion del puerto serie almacenada en la base de datos
            self.serial_cfg=self.db_conn.get_serial_config()
    
            try:
                #inicializar puerto serie con la configuracion obtenida
                self.ser = serial.Serial( port     = self.serial_cfg.port,
                                          baudrate = int(self.serial_cfg.baudrate),
                                          parity   = self.serial_cfg.parity,
                                          stopbits = int(self.serial_cfg.stopbits),
                                          bytesize = int(self.serial_cfg.bytesize),
                                          timeout  = 2
                                          )
                self.ser.close()
                
            except serial.SerialException:   
                msg='No se pudo establecer la conexion con el puerto:%s'%self.serial_cfg.port 
                logging.error( msg )
                sys.exit(2)
            
            self.ser.open()
            # Establecer tiempo de espera en segundos entre medicion y medicion,
            # utilizado para establecer la cantidad de datos almacenados por el software.
            
            self.delay=60/int(self.serial_cfg.puntos)            
            msg='Iniciacndo bucle de adquisicion de datos'
            logging.info(msg)
                        
            while True:
		logging.debug ('EN Bucle')
                self.ser.read(self.ser.in_waiting)
                data=[]
		logging.debug('Creado array')
                logging.debug(str(self.ser.readline())) # Se deacarta primer linea para evitar un dato truncado
                i=range(0,8,1)  
                for i in i:         # se leen 8 lineas consecutivas (1 por canal)
                    
                    data.append( self.ser.readline())
                
                logging.debug(str(data))
    		try:
                    self.save_data(data)
		except:
                    logging.error('Error en save_data')

                time.sleep(self.delay) 
    
            self.ser.close()
            msg='Finalizando proceso de adquisicion'
            logging.info(msg)
            time.sleep(1)
        else:
            sys.exit(2)



    def save_data(self, data):
        from datetime import datetime
        try:
	    channel_cfg = self.db_conn.get_channel_info()
	except:
	    logging.error('Fallo al obtener configuracion de canales')
        try:
	    registro=db.Registro()
	except:
            logging.debug(str(sys.exc_info()[0]))	
        for dato in data:
	    logging.debug('Preparando datos')
	    try:
                channel, value= str(dato).split('  ')
		val, unit= str(value).split(' ')
	    except:
		logging.error('Error en split:'+str(sys.exc_info()[0]))
		sys.exit(2)
	    logging.debug('Datos:'+str(channel)+str(val)+str(unit))
            if channel_cfg.__getattribute__(channel)[2]:
                registro.__setattr__(channel, val)
            else:
                registro.__setattr__(channel, -0.1)
        registro.__setattr__('datetime',datetime.now())
	logging.debug(str(registro))
	try:
        	self.db_conn.insert_data(registro)
	except:
		loggin.error(str(sys.exc_info()[0]))
		        
 
if __name__ == "__main__":
        daemon = ADQ('/tmp/daemon-example.pid')
        if len(sys.argv) == 2:
                if 'start' == sys.argv[1]:
                        daemon.start()
                elif 'stop' == sys.argv[1]:
                        daemon.stop()
                elif 'restart' == sys.argv[1]:
                        daemon.restart()
                else:
                        print "Unknown command"
                        sys.exit(2)
                sys.exit(0)
        else:
                print "usage: %s start|stop|restart" % sys.argv[0]
                sys.exit(2)
