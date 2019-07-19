from usl import Usl
from validador import *
from Util import *

from threading import *
from time import *


class Azules():


    def __init__(self, ipServer, portServer):

        # Variables para paquetes de verdes
        self.uslito = Usl()
        self.esta_en_arbol = False
        self.id_nodo = 0
        self.vecinos = []
        self.vecinos_arbol = []
        self.ip_server = ipServer
        self.puerto_server = portServer

        self.estoy_en_arbol = False
        

        t_recibir = Thread(target=self.recibir)

        t_recibir.start()

        self.joinGraph()



######################################### NARANJA - AZUL ##############################################

    # Metodo que envia request a naranja para unirse al grafo
    def joinGraph(self):

        paquete_joinGraph = (14).to_bytes(1, byteorder='big')

        print('Enviando Join request a Naranja....')

        self.uslito.enviar(paquete_joinGraph, self.ip_server, self.puerto_server)

        print( 'Se envio correctamente el request...')

#######################################################################################################


######################################### AZUL - AZUL #################################################

    # Metodo que envia paquete Hello al vecino
    def hello(self, vecinoIp, vecinoPort):

        tipo = (1).to_bytes(1, byteorder='big')
        nodoId = (self.id_nodo).to_bytes(2, byteorder='big')
        paquete_hello = tipo + nodoId
        print('Enviando HELLO a vecino IP: {} PUERTO: {}'.format(vecinoIp, vecinoPort))

        self.uslito.enviar(paquete_hello, vecinoIp, vecinoPort)
        
        print('HELLO enviado a vecino IP: {} PUERTO: {}'.format(vecinoIp, vecinoPort))


#######################################################################################################


######################################### Arbol Generador #############################################

    def join_tree(self):  
        if self.id_nodo == 1:  
            self.estoy_en_arbol = True 
            return 0
        
        while self.estoy_en_arbol == False:
            msgId = (11).to_bytes(1, byteorder="big")
            nodeId = (self.id_nodo).to_bytes(2, byteorder="big")
            msgFinal = (msgId + nodeId)
            for vecino in self.vecinos:
                self.uslito.enviar(msgFinal, str(vecino[1]), int(vecino[2]))
                print('enviando a vecino: ' + str(vecino[0]))
                
            sleep(2)

    def Ido(self, id):  
        if self.estoy_en_arbol == True:
            msg = (12).to_bytes(1, byteorder="big") + (self.id_nodo).to_bytes(2, byteorder="big")
            for i in self.vecinos:
                if i[0] == id:
                    self.uslito.enviar(msg, str(i[1]), int(i[2]))

    def daddy(self, id): 
        msg = (13).to_bytes(1, byteorder="big") + (self.id_nodo).to_bytes(2, byteorder="big")
        for i in self.vecinos:
            if i[0] == id:
                self.uslito.enviar(msg, str(i[1]), int(i[2])) 
            self.estoy_en_arbol = True
       
        


#######################################################################################################


    # Hilo que se encarga de recibir paquetes y procesarlos
    def recibir(self):

        while (True):
            paquete = self.uslito.getPaquete()

            # Si es un paquete HELLO
            if int(paquete[0][0]) == 1:
                vecino = int.from_bytes(paquete[0][1:3], byteorder='big')
                ip_vecino =  ip_tuple_to_str(paquete[1][0])
                port_vecino = paquete[1][1]
                print('HELLO desde nodo: ' + str(vecino) )

                # agrego la ip y puerto del vecino 
                for i in self.vecinos:
                    if i[0] == vecino:
                        i[1] = ip_vecino
                        i[2] = port_vecino
                
            # No tiene ip y puerto
            elif int(paquete[0][0]) == 15:

                self.id_nodo = int.from_bytes(paquete[0][1:3], byteorder='big')
                vecino_id = int.from_bytes(paquete[0][3:5], byteorder='big')
                print('Ha llegado paquete con vecino ID {} no instanciado'.format(vecino_id))
                print('---------- MI ID ES {} ----------'.format(self.id_nodo))
                repetido = False
                for i in self.vecinos:
                    if i[0] == vecino_id:
                        repetido = True

                if repetido == False:
                    vecino = [vecino_id, 0, 0]
                    self.vecinos.append(vecino)

            # Paquete con el ip y puerto del vecino
            elif int(paquete[0][0]) == 16:

                self.id_nodo = int.from_bytes(paquete[0][1:3], byteorder='big')
                vecino_id = int.from_bytes(paquete[0][3:5], byteorder='big')
                vecino_ip = ip_to_int_tuple(paquete[0][5:9])
                vecino_ip = ip_tuple_to_str(vecino_ip)
                vecino_puerto = int.from_bytes(paquete[0][9:11], byteorder='big')
                print('Ha llegado paquete con vecino ID {} intanciado'.format(vecino_id))
                print('---------- MI ID ES {} ----------'.format(self.id_nodo))
                repetido = False
                for i in self.vecinos:
                    if i[0] == vecino_id:
                        repetido = True

                if repetido == False:
                    vecino = [vecino_id, vecino_ip, vecino_puerto]
                    self.vecinos.append(vecino)

                self.hello(vecino_ip, vecino_puerto)

            # Llega paquete de tipo completeGraph y debe empezar a hacer el joinTree para armar la topología
            elif int(paquete[0][0]) == 17:
                print('El grafo está completo\n')

                # Debe empezar a unirse al arbol
                print("Comenzando a crear el árbol......")
                arbol = Thread(target= self.join_tree)
                arbol.start()
		
            elif int(paquete[0][0]) == 11: # Paquete JoinTree

                print('Recibí paquete JOINTREE')
                vecino = int.from_bytes(paquete[0][1:3], byteorder='big')
                self.Ido(vecino)


            elif int(paquete[0][0]) == 12: # Paquete I DO

                print('Recibí paquete I DO')
                # Si aún no estoy en el árbol, me uno con padre = id del nodo del paquete que me llegó
                if self.estoy_en_arbol == False:
                    papi = int.from_bytes(paquete[0][1:3], byteorder='big')
                    self.daddy(papi)

                    print("Soy -->  " + self.id_nodo + " hijo de -->  " + papi)
                    self.vecinos_arbol.append(papi)
                else:
                    print('ya estoy en el arbol...')
                
            elif int(paquete[0][0]) == 13: # Paquete DADDY 

                print('Recibí paquete DADDY')
                hijo = int.from_bytes(paquete[0][1:3], byteorder='big')
                self.vecinos_arbol.append(hijo)



def main():

    valida = Validador()

    print('Introduzca IP de Naranja:')
    ip = input()
    if not valida.ip_valida(ip):
	    print('---------- IP INVALIDO ----------')

    print('Introduzca Puerto de Naranja:')
    puerto = input()
    if not valida.puerto_valido(puerto):
	    print('---------- Puerto INVALIDO ----------')


    nodo_azul = Azules(str(ip), int(puerto))



if __name__ == "__main__":
    main()
