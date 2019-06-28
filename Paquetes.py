from struct import *
from ipaddress import*

#paquetes estilo python para facilidad de procesamiento
#paquetes estilo python para facilidad de procesamiento
#paquetes estilo python para facilidad de procesamiento
#paquetes estilo python para facilidad de procesamiento
class paquete_asignacion:
	def __init__(self):
		self.tipo = 0
		self.ip_azul=''
		self.puerto_azul=0
		self.nodo=0



class paquete_inicial:
	def __init__(self):
		self.tipo = 0
		self.ip_naranja=''
		self.elegido=0

class paquete_vacio:
	def __init__(self):
		self.tipo =0



class paquete_azul:
	def __init__(self):
		self.tipo = 0
		self.usl=0
		self.sn=0
		

class paquete_complete:
	def __init__(self):
		self.tipo = 0


		
		
#clase encargada de procesar paquetes en bytes
class Paquetes():
	
	def __init__(self):
		pass

	#creo cadena de bytes 
	def create_pack_asignacion(self,tipo,nodo, ip_azul, puerto_azul):
		return pack('BhIh', tipo, nodo, ip_azul, puerto_azul)

	#paso cadena de bytes a paquete python para procesar
	def unpack_pack_asignacion(self, byte_pack):
		paquete=paquete_asignacion()
		datos=unpack('BhIh', byte_pack)
		paquete.tipo=datos[0]
		paquete.ip_azul=str(IPv4Address(datos[2]))
		paquete.nodo=datos[1]
		paquete.puerto_azul=datos[3]
		return paquete


	
	def imprimir_inicial(self, paquete):
		print(str(paquete.tipo)+ ' '+str(paquete.ip_naranja)+' ' + paquete.elegido)


	def imprimir_token(self, paquete):
		print('me llego '+str(paquete.tipo)+ ' ' +  str(paquete.nodo)+' ' +str(paquete.ip_azul)+' '+ str(paquete.puerto_azul) )

	def unpack_pack_azul(self, byte_pack):
		paquete=paquete_azul()
		datos=unpack('BhB',byte_pack)
		paquete.tipo=datos[0]
		paquete.usl=datos[1]
		paquete.sn=datos[2]
	
		return paquete


	#creo cadena de bytes 
	def create_pack_inicial(self, tipo, ip_naranja):
		return  pack('BI', tipo, ip_naranja)

	
	#paso cadena de bytes a paquete python para procesar
	def unpack_pack_inicial(self, byte_pack):
		paquete=paquete_inicial()
		datos=unpack('BI', byte_pack)
		paquete.tipo=datos[0]
		paquete.ip_naranja=datos[1]
		return paquete


	#creo cadena de bytes 
	def create_pack_complete(self, tipo):
		return  pack('B', tipo)

	
	#paso cadena de bytes a paquete python para procesar
	def unpack_pack_complete(self, byte_pack):
		paquete=paquete_complete()
		datos=unpack('B', byte_pack)
		paquete.tipo=datos[0]
		return paquete

	#creo cadena de bytes 
	def create_pack_vacio(self, tipo):
		return  pack('B', tipo)

	
	#paso cadena de bytes a paquete python para procesar
	def unpack_pack_vacio(self, byte_pack):
		paquete=paquete_vacio()
		datos=unpack('B', byte_pack)
		paquete.tipo=datos[0]
		return paquete

		
	
