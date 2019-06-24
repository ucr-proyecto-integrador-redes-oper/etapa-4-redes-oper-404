from threading import *
from struct import *
import csv
from Paquetes import *
import socket
import sys
import time

class Naranja():
	
	def __init__(self): 
		self.completos=0

		#cola de solicitudes de nodos azules
		self.solicitudes = [['255.234.234.255', 9999]]
		#cola de nodos muertos de nodos azules
		self.muertos=[['255.234.234.255',1, 6666], ['253.234.234.255',2, 6667], ['255.234.234.222',3, 7666]]
		
		#Banderas para manejo de paquetes
		self.completo=0
		self.token=0
		self.inicial=0
		
		#lista de nodos activos'
		self.nodos_grafo = []
		

		#cola de paquetes
		self.paquetes=[]

		#almacena todo el grafo
		self.grafo=[]
		
		self.packs=Paquetes()

		#avisa que llegan los paquetes para el timer con llego=1 avisa que llego el paquete y reenviar=1 acabo el timer
		self.llego=-1
		self.reenviar=0

		#variables para conexion UDP
		self.mi_ip='localhost'
		self.mi_port   = 7777
		self.bufferSize  = 1024
		self.UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)



		# Bind to address and ip

		self.UDPServerSocket.bind((self.mi_ip, self.mi_port))
		self.vecino=(self.mi_ip, 8888)



		print("UDP server up and listening")


		self.mutex = Lock()
		
	#lee el csv y crea el grafo
	def leer_grafo(self):
		with open('grafo_prueba.csv', newline='') as File:  
			reader = csv.reader(File)
			for row in reader:
				self.grafo.append(row)

		print(self.grafo)
				

	#busca posible nodos libres dentro del grafo y da -1 si no hay disponibles
	def buscar_nodo(self):
		
		for f in range(len(self.grafo)):
			for c in range(len(self.grafo[0])):
				existe=False
				if self.grafo[f][c]!='':
				
					if self.nodos_grafo !=[]:
						
						for temp in self.nodos_grafo:
							if int(self.grafo[f][c]) in temp:
								existe=True

						if not existe:
							return self.grafo[f][c]
							
					else:
					
						return self.grafo[f][c]
					
					

		return -1


	#inicio del proceso
	def inicio(self):
		while True:
			
			senal = input()
			#al todos estar levantados se escribe start en consola
			if senal=='start':
				break
		
		#se crea el token inicial y se pone llego=0 para esperar que llegue con el timer
		paquete=self.packs.create_pack_inicial('0', self.mi_ip)
		self.llego=0
		

		#se lee el grafo al inicio
		self.leer_grafo()
	
		#lock
		
		self.paquetes.append(paquete)
		return True
		#unlock



	#procesamiento azul-azul
	def procesar_azul(self, paquete):
		
		
		if paquete.tipo== '14':
			aux=[paquete.ip_azul, paquete.puerto_azul]
			solicitudes.append(aux)


		elif paquete.tipo== '17':
			self.completo=1

	
			
		
			

	

	#procesmaiento del paquete
	def procesar_paquete(self,paquete, paquete_enviar):
		
	#si es igual ip me llego el paquete que envie y libero el token

	
		#en caso de disponibilidad del token
		if paquete.tipo== '3':
			
			
			#reviso si tengo solicitudes y en caso de tenerlas creo paquete solicitud para mi azul			
			if len(self.solicitudes):
				
				aux=self.solicitudes.pop()
				nodo=self.buscar_nodo()
				if nodo!= -1:
					print('encontro'+ str(nodo))
					
					self.nodos_grafo.append([int(nodo), aux[0], aux[1]])
					print(self.nodos_grafo)
					#para control con timer
					self.llego=0
					paquete_enviar= self.packs.create_pack_asignacion('1' , int(nodo) , aux[0], aux[1])
					self.token=1
					#paquete_azul= self.packs.create_pack_asignacion()

						
			#reviso si tengo posibles reportados muertos 		
			#elif len(self.muertos):
				#aux=self.muertos.pop()
				#para control con timer
				#self.llego=0
				#paquete_enviar= self.packs.create_pack_token('T' , '1' ,  self.mi_ip , paquete.ip_azul , aux[1] , 'D' , paquete.puerto_azul)
				
			#reviso si mis nodos azules estan completos		
			elif self.completo:
				#para control con timer
				self.llego=0
				self.token=1
				paquete_enviar= self.packs.create_pack_complete('2')
		
			self.paquetes.append(paquete_enviar)
	
		#caso del que el token esta ocupado		
		elif paquete.tipo=='1':
			print('voy a agregar')

			#guardo el nodo que llego de otro naranja en mi lista de nodos ocupados
					
			aux=[paquete.nodo, paquete.ip_azul, paquete.puerto_azul]
					
			if aux in self.nodos_grafo:
				paquete_enviar= self.packs.create_pack_vacio('3')
				self.token=0
			
			else:
				self.nodos_grafo.append(aux)
		
				print(self.nodos_grafo)
			
				self.paquetes.append(paquete_enviar)

				


			#elimino el nodo muerto de mi lista de nodo activos
			#elif paquete.subtipo=='D':
				
				#paquete_enviar= self.packs.create_pack_token('T' , '1' ,  paquete.ip_naranja , paquete.ip_azul , paquete.nodo  , 'D' , paquete.puerto_azul)

				#for temp in self.nodos_grafo:
					#if paquete.nodo in temp:
						#self.nodos_grafo.remove(temp)					
				
		#procesamientos paquete complete
		elif paquete.tipo=='2':
				
			if self.token:
				paquete_enviar= self.packs.create_pack_vacio('3')
				self.token=0	
			
			else:
				self.completos = self.completos + 1
				#if completos == cant_nodos
				#	send paquete 
				
			self.paquetes.append(paquete_enviar)
		

		elif paquete.tipo=='0':
			
			
			if paquete.ip_naranja != self.mi_ip:
			
				#reviso ip a ver si gana el que llego y lo modifico en caso de 
				if paquete.ip_naranja < self.mi_ip:
					self.inicial=self.inicial+1		 
						
				self.paquetes.append(paquete_enviar)
			

			#ya me llego mi token inicial...				
			if self.inicial==2:
				
				#veo si soy el elegido y creo un token inicial con solicitud en caso de tenerla y si no solo lo paso a mi vecino
				
				aux=['',0]
				
				nodo=self.buscar_nodo()
				if len(self.solicitudes):
					aux=self.solicitudes.pop()
					if nodo!= -1:
						print('encontro')
						
						self.nodos_grafo.append([int(nodo), aux[0], aux[1]])
						print(self.nodos_grafo)
						#para control con timer
						self.llego=0
						paquete_enviar= self.packs.create_pack_asignacion('1' , int(nodo), aux[0], aux[1])
						self.token=1

		
						self.paquetes.append(paquete_enviar)
				
				

	

	#thread que solo envia
	def enviar_naranja_naranja(self):

		while True:
			self.mutex.acquire()
			if len(self.paquetes):
				paquete=self.paquetes.pop()
				#paquete auxiliar por si se pierde el que envie
				paquete_respaldo=paquete
				#print(paquete)
				if str(chr(paquete[0]))!='3':
					print('voy a enviar ' + str(paquete))
				self.UDPServerSocket.sendto(paquete, self.vecino)

			self.mutex.release()
			#cuando esto se cumpla significa que envia un paquete, el timer se vencio y no me llego entonces reeenvio y reinicio timer 
			if self.reenviar==1 and self.llego==0:
				self.UDPServerSocket.sendto(paquete_respaldo, self.vecino)
				self.reenviar=0
				

			
			
	




	#thread que recibe paquetes
	def recibir_naranja_naranja(self):
		
		while True:

			bytesAddressPair = self.UDPServerSocket.recvfrom(self.bufferSize)

			paquete = bytesAddressPair[0]


			self.mutex.acquire()


			#verficio si es token inicial
			if str(chr(paquete[0]))=='0':
				#paso de bytes a paquetes para procesar
				paquete_inicial=self.packs.unpack_pack_inicial(paquete)
				
				
				#print y proceso el paquete
				print('me llego ' + str(paquete))
				self.procesar_paquete(paquete_inicial,paquete)

			#verifico si es paquete token
			elif str(chr(paquete[0]))=='1':
				#paso de bytes a paquetes para procesar
				paquete_asignacion=self.packs.unpack_pack_asignacion(paquete)
				#llego mi paquete cierro el timer
				if self.token:
					self.llego=1
				
				#print y proceso el paquete
				self.packs.imprimir_token(paquete_asignacion)
				
				self.procesar_paquete(paquete_asignacion,paquete)

			elif str(chr(paquete[0]))=='2':
				#paso de bytes a paquetes para procesar
				paquete_complete=self.packs.unpack_pack_complete(paquete)
				#llego mi paquete cierro el timer
				if self.token:
					self.llego=1
				
				#print y proceso el paquete
				print('me llego ' + str(paquete))
				
				self.procesar_paquete(paquete_complete,paquete)
			
			elif str(chr(paquete[0]))=='3':
				#paso de bytes a paquetes para procesar
				paquete_vacio=self.packs.unpack_pack_vacio(paquete)
				#llego mi paquete cierro el timer
				if self.token:
					self.llego=1
				
				#print y proceso el paquete
				#print('me llego ' + str(paquete))
				
				self.procesar_paquete(paquete_vacio,paquete)


			self.mutex.release()


# AZUL-NARANJA EN PROCESO
	def enviar_naranja_azul(self):

		while True:
			#lock

			if len(self.paquetes_azules):
				paquete=self.paquetes_azules.pop()
				

			#unlock
			#send secure udp
			

	def recibir_azul_naranja(self):
		
		while True:

			#paquete=secure_udp

			elif str(chr(paquete[0]))=='14':
				#paso de bytes a paquetes para procesar
				paquete_join_graph=self.packs.unpack_pack_join_graph(paquete)
				
				#print y proceso el paquete
				print('me llego ' + str(paquete))
				
				self.procesar_azul(paquete_join_graph)
			
			elif str(chr(paquete[0]))=='17':
				#paso de bytes a paquetes para procesar
				paquete_complete_azul=self.packs.unpack_pack_complete_azul(paquete)
					
				#print y proceso el paquete
				print('me llego ' + str(paquete))
				
				self.procesar_azul(paquete_complete_azul)

			

			


	#Manejo de input 
	def input_consola(self):
		while True:
			nombre=input()
			if nombre=='exit':
				quit()


	#thread del timer
	def timer(self):
		while True:
			if self.llego==0:
				time.sleep(180)
				self.reenviar=1




			
def main():
	n_naranja = Naranja()
	
	if n_naranja.inicio():
		t1=Thread(target=n_naranja.recibir_naranja_naranja)
		t2=Thread(target=n_naranja.enviar_naranja_naranja)
		t3=Thread(target=n_naranja.timer)
		t1.start()
		t2.start()
		t3.start()
		t3.join()
		t1.join()
		t2.join()

	#n_naranja.leer_grafo()
	#print(n_naranja.buscar_nodo())

		#t3=Thread(target=n_naranja.input_consola).start()


if __name__ == '__main__':
	main()


		
	
