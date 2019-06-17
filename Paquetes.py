from struct import *

#paquetes estilo python para facilidad de procesamiento
#paquetes estilo python para facilidad de procesamiento
#paquetes estilo python para facilidad de procesamiento
#paquetes estilo python para facilidad de procesamiento
class paquete_token:
	def __init__(self):
		self.token = ''
		self.tipo = 'T'
		self.ip_naranja=''
		self.ip_azul=''
		self.puerto_azul=''
		self.subtipo=''
		self.nodo=0


class paquete_azul:
	def __init__(self):
		self.tipo = 'T'
		self.ip_azul=''
		self.puerto_azul=''
		self.nodo=0

class paquete_inicial:
	def __init__(self):
		self.tipo = 'I'
		self.ip_naranja=''
		self.elegido=''


#clase encargada de procesar paquetes en bytes
class Paquetes():
	
	def __init__(self):
		pass

	#creo cadena de bytes 
	def create_pack_token(self,tipo, token, ip_naranja, ip_azul, nodo,subtipo, puerto_azul):
		return pack('cc15p15phch', tipo.encode(), token.encode(), ip_naranja.encode(), ip_azul.encode(),  nodo , subtipo.encode(), puerto_azul)

	#paso cadena de bytes a paquete python para procesar
	def unpack_pack_token(self, byte_pack):
		paquete=paquete_token()
		datos=unpack('cc15p15phch', byte_pack)
		paquete.tipo=datos[0].decode('utf-8')
		paquete.token=datos[1].decode('utf-8')
		paquete.ip_naranja=datos[2].decode('utf-8')
		paquete.ip_azul=datos[3].decode('utf-8')
		paquete.nodo=datos[4]
		paquete.subtipo=datos[5].decode('utf-8')
		paquete.puerto_azul=datos[6]
		return paquete


	def imprimir_inicial(self,paquete):
		print(paquete.tipo + ' '+paquete.ip_naranja+' ' + paquete.elegido)


	def imprimir_token(self,paquete):
		print(paquete.tipo + ' ' + paquete.token+' ' + paquete.ip_naranja+' ' + paquete.ip_azul+' ' + str(paquete.nodo)+' ' + paquete.subtipo+' ' + str(paquete.puerto_azul) )
		

	# def unpack_pack_azul(self, byte_pack):
	# 	paquete=paquete_azul()
	# 	datos=unpack('c15phh',byte_pack)
	# 	paquete.tipo=datos[0].decode('utf-8')
	# 	paquete.ip_azul=datos[1].decode('utf-8')
	# 	paquete.puerto_azul=datos[2].decode('utf-8')
	# 	paquete.nodo=datos[3]
		
	# 	return paquete

	#creo cadena de bytes 
	def create_pack_inicial(self, tipo, ip_naranja, elegido):
		return  pack('c15pc', tipo.encode(), ip_naranja.encode(), elegido.encode())

	
	#paso cadena de bytes a paquete python para procesar
	def unpack_pack_inicial(self, byte_pack):
		paquete=paquete_inicial()
		datos=unpack('c15pc', byte_pack)
		paquete.tipo=datos[0].decode('utf-8')
		paquete.ip_naranja=datos[1].decode('utf-8')
		paquete.elegido=datos[2].decode('utf-8')
		return paquete

		
	
