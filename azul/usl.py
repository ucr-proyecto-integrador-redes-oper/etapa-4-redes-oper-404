from validador import Validador
from threading import *
from time import *
from Util import *

import socket

class Usl():
	
	def __init__(self):
		
		self.mi_ip = '127.0.0.1'
		self.mi_puerto = 6854
		self.buffersize = 1035
		self.SN = 0

		# colas necesarias 
		self.recibidos = []
		self.enviados = []
		self.mensajes = []

		# locks necesarios
		self.lock_recibir = Lock()
		self.lock_enviar = Lock()
		
		self.UDPSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		
		# Bind al ip y puerto
		self.UDPSocket.bind((self.mi_ip, self.mi_puerto))
		
		# Hilos de ejecucion
		hilo_timer = Thread(target=self.timer, args=())
		hilo_rec = Thread(target=self.recibir, args=())
		hilo_revisar = Thread(target=self.revisar, args=())

		hilo_timer.start()
		hilo_rec.start()
		hilo_revisar.start()

	#Metodo que envia mensajes utiles	
	def enviar(self, payload, ip, puerto):

		addr = (ip, puerto)
		clientIP = " Client IP: {} Port: {}".format(addr[0], addr[1])
		paquete = (0).to_bytes(1, byteorder="big") + (self.SN).to_bytes(2, byteorder="big") + payload
		self.SN = (self.SN + 1) % 65536
		# print('Estoy aqui.....')
		self.UDPSocket.sendto(paquete, addr)
		paquete_nuevo = (paquete, addr)

		#print("Enviar  " + str(paquete) + " a " + clientIP)

		self.lock_enviar.acquire()

		self.enviados.append(paquete_nuevo)
		
		self.lock_enviar.release()

		
	# Hilo de recibir paquetes
	def recibir(self):
		while True:

			paquete, addr = self.UDPSocket.recvfrom(self.buffersize)
			clientIP = " Client IP: {} Port: {}".format(addr[0], addr[1])
			#print("Recibí " + str(paquete) + " de " + clientIP)
			paquete_nuevo = (paquete, addr)
			
			self.lock_recibir.acquire()

			self.recibidos.append(paquete_nuevo)
			
			self.lock_recibir.release()
			

	#Hilo que revisa la lista de recibidos
	def revisar(self):
		while True:

			if len(self.recibidos):
				paquete = self.recibidos.pop(0)
				clientIP = " Client IP: {} Port: {}".format(paquete[1][0], paquete[1][1])

				# Revisa si es un ACK
				if paquete[0][0] == 1:
				
					SNR = int.from_bytes([paquete[0][1], paquete[0][2]], byteorder='big')  
					#print("ACK de " + clientIP + " RN: " + str(SNR))
					
					self.lock_enviar.acquire()

					for pkt in self.enviados:
						j = 0
						SNE =  int.from_bytes([pkt[0][1], pkt[0][2]], byteorder='big')
						if SNE == SNR: 
							del self.enviados[j]
						j += 1

					self.lock_enviar.release()

				# sino, si es un paquete
				elif paquete[0][0] == 0:
					
					SN = int.from_bytes([paquete[0][1], paquete[0][2]], byteorder='big')
					message = bytearray([1, paquete[0][1], paquete[0][2]])
				
					self.UDPSocket.sendto(message, paquete[1])  # ack enviado
						
					#print("ACK enviado a " + clientIP + " SN: " + str(SN))
					# Guarda mensaje en cola de mensajes
					self.mensajes.append((paquete[0][3:len(paquete[0])], paquete[1])) 
					

	#Hilo que revisa cola de enviados y reenvia
	def timer(self):
		while True:

			sleep(2)

			self.lock_enviar.acquire()

			for paquete, address in self.enviados:
				self.UDPSocket.sendto(paquete, address)

			self.lock_enviar.release()



	#Método para obtener mensajes 
	def getPaquete(self):
		while True:

			if len(self.mensajes):
				return self.mensajes.pop(0) 	
				
	

# Para pruebas con el secure
def main():
	
	prueba_secure = UDP_seguro()
	valida = Validador()

	# prueba de enviar SecureUDP
	def prueba_enviar():
		while True:
			
			print('Introduzca IP:')
			ip = input()
			if not valida.ip_valida(ip):
				print('---------- IP INVALIDO ----------')
				
			print('Introduzca Puerto:')
			puerto = input()
			if not valida.puerto_valido(puerto):
				print('---------- Puerto INVALIDO ----------')
				
			print('Introduzca Mensaje:')
			mensaje = input()

			if valida.ip_valida(ip) and valida.puerto_valido(puerto):
				prueba_secure.enviar(mensaje.encode('utf-8'), ip, int(puerto))
				sleep(1)
			else:
				print('Vuelva a introducir los datos...')

	# Prueba de recibir SecureUDP
	def prueba_recibir():
		while True:
			msj = prueba_secure.getPaquete()
			print(f"Mensaje Recibido: {msj}")

	t1 = Thread(target=prueba_enviar)
	t1.start()

	t2 = Thread(target=prueba_recibir)
	t2.start()


if __name__ == '__main__':
	main()
