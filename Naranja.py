import threading
from struct import *
import csv
from Paquetes import *

class Naranja():
	
	def __init__(self): 
		self.completos=0
		
		self.solicitudes = [['255.234.234.255', 6666], ['253.234.234.255', 6667], ['255.234.234.222',  7666]]
		
		self.muertos=[['255.234.234.255',600, 6666], ['253.234.234.255',60, 6667], ['255.234.234.222',607, 7666]]
		self.completo=0
		self.nodos_grafo = []
		self.paquetes=[]
		self.grafo=[]
		self.mi_ip='255.255.255.255'
		self.packs=Paquetes()
		

	def leer_grafo(self):
		with open('grafo_prueba.csv', newline='') as File:  
			reader = csv.reader(File)
			for row in reader:
				grafo.append(row)

	
	def buscar_nodo(self):
		for f in len(grafo):
			for i in len(grafo[0]):
				if grafo[f][c] not in nodos_grafo:
					return grafo[f][c]

		return -1



	def inicio(self):
		paquete=paquete_inicial()
		paquete.ip_naranja=0
		#lock
		self.paquetes_tok.append(paquete)
		#unlock




	def procesar_azul(self, paquete):
		
		if paquete.tipo=='R':
			aux=[paquete.ip_azul, paquete.puerto_azul]
			solicitudes.append(aux)

		elif paquete.tipo=='D':
			aux=[paquete.ip_azul, paquete.nodo, paquete.puerto_azul]
			muertos.append(aux)

				
		elif paquete.tipo=='C':
			self.completo=1

	


	def procesar_token(self,paquete):
		
		paquete_enviar= self.packs.create_pack_token('T' ,'0' ,paquete.ip_naranja ,paquete.ip_azul ,paquete.nodo  , 'S' , paquete.puerto_azul)
		
		
		if paquete.ip_naranja==self.mi_ip:
			
			paquete_enviar= self.packs.create_pack_token('T' , '0' , paquete.ip_naranja,  paquete.ip_azul , paquete.nodo ,'S' , paquete.puerto_azul)
			
			
			self.paquetes.append(paquete_enviar)
		
		else: 
			
			if paquete.token== '0':
				
							
				if len(self.solicitudes):
					aux=self.solicitudes.pop()
					nodo=self.buscar_nodo()
					if nodo!= -1:
						paquete_enviar= self.packs.create_pack_token('T' , '1' ,  self.mi_ip, aux[0], nodo  ,  'S' , aux[1])
						paquete_azul= self.packs.create_pack_asignacion()

							
						
				elif len(self.muertos):
					aux=self.muertos.pop()
					paquete_enviar= self.packs.create_pack_token('T' , '1' ,  + self.mi_ip , paquete.ip_azul , aux , 'D' , paquete.puerto_azul)
					
						
				elif self.completo:
					paquete_enviar= self.packs.create_pack_token('T' , '1', self.mi_ip , paquete.ip_azul , paquete.nodo, 'C' , paquete.puerto_azul)
			
				self.paquetes.append(paquete_enviar)
					
			else:

				if paquete.subtipo=='S':
					paquete_enviar= self.packs.create_pack_token('T' , '1'   , paquete.ip_naranja, paquete.ip_azul , paquete.nodo  , 'S' , paquete.puerto_azul)
					existe=False
						
					aux=[paquete.nodo, paquete.ip_azul, paquete.puerto_azul]
						
					for temp in self.nodos_grafo:
						if paquete.nodo in temp:
							existe=True

					if not existe:
						self.nodos_grafo.append(aux)

				
				elif paquete.subtipo=='D':
					paquete_enviar= self.packs.create_pack_token('T' , '1' ,  paquete.ip_naranja , paquete.ip_azul , paquete.nodo  , 'D' , paquete.puerto_azul)

					for temp in self.nodos_grafo:
						if paquete.nodo in temp:
							self.nodos_grafo.remove(temp)					
					

				elif paquete.subtipo=='C':
					paquete_enviar= self.packs.create_pack_token('T' , '1' ,paquete.ip_naranja, paquete.ip_azul , paquete.nodo  , 'C' , paquete.puerto_azul)
					self.completos = self.completos + 1
						#if completos == cant_nodos
						#	send paquete 
					
				self.paquetes.append(paquete_enviar)


	

	def procesar_inicial(self,paquete):
		paquete_enviar=''
		if paquete.elegido != self.mi_ip:
			if paquete.ip_naranja < self.mi_ip:			 
				paquete_enviar= self.packs.create_pack_inicial(paquete.tipo, paquete.ip_naranja, self.mi_ip)

			
					
		else:
			aux=[0,'',0]
			nodo=self.buscar_nodo()
			paquete_enviar= self.packs.create_pack_token('T' ,'0' ,self.mi_ip, aux[0] ,nodo , 'S' , aux[1])
			if len(self.solicitudes):
				aux=self.solicitudes.pop()
				if nodo!= -1:
					paquete_enviar= self.packs.create_pack_token('T' , '1',  self.mi_ip , aux[0], nodo , 'S' , aux[1])

		
		self.paquetes.append(paquete_enviar)

	

	
	def enviar_naranja_naranja(self):

		for i in range(10):
			#lock

			if len(self.paquetes):
				paquete=self.paquetes.pop()
				

			#unlock
			#send secure udp
			

	def recibir_naranja_naranja(self):
		
		for i in range(10):

			paquete = self.packs.create_pack_token('T' , '1', '123.124.125.154' , '255.255.256.255', 60, 'S', 7777)


			if str(chr(paquete[0]))=='I':

				paquete_inicial=self.packs.unpack_pack_inicial(paquete)
				self.procesar_inicial(paquete_inicial)


			elif str(chr(paquete[0]))=='T':
				
				paquete_token=self.packs.unpack_pack_token(paquete)
				self.procesar_token(paquete_token)



	def enviar_naranja_azul(self):

		for i in range(10):
			#lock

			if len(self.paquetes_azules):
				paquete=self.paquetes_azules.pop()
				

			#unlock
			#send secure udp
			

	def recibir_azul_naranja(self):
		
		for i in range(10):

			paquete = self.packs.create_pack_token('S')

			paquete_azul = self.packs.unpack_pack_azul(paquete)

			self.procesar_azul(paquete_azul)








				



			
def main():
	n_naranja = Naranja()
	threading.Thread(target=n_naranja.recibir_naranja_naranja).start()
	threading.Thread(target=n_naranja.enviar_naranja_naranja).start()


if __name__ == '__main__':
	main()


		
	
