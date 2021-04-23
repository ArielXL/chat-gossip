from gossip import Gossip

def main():
    host = 'localhost'
    port = 8003
    connected_nodes = { 8001 }

    node = Gossip(host, port, connected_nodes)

if __name__ == '__main__':
    main()