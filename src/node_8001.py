from gossip import Gossip

def main():
    host = 'localhost'
    port = 8001
    connected_nodes = { 8000 , 8003 , 8004 }

    node = Gossip(host, port, connected_nodes)

if __name__ == '__main__':
    main()