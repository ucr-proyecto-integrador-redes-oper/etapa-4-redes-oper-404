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
        

	def create_pack_token(self,tipo, token, ip_naranja, ip_azul, subtipo, nodo, puerto_azul):
		return byte_pack= struct.pack('BBiiBhh', tipo.uncode(), token, ip_naranja.uncode(), ip_azul.uncode(),  nodo, subtipo.uncode(), puerto_azul)

 	def unpack_pack_token(self):
		paquete=paquete_token()
		struct.unpack('BBiiBhh', datos)
		paquete.tipo=datos[0].decode('utf-8')
		paquete.token=datos[1]
		paquete.ip_naranja=datos[2].decode('utf-8')
		paquete.ip_azul=datos[3].decode('utf-8')
		paquete.nodo=datos[4]
		paquete.subtipo=datos[5]
		paquete.puerto_azul=datos[6]
		return paquete


	def create_pack_inicial(self, tipo, ip_naranja, elegido):
		return byte_pack= struct.pack('Bii', tipo.uncode(), ip_naranja.uncode(), elegido.uncode())

 	def unpack_pack_inicial(self, datos):
		paquete=paquete_inicial()
		struct.unpack('Bii', datos)
		paquete.tipo=datos[0].decode('utf-8')
		paquete.ip_naranja=datos[1].decode('utf-8')
		paquete.elegido=datos[2].decode('utf-8')
		return paquete

	def procesar_token(self,paquete):
		
		paquete_enviar= self.create_pack_token('T' ,'0' ,paquete.ip_naranja ,paquete.ip_azul ,paquete.nodo  , 'S' , paquete.puerto_azul)
		
		if paquete.ip_naranja==self.mi_ip:
			
			paquete_enviar= self.create_pack_token('T' , '0' , paquete.ip_naranja,  paquete.ip_azul , paquete.nodo ,'S' , paquete.puerto_azul)
			
			self.paquetes.append(paquete_enviar)
		
		else: 
			
			if paquete.token== '0':
							
				if len(self.solicitudes):
					aux=self.solicitudes.pop()
					paquete_enviar= self.create_pack_token('T' , '1' ,  self.mi_ip, aux[0], aux[1] ,  'S' , aux[2])
							
						
				elif len(self.muertos):
					aux=self.muertos.pop()
					paquete_enviar= self.create_pack_token('T' , '1' ,  + self.mi_ip , paquete.ip_azul , aux , 'D' , paquete.puerto_azul)
					
						
				elif self.completo:
					paquete_enviar= self.create_pack_token('T' , '1', self.mi_ip , paquete.ip_azul , paquete.nodo, 'C' , paquete.puerto_azul)
			
				self.paquetes.append(paquete_enviar)
					
			else:

				if paquete.subtipo=='S':
					paquete_enviar= self.create_pack_token('T' , '1' ,  , paquete.ip_naranja, paquete.ip_azul , paquete.nodo  , 'C' , paquete.puerto_azul)
					existe=False
						
					aux=[paquete.nodo, paquete.ip_azul, paquete.puerto_azul]
						
					for temp in self.nodos_grafo:
						if paquete.nodo in temp:
							existe=True

					if not existe:
						self.nodos_grafo.append(aux)		
				
				elif paquete.subtipo=='D':
					paquete_enviar= self.create_pack_token('T' , '1' ,  paquete.ip_naranja , paquete.ip_azul , paquete.nodo  , 'D' , paquete.puerto_azul)

					for temp in self.nodos_grafo:
						if paquete.nodo in temp:
							self.nodos_grafo.remove(temp)					
					

				elif paquete.subtipo=='C':
					paquete_enviar= self.create_pack_token('T' , '1' ,paquete.ip_naranja, paquete.ip_azul , paquete.nodo  , 'C' , paquete.puerto_azul)
					self.completos = self.completos + 1
						#if completos == cant_nodos
						#	send paquete 
					
				self.paquetes.append(paquete_enviar)


	

	def procesar_inicial(self,paquete):
		paquete_enviar=''
		if paquete.elegido != self.mi_ip:
			if paquete.ip_naranja < self.mi_ip:			 
				paquete_enviar= self.create_pack_inicial(paquete.tipo, paquete.ip_naranja, self.mi_ip)

			
					
		else:
			aux=[0,'',0]
			paquete_enviar= self.create_pack_token('T' + '0' +  + aux[0]+ aux[1] + aux[2] + 'S' + self.mi_ip)
			if len(self.solicitudes):
				aux=self.solicitudes.pop()
				paquete_enviar= self.create_pack_token('T' + '1' +  + aux[0]+ aux[1] + aux[2] + 'S' + self.mi_ip)

		
		self.paquetes.append(paquete_enviar)

	

	
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
			
			if paquete[0]=='I':
				paquete_inicial=self.unpack_pack_inicial(paquete)
				procesar_inicial(paquete_inicial)


			elif paquete[0]=='T':
				paquete_token=self.unpack_pack_token(paquete)
				procesar_token(paquete_inicial)

				



			
def main():
	n_naranja = Naranja()
	threading.Thread(target=n_naranja.recibir_naranja_naranja).start()
	threading.Thread(target=n_naranja.enviar_naranja_naranja).start()


if __name__ == '__main__':
	main()


		
	
