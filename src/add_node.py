import argparse
from gossip import Gossip

def get_arguments():

    parser = argparse.ArgumentParser(description='Adiciona un nodo.')
    parser.add_argument('-o', '--host', type=str, dest='hostname', 
                            help='Direccion para establecer las conexiones.')
    parser.add_argument('-p', '--port', type=int, dest='port', 
                            help='Puerto para establecer las conexiones.')
    parser.add_argument('-n', '--node', action='append', dest='nodes', default=[], 
            help='Conjunto de los nodos conectados a traves de los puertos.')

    return parser.parse_args()

def main():

    args = get_arguments()

    host = args.hostname
    port = args.port
    connected_nodes = [ int(node) for node in args.nodes ]

    node = Gossip(host, port, set(connected_nodes))

if __name__ == '__main__':
    main()