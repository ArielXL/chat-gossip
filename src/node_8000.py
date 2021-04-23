from gossip import Gossip

def main():
    host = 'localhost'
    port = 8000
    connected_nodes = { 8001 , 8002 }

    node = Gossip(host, port, connected_nodes)

if __name__ == '__main__':
    main()