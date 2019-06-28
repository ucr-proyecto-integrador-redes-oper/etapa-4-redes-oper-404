from threading import *
from struct import *
import csv
from Paquetes import *
import socket
import sys
import time

class Naranja():
	

	def __init__(self): 
			
		#cola de paquetes
		self.paquetes=[]

		
		#variables para conexion UDP
		self.mi_ip='10.1.137.137'
		self.mi_port   = 3939
		self.bufferSize  = 1035
		self.UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)


		# Bind to address and ip

		self.UDPServerSocket.bind((self.mi_ip, self.mi_port))
		#self.vecino=('10.1.137.154', 2909)
		
		self.reenviar=0
		self.sn=1


		print("UDP server up and listening")
		#self.primero=pack('ch4p', '0'.encode(), self.sn,'hola'.encode())
		#aquete_nuevo = [self.primero, self.vecino]
		#self.paquetes.append(paquete_nuevo)
		#self.llego=1

		

		


		self.mutex = Lock()
	
	#thread que solo envia
	def enviar_naranja_naranja(self):

		while True:
			self.mutex.acquire()
			if len(self.paquetes):
				paquete=self.paquetes.pop()
				#print(paquete)
				if str(chr(paquete[0][0]))=='0':
					paquete_aux=unpack('ch4p', paquete[0])
					print('ENVIA SN  '+ str(paquete_aux[1]) + ' IP: ' +self.vecino[0]+ '  puerto: '+ str(self.vecino[1]) )
					self.llego= self.llego+1

				if str(chr(paquete[0][0]))=='1':
					print('Responde Ack' + 'IP: ' +self.vecino[0]+ 'puerto: '+ str(self.vecino[1]) )
				
				self.UDPServerSocket.sendto(paquete[0], paquete[1])

			self.mutex.release()
			

			
			
	def create_pack_0(self,tipo,SN):
		return pack('ch', tipo.encode(), SN)

	#paso cadena de bytes a paquete python para procesar
	def unpack_pack_0(self, byte_pack):
		
		datos=unpack('ch', byte_pack)
		
		return datos






	#thread que recibe paquetes
	def recibir_naranja_naranja(self):
		
		while True:

			bytesAddressPair = self.UDPServerSocket.recvfrom(self.bufferSize)


			paquete = bytesAddressPair[0]
			address=bytesAddressPair[1]
			clientIP  = "Client IP Address:{}".format(address)
		
			paquete_nuevo = []
			


			self.mutex.acquire()


			#verficio si es token inicial
			if paquete[0]==0:
				#paso de bytes a paquetes para procesar
				
				
				
				#print y proceso el paquete
				print('Recibi SN: ' + str(paquete)+ clientIP)

				paquete=pack('Bh', 1, paquete[1])
				paquete_nuevo=[paquete, address]
				self.paquetes.append(paquete_nuevo)

			#verifico si es paquete token
			elif paquete[0]==1:
				print('Recibi ACK: ' + clientIP)
				self.llego=self.llego-1
				self.sn=self.sn+1
				#print y proceso el paquete



			self.mutex.release()

	def timer(self):
		while True:
			if self.llego!=0:
				time.sleep(60)
				self.reenviar=1







			
def main():
	n_naranja = Naranja()
	

	t1=Thread(target=n_naranja.recibir_naranja_naranja)
	t2=Thread(target=n_naranja.enviar_naranja_naranja)
		
	t1.start()
	t2.start()
	t1.join()
	t2.join()

	#n_naranja.leer_grafo()
	#print(n_naranja.buscar_nodo())

		#t3=Thread(target=n_naranja.input_consola).start()


if __name__ == '__main__':
	main()


		
	
