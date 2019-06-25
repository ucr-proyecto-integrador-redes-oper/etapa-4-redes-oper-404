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
		self.mi_port   = 5005
		self.bufferSize  = 1024
		self.UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)


		# Bind to address and ip

		self.UDPServerSocket.bind((self.mi_ip, self.mi_port))
		self.vecino=('10.1.138.212', 8888)


		print("UDP server up and listening")
		# self.primero=pack('ch', '0'.encode(), 1)
		# self.paquetes.append(self.primero)

		

		


		self.mutex = Lock()
	
	#thread que solo envia
	def enviar_naranja_naranja(self):

		while True:
			self.mutex.acquire()
			if len(self.paquetes):
				paquete=self.paquetes.pop()
				#print(paquete)
				if str(chr(paquete[0]))=='0':
					paquete_aux=unpack('ch', paquete)
					print('ENVIA SN  '+ str(paquete_aux[1]) + ' IP: ' +self.vecino[0]+ '  puerto: '+ str(self.vecino[1]) )

				if str(chr(paquete[0]))=='1':
					print('Responde Ack' + 'IP: ' +self.vecino[0]+ 'puerto: '+ str(self.vecino[1]) )
				
				self.UDPServerSocket.sendto(paquete, self.vecino)

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


			self.mutex.acquire()


			#verficio si es token inicial
			if str(chr(paquete[0]))=='0':
				#paso de bytes a paquetes para procesar
				paquete_inicial=self.unpack_pack_0(paquete)
				
				
				#print y proceso el paquete
				print('Recibi SN: ' + paquete_inicial+ ClientIP[0]+ClientIP[1])

				paquete=pack('c', '1')
				self.paquetes.append(paquete)

			#verifico si es paquete token
			elif str(chr(paquete[0]))=='1':
				
				print('Recibi ACK: ' + ClientIP)
				#print y proceso el paquete



			self.mutex.release()




			
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


		
	
