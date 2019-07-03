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
		self.ip_naranja=0


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
		data=pack('B',tipo)
		data+=pack('H',nodo)
		data+=pack('>I',ip_azul)
		data+=pack('H',puerto_azul)
		return data

	def create_pack_15(self,usl,sn,tipo,nodo,vecino):
		data=pack('B',usl)
		data+=pack('>H',sn)
		data+=pack('B',tipo)
		data+=pack('>H',nodo)
		data+=pack('>H',vecino)
		return data

	def create_pack_16(self,usl,sn,tipo,nodo, vecino, ip_azul, puerto_azul,):
		data=pack('B',usl)
		data+=pack('>H',sn)
		data+=pack('B',tipo)
		data+=pack('>H',nodo)
		data+=pack('>H',vecino)
		data+=pack('>I',ip_azul)
		data+=pack('>H',puerto_azul)
		return data


	#paso cadena de bytes a paquete python para procesar
	def unpack_pack_asignacion(self, byte_pack):
		paquete=paquete_asignacion()
		paquete.tipo=byte_pack[0]
		paquete.ip_azul=str(IPv4Address(byte_pack[3:7]))
		nodo=unpack('H',byte_pack[1:3])
		puerto_azul=unpack('H',byte_pack[7:9])
		paquete.nodo=nodo[0]
		paquete.puerto_azul=puerto_azul[0]
		return paquete



	def imprimir_inicial(self, paquete):
		print(str(paquete.tipo)+ ' '+str(paquete.ip_naranja))


	def imprimir_token(self, paquete):
		print('me llego '+str(paquete.tipo)+ ' ' +  str(paquete.nodo)+' ' +str(paquete.ip_azul)+' '+ str(paquete.puerto_azul) )

	def unpack_pack_azul(self, byte_pack):
		paquete=paquete_azul()
		paquete.tipo=byte_pack[3]
		paquete.usl=byte_pack[0]
		sn=unpack('h',byte_pack[1:3])
		paquete.sn=sn[0]
		return paquete


	#creo cadena de bytes
	def create_pack_inicial(self, tipo, ip_naranja):
		data=pack('B',tipo)
		data+=pack('>I',ip_naranja)
		return data


	#paso cadena de bytes a paquete python para procesar
	def unpack_pack_inicial(self, byte_pack):
		paquete=paquete_inicial()
		paquete.tipo=byte_pack[0]
		paquete.ip_naranja=str(IPv4Address(byte_pack[1:5]))
		return paquete


	#creo cadena de bytes
	def create_pack_complete(self, tipo):
		return  pack('B', tipo)


	#paso cadena de bytes a paquete python para procesar
	def unpack_pack_complete(self, byte_pack):
		paquete=paquete_complete()
		paquete.tipo=byte_pack[0]
		return paquete

	#creo cadena de bytes
	def create_pack_vacio(self, tipo):
		return  pack('B', tipo)


	#paso cadena de bytes a paquete python para procesar
	def unpack_pack_vacio(self, byte_pack):
		paquete=paquete_vacio()
		paquete.tipo=byte_pack[0]
		return paquete
