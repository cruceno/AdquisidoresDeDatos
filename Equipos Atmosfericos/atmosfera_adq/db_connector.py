#!/home/sistemas/atmosfera_adq/env/bin/python
# -*- coding: utf-8 -*-
'''
Created on 26 de ene. de 2016

@author: javit
'''
import MySQLdb

class Serial_CFG(object):
    def __init__(self):
        self.port=""
        self.baudrate=""
        self.stopbits=""
        self.parity=""
        self.bytesize=""
        self.puntos=""
        
class Channel_CFG(object):
    def __init__(self):
        self.C1=["","",0]
        self.C2=["","",0]
        self.C3=["","",0]
        self.C4=["","",0]
        self.C5=["","",0]
        self.C6=["","",0]
        self.C7=["","",0]
        self.C8=["","",0]
class Registro(object):
    def __init__(self):
        self.datetime=""
        self.C1=""
        self.C2=""
        self.C3=""
        self.C4=""
        self.C5=""
        self.C6=""
        self.C7=""
        self.C8=""
class db ():    
    def __init__(self,datos):
        
        self.datos = [datos[0].replace('\r\n',''),datos[1].replace('\r\n',''),datos[2].replace('\r\n',''),datos[3].replace('\r\n','')]
        
    def test_db(self):
        try:
            conn = MySQLdb.connect(*self.datos) # Conectar a la base de datos 
            conn.close()
            return True
        except:
            return False
    def get_serial_config(self):
        serial_cfg=Serial_CFG()

        conn = MySQLdb.connect(*self.datos) # Conectar a la base de datos 
        cursor = conn.cursor()              # Crear un cursor 
        
        query='SELECT * FROM `serial`'
        cursor.execute(query)
        table=cursor.fetchall()
        cursor.close()
        conn.close()
        for row in table:
            serial_cfg.__setattr__(row[0],row[1])
        return serial_cfg
    
    def update_serial_config(self, serial_cfg):
        
        conn = MySQLdb.connect(*self.datos) # Conectar a la base de datos 
        cursor = conn.cursor()              # Crear un cursor 
        querys=[]
        
        querys.append("UPDATE `serial` SET `valores` = '" +serial_cfg.port+"' WHERE `serial`.`parametros`='port'") 
        querys.append("UPDATE `serial` SET `valores` = '" +serial_cfg.baudrate+"' WHERE `serial`.`parametros`='baudrate'")
        querys.append("UPDATE `serial` SET `valores` = '" +serial_cfg.stopbits+"' WHERE `serial`.`parametros`='stopbits'")
        querys.append("UPDATE `serial` SET `valores` = '" +serial_cfg.parity+"' WHERE `serial`.`parametros`='parity'")
        querys.append("UPDATE `serial` SET `valores` = '" +serial_cfg.bytesize+"' WHERE `serial`.`parametros`='bytesize'")
        querys.append("UPDATE `serial` SET `valores` = '" +serial_cfg.puntos+"' WHERE `serial`.`parametros`='puntos'")
        for query in querys:
            
            cursor.execute(query)
            conn.commit()
        
        conn.close()
        
    def get_channel_info(self):
        channel_cfg=Channel_CFG()

        conn = MySQLdb.connect(*self.datos) # Conectar a la base de datos 
        cursor = conn.cursor()              # Crear un cursor 
        
        query='SELECT * FROM `channels`'
        cursor.execute(query)
        table=cursor.fetchall()
        cursor.close()
        conn.close()
        for row in table:
            channel_cfg.__setattr__(row[0],[row[1],row[2],row[3]])
        return channel_cfg
    
    def update_channel_info(self, channels_cfg):
        
        conn = MySQLdb.connect(*self.datos) # Conectar a la base de datos 
        cursor = conn.cursor()              # Crear un cursor 
        querys=[]
        
        for i in range(1,9,1):
            key='C'+str(i)
            querys.append("UPDATE `channels` SET `model`='"+channels_cfg.__getattribute__(key)[0]
                                        +"',`description`='"+channels_cfg.__getattribute__(key)[1]
                                        +"',`status`='"+str(channels_cfg.__getattribute__(key)[2])
                                        +"' WHERE `channels`.`channel`='"+key+"'")
        
        for query in querys:
            cursor.execute(query)
            conn.commit()
        
        conn.close()
        
    def get_status(self):
        pass
    def set_status(self):
        pass
    
    def insert_data(self, registro):
        conn = MySQLdb.connect(*self.datos) # Conectar a la base de datos 
        cursor = conn.cursor()              # Crear un cursor 
       
        # Dar formato a la query para que se correspondan con la base de datos a ser utilizada
        
        # Agrega a la lista de campos que se van a ingresar el datetime.
        lisr_of_chanels=[('datetime',registro.datetime)] 
        
        # Estructura tabla data datetime (DATETIME) C1(FLOAT) C2 (FLOAT) C3 (FLOAT) C4 (FLOAT)... C8 (FLOAT)
        # Inicia la primer parte de la query que contiene lo campos que se van a ingresar. 

        campos = "INSERT INTO `data` (`datetime`,  `C1`, `C2`, `C3`, `C4`, `C5`, `C6`, `C7`, `C8`) "
        
        # Inicia la segunda parte de la query que contiene lo valores. 
        valores =" VALUES ('{datetime}','{C1}', '{C2}', '{C3}', '{C4}', '{C5}', '{C6}', '{C7}', '{C8}')"
        
        for i in range(1,9,1):
            try:
                lisr_of_chanels.append(('C'+str(i),registro.__getattribute__('C'+str(i))))
            except:
                lisr_of_chanels.append(('C'+str(i),0.0))
        
        # dict() crea un diccionario a partir de una lista de tuplas lista =[(clave, valor), (clave2, valor2)]
        
        query=campos+valores.format(**dict(lisr_of_chanels)) #Genera la queri pasando un diccionario como referencia.
        
        cursor.execute(query) # Ejecuta la query
        conn.commit() # Confirma registro en la base de datos
        conn.close() # Cierra la conexion
    
    def select_data(self):
            # Dar formato a la query para que se correspondan con la base de datos a ser utilizada
            query = "SELECT b1, b2 FROM b ORDER BY b2 DESC" 
            result = self.run_query(query) 
            return result


        
