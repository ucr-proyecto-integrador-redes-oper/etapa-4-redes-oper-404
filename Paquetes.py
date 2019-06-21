from struct import *

#paquetes estilo python para facilidad de procesamiento
#paquetes estilo python para facilidad de procesamiento
#paquetes estilo python para facilidad de procesamiento
#paquetes estilo python para facilidad de procesamiento
class paquete_asignacion:
	def __init__(self):
		self.tipo = '1'
		self.ip_azul=''
		self.puerto_azul=''
		self.nodo=0



class paquete_inicial:
	def __init__(self):
		self.tipo = '0'
		self.ip_naranja=''
		self.elegido=''

class paquete_vacio:
	def __init__(self):
		self.tipo = '3'
		

class paquete_complete:
	def __init__(self):
		self.tipo = '2'
		
#clase encargada de procesar paquetes en bytes
class Paquetes():
	
	def __init__(self):
		pass

	#creo cadena de bytes 
	def create_pack_asignacion(self,tipo,nodo, ip_azul, puerto_azul):
		return pack('ch15ph', tipo.encode(), nodo, ip_azul.encode(), puerto_azul)

	#paso cadena de bytes a paquete python para procesar
	def unpack_pack_asignacion(self, byte_pack):
		paquete=paquete_asignacion()
		datos=unpack('ch15ph', byte_pack)
		paquete.tipo=datos[0].decode('utf-8')
		paquete.ip_azul=datos[2].decode('utf-8')
		paquete.nodo=datos[1]
		paquete.puerto_azul=datos[3]
		return paquete


	def imprimir_inicial(self, paquete):
		print(paquete.tipo + ' '+paquete.ip_naranja+' ' + paquete.elegido)


	def imprimir_token(self, paquete):
		print('me llego '+paquete.tipo + ' ' +  str(paquete.nodo)+' ' +paquete.ip_azul+' '+ str(paquete.puerto_azul) )
		

	# def unpack_pack_azul(self, byte_pack):
	# 	paquete=paquete_azul()
	# 	datos=unpack('c15phh',byte_pack)
	# 	paquete.tipo=datos[0].decode('utf-8')
	# 	paquete.ip_azul=datos[1].decode('utf-8')
	# 	paquete.puerto_azul=datos[2].decode('utf-8')
	# 	paquete.nodo=datos[3]
		
	# 	return paquete

	#creo cadena de bytes 
	def create_pack_inicial(self, tipo, ip_naranja):
		return  pack('c15p', tipo.encode(), ip_naranja.encode())

	
	#paso cadena de bytes a paquete python para procesar
	def unpack_pack_inicial(self, byte_pack):
		paquete=paquete_inicial()
		datos=unpack('c15p', byte_pack)
		paquete.tipo=datos[0].decode('utf-8')
		paquete.ip_naranja=datos[1].decode('utf-8')
		return paquete


	#creo cadena de bytes 
	def create_pack_complete(self, tipo):
		return  pack('c', tipo.encode()())

	
	#paso cadena de bytes a paquete python para procesar
	def unpack_pack_complete(self, byte_pack):
		paquete=paquete_complete()
		datos=unpack('c', byte_pack)
		paquete.tipo=datos[0].decode('utf-8')
		return paquete

	#creo cadena de bytes 
	def create_pack_vacio(self, tipo):
		return  pack('c', tipo.encode())

	
	#paso cadena de bytes a paquete python para procesar
	def unpack_pack_vacio(self, byte_pack):
		paquete=paquete_vacio()
		datos=unpack('c', byte_pack)
		paquete.tipo=datos[0].decode('utf-8')
		return paquete

		
	
