import threading


class paquete_token:
    def __init__(self):
        self.token = 0
        self.tipo = 'T'
        self.ip_naranja=0
        self.ip_azul=0
        self.puerto_azul=0
        self.subtipo=''
        self.nodo=0

class paquete_inicial:
    def __init__(self):
        self.tipo = 'I'
        self.ip_naranja=0
        self.elegido=0


class Naranja():
	
	def __init__(self): 
		self.solicitudes = []
		self.muertos=[]
		self.paquetes_tok=[]
		self.completo=0
		self.nodos_grafo = []
		self.paquetes=[]
		self.mi_ip=0

	def inicio(self):
		paquete=paquete_inicial()
		paquete.ip_naranja=0
		#lock
		self.paquetes_tok.append(paquete)
		#unlock
        

	
	def enviar_naranja_naranja(self):

		for i in range(10):
			#lock
			hay_paquete=False
			if len(self.paquetes_tok):

				paquete=self.paquetes.pop()
				hay_paquete=True

			if len(self.paquetes) and not hay_paquete:
				paquete=self.paquetes.pop()

			#unlock
			#send secure udp


	def recibir_naranja_naranja(self):
		


		for i in range(10):

			#paquete = recibe secureUDP
			#lock	
			paquete=paquete_inicial()
			
			if paquete.tipo=='I':
				if paquete.elegido != self.mi_ip:
					if paquete.ip_naranja < self.mi_ip:
						paquete.elegido = self.mi_ip

					self.paquetes_tok.append(paquete)
					
				else:
					primer_token=paquete_token()
					if len(self.solicitudes):
						aux=self.solicitudes.pop()
						primer_token.nodo=aux[0]
						primer_token.ip_azul=aux[1]
						primer_token.puerto_azul=aux[2]
						primer_token.token=1
						primer_token.ip_naranja=self.mi_ip
						primer_token.subtipo='S'

					self.paquetes.append(primer_token)



			elif paquete.tipo=='T':

				if paquete.ip_naranja==self.mi_ip:
					paquete.token=0
					self.paquetes.append(paquete)
				else: 
					if not paquete.token:
						
						if len(self.solicitudes):
							aux=self.solicitudes.pop()
							paquete.nodo=aux[0]
							paquete.ip_azul=aux[1]
							paquete.puerto_azul=aux[2]			
						
						if len(self.muertos):
							aux=self.muertos.pop()
							paquete.nodo=aux
						if completo:
							paquete.subtipo='C'

						
						self.paquetes.append(paquete)
					
					else:

						if paquete.subtipo=='S':
							existe=False
						
							aux=[paquete.nodo, paquete.ip_azul, paquete.puerto_azul]
						
							for temp in self.nodos_grafo:
								if paquete.nodo in temp:
									existe=True

							if not existe:
								self.nodos_grafo.append(aux)
								
							
							self.paquetes.append(paquete)


						elif paquete.subtipo=='D':

							for temp in self.nodos_grafo:
								if paquete.nodo in temp:
									self.nodos_grafo.remove(temp)

							self.paquetes.append(paquete)			 


						elif paquete.subtipo=='C':
							pass

			#unlock
def main():
	n_naranja = Naranja()
	threading.Thread(target=n_naranja.recibir_naranja_naranja).start()
	threading.Thread(target=n_naranja.enviar_naranja_naranja).start()


if __name__ == '__main__':
	main()


		
	