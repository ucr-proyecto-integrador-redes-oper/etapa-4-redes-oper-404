from threading import *
from struct import *
import csv
from Paquetes import *
import socket
import sys
import time
from ipaddress import*




class Naranja():

	def __init__(self):
		self.completos=0

		#cola de solicitudes de nodos azules
		self.solicitudes = []
		self.solicitudes_listas=[]
		#cola de nodos muertos de nodos azules
		self.muertos=[['255.234.234.255',1, 6666], ['253.234.234.255',2, 6667], ['255.234.234.222',3, 7666]]

		#Banderas para manejo de paquetes
		self.completo=0
		self.token=0
		self.inicial=0
		self.azules=0
		self.timer = Event()
		self.termino=1
		self.mando=0
		self.total_naranjas=int(sys.argv[1])
		self.total_azules=int(sys.argv[2])
		self.soy_generador=0

		#lista de nodos activos'
		self.nodos_grafo = []


		#cola de paquetes
		self.paquetes_naranjas=[]
		self.paquetes_azules=[]
		self.sn_azul=0

		#almacena todo el grafo
		self.grafo=[]

		self.packs=Paquetes()

		#avisa que llegan los paquetes para el timer con llego=1 avisa que llego el paquete y reenviar=1 acabo el timer
		self.llego_naranja=-1
		self.reenviar_naranja=0


		self.reenviar_azul=0
		self.llego_azul=0
		self.mi_complete=0




		#variables para conexion UDP
		self.mi_ip= sys.argv[3]
		self.mi_port = 9999
		self.port_azul   = 5005
		self.bufferSize  = 1035
		self.UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
		self.UDPServerazul = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)



		# Bind to address and ip

		self.UDPServerSocket.bind((self.mi_ip, self.mi_port))
		self.UDPServerazul.bind((self.mi_ip, self.port_azul))
		self.vecino=(sys.argv[4], int(sys.argv[5]))



		print("UDP server up and listening")


		self.mutex_naranja = Lock()

		self.mutex_azul = Lock()

	#lee el csv y crea el grafo
	def leer_grafo(self):
		with open('grafo.csv', newline='') as File:
			reader = csv.reader(File)
			for row in reader:
				self.grafo.append(row)

		print(self.grafo)


	#busca posible nodos libres dentro del grafo y da -1 si no hay disponibles
	def buscar_nodo(self):

		for f in range(len(self.grafo)):
			for c in range(len(self.grafo[f])):
				existe=False
				if self.grafo[f][c]!='':

					if self.nodos_grafo !=[]:

						for temp in self.nodos_grafo:
							if int(self.grafo[f][c]) in temp:
								existe=True

						if not existe:
							return int(self.grafo[f][c])

					else:

						return int(self.grafo[f][c])



		return -1



	def buscar_nodo_exist(self,nodo):

		for f in range(len(self.grafo)):
			for c in range(len(self.grafo[f])):
				if self.grafo[f][c]==str(nodo):
					return self.grafo[f]


	#inicio del proceso
	def inicio(self):
		while True:

			senal = input()
			#al todos estar levantados se escribe start en consola
			if senal=='start':
				break

		#se crea el token inicial y se pone llego=0 para esperar que llegue con el timer
		paquete=self.packs.create_pack_inicial(0, int(IPv4Address(self.mi_ip)))
		self.llego_naranja=0
		valor=int(IPv4Address(self.mi_ip))
		print(str(valor))
		print(IPv4Address(valor))
		print(str(IPv4Address(valor)))


		#se lee el grafo al inicio
		self.leer_grafo()

		#lock

		self.paquetes_naranjas.append(paquete)
		return True
		#unlock




	#procesmaiento del paquete
	def procesar_paquete_naranja(self,paquete, paquete_enviar):

	#si es igual ip me llego el paquete que envie y libero el token


		#en caso de disponibilidad del token
		if paquete.tipo == 3:


			#reviso si tengo solicitudes y en caso de tenerlas creo paquete solicitud para mi azul
			if len(self.solicitudes):

				aux=self.solicitudes.pop()
				nodo=self.buscar_nodo()
				if nodo!= -1:
					print('encontro'+ str(nodo))

					self.nodos_grafo.append([nodo, aux[0], aux[1]])
					print(self.nodos_grafo)
					#para control con timer
					
					paquete_enviar= self.packs.create_pack_asignacion(1 , nodo , int(IPv4Address(aux[0])), aux[1])
					self.token=1
					#paquete_azul= self.packs.create_pack_asignacion()


			#reviso si tengo posibles reportados muertos
			#elif len(self.muertos):
				#aux=self.muertos.pop()
				#para control con timer
				#self.llego_naranja=0
				#paquete_enviar= self.packs.create_pack_token('T' , '1' ,  self.mi_ip , paquete.ip_azul , aux[1] , 'D' , paquete.puerto_azul)

			#reviso si mis nodos azules estan completos
			elif self.completo and self.mi_complete:
				print('llego complete1')
				self.completos = self.completos + 1
				self.mi_complete=1
				#para control con timer
				
				self.token=1
				paquete_enviar= self.packs.create_pack_complete(2)

			self.paquetes_naranjas.append(paquete_enviar)

		#caso del que el token esta ocupado
		elif paquete.tipo==1:
			print('voy a agregar')

			#guardo el nodo que llego de otro naranja en mi lista de nodos ocupados

			aux=[paquete.ip_azul, paquete.puerto_azul]

			if aux in self.solicitudes_listas:
				paquete_enviar= self.packs.create_pack_vacio(3)
				self.token=0
				
				self.paquetes_naranjas.append(paquete_enviar)

				vecinos=self.buscar_nodo_exist(paquete.nodo)
				sn_aux=self.sn_azul
				print(vecinos)
				self.mutex_azul.acquire()
				if self.azules==self.total_azules:
					self.mi_complete=1

				for i in vecinos:

					existe=False
					if i != '' and i != str(paquete.nodo):
						for temp in self.nodos_grafo:
							if int(i) in temp:
								existe=True
								paquete_azul=self.packs.create_pack_16(0, sn_aux, 16,  paquete.nodo, temp[0] , int(IPv4Address(temp[1])), temp[2])
								paquete_send=[paquete_azul, (paquete.ip_azul, paquete.puerto_azul), sn_aux]
								self.paquetes_azules.append(paquete_send)
								self.llego_azul= self.llego_azul+1


						if not existe:

							paquete_azul=self.packs.create_pack_15( 0, sn_aux,15, paquete.nodo, int(i))
							paquete_send=[paquete_azul, (paquete.ip_azul, paquete.puerto_azul), sn_aux]
							self.paquetes_azules.append(paquete_send)
							self.llego_azul= self.llego_azul+1

						sn_aux+=1

				self.mutex_azul.release()




			else:
				aux=[paquete.nodo, paquete.ip_azul, paquete.puerto_azul]
				self.nodos_grafo.append(aux)

				print(self.nodos_grafo)

				self.paquetes_naranjas.append(paquete_enviar)




			#elimino el nodo muerto de mi lista de nodo activos
			#elif paquete.subtipo=='D':

				#paquete_enviar= self.packs.create_pack_token('T' , '1' ,  paquete.ip_naranja , paquete.ip_azul , paquete.nodo  , 'D' , paquete.puerto_azul)

				#for temp in self.nodos_grafo:
					#if paquete.nodo in temp:
						#self.nodos_grafo.remove(temp)

		#procesamientos paquete complete
		elif paquete.tipo==2:

			if self.token:
				print('llego complete')
				paquete_enviar= self.packs.create_pack_vacio(3)
				self.paquetes_naranjas.append(paquete_enviar)
				self.token=0
				self.mi_complete=0


			else:
				self.completos = self.completos + 1
				self.paquetes_naranjas.append(paquete_enviar)

				#if completos == cant_nodos
				#	send paquete

			if self.completos==self.total_naranjas+1:
				sn_aux=self.sn_azul

				self.mutex_azul.acquire()
				for i in self.solicitudes_listas:
					listo=self.packs.create_pack_17(0, sn_aux ,17)
					paquete_send=[listo, (i[0], i[1]), sn_aux]
					self.paquetes_azules.append(paquete_send)
					self.llego_azul= self.llego_azul+1
					sn_aux+=1
				self.mutex_azul.release()


			


		elif paquete.tipo==0:



			if int(IPv4Address(paquete.ip_naranja))!=  int(IPv4Address(self.mi_ip)):

				#reviso ip a ver si gana el que llego y lo modifico en caso de
				if int(IPv4Address(paquete.ip_naranja)) > int(IPv4Address(self.mi_ip)):
					self.inicial=self.inicial+1


				self.paquetes_naranjas.append(paquete_enviar)




			#ya me llego mi token inicial...








	#thread que solo envia
	def enviar_naranja_naranja(self):

		while True:
			self.mutex_naranja.acquire()
			if len(self.paquetes_naranjas):
				paquete=self.paquetes_naranjas.pop()
				#paquete auxiliar por si se pierde el que envie
				paquete_respaldo=paquete
				#print(paquete)
				#if paquete[0]!=3:
				print('voy a enviar ' + str(paquete))
				self.UDPServerSocket.sendto(paquete, self.vecino)

			self.mutex_naranja.release()
			if self.mando==1:	
				self.termino=1
				for i in range(60):
   					time.sleep(1)
   					if self.termino==0:
   						break

				if self.termino==1:
					print('voy a reenviar ' + str(paquete_respaldo))
					self.UDPServerSocket.sendto(paquete_respaldo, self.vecino)
					
			if self.soy_generador or self.token:
				self.mando=1


			#cuando esto se cumpla significa que envia un paquete, el timer se vencio y no me llego entonces reeenvio y reinicio timer
			# if self.reenviar_naranja==1 and self.llego_naranja==0:
			# 	print('voy a reenviar ' + str(paquete_respaldo))
			# 	self.UDPServerSocket.sendto(paquete_respaldo, self.vecino)
			# 	self.reenviar_naranja=0









	#thread que recibe paquetes
	def recibir_naranja_naranja(self):

		while True:

			bytesAddressPair = self.UDPServerSocket.recvfrom(self.bufferSize)

			paquete = bytesAddressPair[0]
		


			self.mutex_naranja.acquire()



			#verficio si es token inicial
			if paquete[0]==0:
				#paso de bytes a paquetes para procesar
				print('me llego ' + str(paquete))

				paquete_inicial =self.packs.unpack_pack_inicial(paquete)
				#print y proceso el paquete
				#print('me llego ' + str(paquete))
				self.procesar_paquete_naranja(paquete_inicial,paquete)

			#verifico si es paquete token
			elif paquete[0]==1:
				#paso de bytes a paquetes para procesar
				paquete_asignacion=self.packs.unpack_pack_asignacion(paquete)
				#llego mi paquete cierro el timer
				if self.token or self.soy_generador:
					self.mando=0
					self.termino=0
					
					

				#print y proceso el paquete
				self.packs.imprimir_token(paquete_asignacion)

				self.procesar_paquete_naranja(paquete_asignacion,paquete)

			elif paquete[0]==2:
				#paso de bytes a paquetes para procesar
				paquete_complete=self.packs.unpack_pack_complete(paquete)
				#llego mi paquete cierro el timer
				if self.token or self.soy_generador:
					self.mando=0
					self.termino=0
					

				#print y proceso el paquete
				print('me llego ' + str(paquete))

				self.procesar_paquete_naranja(paquete_complete,paquete)

			elif paquete[0]==3:
				#paso de bytes a paquetes para procesar
				paquete_vacio=self.packs.unpack_pack_vacio(paquete)
				#llego mi paquete cierro el timer
				if self.token or self.soy_generador:
					self.mando=0
					self.termino=0
					

				#print y proceso el paquete
				print('me llego ' + str(paquete))

				self.procesar_paquete_naranja(paquete_vacio,paquete)


			self.mutex_naranja.release()

# AZUL-NARANJA EN PROCESO
	def enviar_naranja_azul(self):

		while True:

			self.mutex_azul.acquire()

			if len(self.paquetes_azules):
				paquete=self.paquetes_azules.pop()

				
				if paquete[2]==-1:
					print('voy a enviar azul ' + str(paquete[0]))
					self.UDPServerazul.sendto(paquete[0], paquete[1])

				elif paquete[2]!=self.sn_azul:
					self.paquetes_azules.insert(0, paquete)

				else:

					paquete_respaldo=paquete
					print('voy a enviar azul ' + str(paquete[0]))
					self.UDPServerazul.sendto(paquete[0], paquete[1])


				self.mutex_azul.release()
				while paquete[2]==self.sn_azul:
					if self.reenviar_azul==1:
						self.UDPServerazul.sendto(paquete_respaldo[0], paquete_respaldo[1])
						self.reenviar_azul=0

			else:
				self.mutex_azul.release()




	def recibir_azul_naranja(self):

		while True:

			#paquete=secure_udp

			bytesAddressPair = self.UDPServerazul.recvfrom(self.bufferSize)

			paquete = bytesAddressPair[0]
			addr=bytesAddressPair[1]
			print('me llego azul ' + str(paquete))




			self.mutex_azul.acquire()
			print('pack id '+ str(int(paquete[0])))
			if paquete[0]==1:
				print('ack llego')
				sn=int.from_bytes(paquete[1:3], "big")
				print('sn que llego  ' + str(sn))
				if sn==self.sn_azul:
					self.sn_azul= self.sn_azul+1

					self.llego_azul= self.llego_azul-1
					print('mi sn aumento'+ str(self.sn_azul)+ '  '+ str(self.llego_azul))


			if paquete[0]==0:
				paquete_azul=self.packs.unpack_pack_azul(paquete)

				if paquete_azul.tipo==14:
					#print y proceso el paquete


					aux=[addr[0], addr[1]]
					if aux not in self.solicitudes_listas:
						self.azules+=1
						self.solicitudes.append(aux)
						self.solicitudes_listas.append(aux)

					if self.azules==self.total_azules:
						self.completo=1

					


					print(self.solicitudes)
					print(str(paquete_azul.sn))
					print(paquete_azul.sn)


					ack=pack('B',1)
					ack+=pack('H',paquete_azul.sn)
					paquete_send=[ack, addr, -1]

					self.paquetes_azules.append(paquete_send)

			self.mutex_azul.release()






	#Manejo de input
	def input_consola(self):
		while True:
			nombre=input()
			if nombre=='exit':
				quit()


	# #thread del timer
	# def timer_naranja(self):
	# 	while True:
	# 		if self.llego_naranja==0:
	# 			time.sleep(50)
	# 			self.reenviar_naranja=1



	def timer_azul(self):
		while True:
			if self.llego_azul!=0:
				time.sleep(60)
				self.reenviar_azul=1


	def verifica_inicial(self):
		while True:

			if self.inicial==self.total_naranjas:
				
				print('soy generador')
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
						self.llego_naranja=0
						paquete_enviar= self.packs.create_pack_asignacion(1 , int(nodo), int(IPv4Address(aux[0])), aux[1])
						self.token=1


						self.paquetes_naranjas.append(paquete_enviar)
						break
				else:

					paquete_enviar= self.packs.create_pack_vacio(3)
					self.token=0
					self.mande=0
					self.paquetes_naranjas.append(paquete_enviar)
					self.soy_generador=1

					break







def main():
	n_naranja = Naranja()

	if n_naranja.inicio():
		t5=Thread(target=n_naranja.recibir_azul_naranja)
		t6=Thread(target=n_naranja.enviar_naranja_azul)
		t7=Thread(target=n_naranja.timer_azul)
		#t3=Thread(target=n_naranja.timer_naranja)
		t4=Thread(target=n_naranja.verifica_inicial)
		t1=Thread(target=n_naranja.recibir_naranja_naranja)
		t2=Thread(target=n_naranja.enviar_naranja_naranja)
		t1.start()
		t2.start()
		#t3.start()
		t4.start()
		t5.start()
		t6.start()
		t7.start()
		#t3.join()
		t1.join()
		t2.join()
		t4:join()
		t5.join()
		t6.join()
		t7.join()

	#n_naranja.leer_grafo()
	#print(n_naranja.buscar_nodo())

		#t3=Thread(target=n_naranja.input_consola).start()


if __name__ == '__main__':
	main()
