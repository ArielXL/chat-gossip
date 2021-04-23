import sys
import time
import socket
import threading

class Gossip:

    infected_nodes = set()

    def __init__(self, host:str, port:int, connected_nodes:set):
        '''
        Inicializa las variables a utilizar e inicia los hilos. 
        Espera el host, el puerto y los puertos conectados a el.
        '''
        
        self.hostname = host
        self.port = port
        self.connected_nodes = connected_nodes
        self.susceptible_nodes = connected_nodes

        # usamos SOCK_DGRAM para poder enviar datos sin una conexion (UDP)
        self.node = socket.socket(type=socket.SOCK_DGRAM)

        # asigna la direccion y puerto del servidor
        self.node.bind((self.hostname, self.port))

        print(f'Empieza un nodo en el puerto {self.port}')
        print(f'Nodos susceptibles => {self.susceptible_nodes if len(self.susceptible_nodes) != 0 else {}}\n')

        # inicia los hilos de escribir y enviar los mensajes
        self.start_threads()

    def input_message(self):
        '''
        Escribe los mensajes para ser enviados.
        '''

        while True:
            # actualizamos la lista de nodos susceptibles
            self.susceptible_nodes = self.connected_nodes.copy()

            print('Escriba un mensaje:')
            message_to_send = input()
            if message_to_send != 'exit':
                self.transmit_message(message_to_send.encode('ascii'))
            else:
                self.node.close()
                sys.exit()

    def receive_message(self):
        '''
        Recibimos los mensajes.
        '''

        while True:
            # actualizamos la lista de nodos susceptibles
            self.susceptible_nodes = self.connected_nodes.copy()

            # usamos 'recvfrom' para recibir los mensajes
            # estamos usando un protocolo sin conexion (UDP)
            message_to_forward, address = self.node.recvfrom(1024)

            self.susceptible_nodes.discard(address[1])
            Gossip.infected_nodes.add(address[1])

            time.sleep(2)

            print(f'\nMensaje: "{message_to_forward.decode("ascii")}"')
            print(f'Recibido el {time.ctime(time.time())} por el puerto [{address[1]}]\n')

            self.transmit_message(message_to_forward)

    def transmit_message(self, message:str):
        '''
        Enviamos los mensajes a los restantes 
        nodos susceptibles.
        '''

        while len(self.susceptible_nodes) != 0:
            selected_port = self.susceptible_nodes.pop()

            print('-' * 50)
            print(f'Nodos susceptibles => {self.susceptible_nodes if len(self.susceptible_nodes) != 0 else {}}')
            print(f'Nodos infectados => {Gossip.infected_nodes if len(Gossip.infected_nodes) != 0 else {}}')
            print(f'Puerto seleccionado => [{selected_port}]')

            # usamos 'sendto' para transmitir los mensajes 
            # estamos usando un protocolo sin conexion (UDP)
            self.node.sendto(message, (self.hostname, selected_port))

            self.susceptible_nodes.discard(selected_port)
            Gossip.infected_nodes.add(selected_port)

            print(f'Mensaje: "{message.decode("ascii")}" enviado a [{selected_port}]')
            print(f'Nodos susceptibles => {self.susceptible_nodes if len(self.susceptible_nodes) != 0 else {}}')
            print(f'Nodos infectados => {Gossip.infected_nodes if len(Gossip.infected_nodes) != 0 else {}}')
            print('-' * 50)
            time.sleep(2)

    def start_threads(self):
        '''
        Permite que cada nodo pueda ingresar un 
        mensaje y aun pueda recibir otro mensaje.
        '''

        input_msg_thread = threading.Thread(target=self.input_message)
        receive_msg_thread = threading.Thread(target=self.receive_message)

        input_msg_thread.daemon = True
        input_msg_thread.start()

        receive_msg_thread.daemon = True
        receive_msg_thread.start()

        input_msg_thread.join()
        receive_msg_thread.join()
