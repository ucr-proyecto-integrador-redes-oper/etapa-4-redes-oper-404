import threading


# class paquete_token:
#     def __init__(self):
#         self.token = 0
#         self.tipo = 'T'
#         self.ip_naranja=0
#         self.ip_azul=0
#         self.puerto_azul=0
#         self.subtipo=''
#         self.nodo=0

# class paquete_inicial:
#     def __init__(self):
#         self.tipo = 'I'
#         self.ip_naranja=0
#         self.elegido=0


class Naranja():
	
	def __init__(self): 
		self.completos=0
		self.solicitudes = [['600','255.234.234.255', '6666']]
		self.muertos=[]
		self.completo=0
		self.nodos_grafo = []
		self.paquetes=[]
		self.mi_ip='255.255.255.255'

	def inicio(self):
		paquete=paquete_inicial()
		paquete.ip_naranja=0
		#lock
		self.paquetes_tok.append(paquete)
		#unlock
        

	
	def enviar_naranja_naranja(self):

		for i in range(10):
			#lock

			if len(self.paquetes):
				paquete=self.paquetes.pop()
				print(paquete)

			#unlock
			#send secure udp
			


	def recibir_naranja_naranja(self):
		


		for i in range(10):

			#paquete = recibe secureUDP
			#lock	
			#paquete='T0600301.301.301.3017777S128.128.128.128'
			paquete='I128.128.128.128130.130.130.130'
			
			
			if paquete[0]=='I':
				valido=False
				ip_naranja=''
				elegido=''
				for i in range(15):
					if paquete[i+1]!='0' or valido:
						ip_naranja= ip_naranja + paquete[i+1]
						valido=True

				valido=False
				for i in range(15):
					if paquete[i+16]!='0' or valido:
						elegido= elegido + paquete[i+16]
						valido=True
				
				
				if elegido != self.mi_ip:
					if ip_naranja < self.mi_ip:			 
						paquete= 'I'+  ip_naranja +   self.mi_ip

					self.paquetes.append(paquete)
					
				else:
					paquete= 'T' + '0' + aux[0] + aux[1] + aux[2] + 'S' + self.mip
					if len(self.solicitudes):
						aux=self.solicitudes.pop()
						paquete= 'T' + '1' + aux[0] + aux[1] + aux[2] + 'S' + self.mip

					self.paquetes.append(paquete)



			elif paquete[0]=='T':

				token=paquete[1]
				ip_naranja=''
				nodo=''
				ip_azul=''
				puerto_azul=''
				
				valido=False
				for i in range(3):
					if paquete[i+2]!='0' or valido:
						nodo= nodo+paquete[i+2]
						valido=True

				valido=False	
				for i in range(15):
					if paquete[i+5]!='0' or valido:
						ip_azul= ip_azul+paquete[i+5]
						valido=True

				valido=False
				for i in range(4):
					if paquete[i+20]!='0' or valido:
						ip_azul= ip_azul+paquete[i+20]
						valido=True

				subtipo=paquete[24]
				
				valido=False
				for i in range(15):
					if paquete[i+25]!='0' or valido:
						ip_naranja= ip_naranja+paquete[i+25]
						valido=True



				if ip_naranja==self.mi_ip:
					paquete[1]='0'
					self.paquetes.append(paquete)
				else: 
					if token== '0':					
						if len(self.solicitudes):
							subtipo='S'
							aux=self.solicitudes.pop()
							nodo=aux[0]
							token='1'
							ip_azul=aux[1]
							puerto_azul=aux[2]
							ip_naranja=self.mi_ip			
						
						elif len(self.muertos):
							token='1'
							subtipo='D'
							aux=self.muertos.pop()
							nodo=aux
							ip_naranja=self.mi_ip
						
						elif self.completo:
							token='1'
							subtipo='C'
							ip_naranja=self.mi_ip


						paquete='T' + token + nodo + ip_azul + puerto_azul + subtipo + ip_naranja
						self.paquetes.append(paquete)
					
					else:

						if subtipo=='S':
							existe=False
						
							aux=[nodo, ip_azul, puerto_azul]
						
							for temp in self.nodos_grafo:
								if nodo in temp:
									existe=True

							if not existe:
								self.nodos_grafo.append(aux)
								
							
							self.paquetes.append(paquete)


						elif subtipo=='D':

							for temp in self.nodos_grafo:
								if nodo in temp:
									self.nodos_grafo.remove(temp)

							self.paquetes.append(paquete)			 


						elif subtipo=='C':
							self.completos = self.completos + 1
							#if completos == cant_nodos
							#	send paquete 

			#unlock
def main():
	n_naranja = Naranja()
	threading.Thread(target=n_naranja.recibir_naranja_naranja).start()
	threading.Thread(target=n_naranja.enviar_naranja_naranja).start()


if __name__ == '__main__':
	main()


		
	