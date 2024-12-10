import socket
import threading

class Network:
    def __init__(self, node):
        self.node = node
        self.peers = []
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = False

    def start_server(self, host='0.0.0.0', port=8333):
        self.server.bind((host, port))
        self.server.listen()
        self.running = True
        print(f"Node listening on {host}:{port}")
        self.server_thread = threading.Thread(target=self.listen_for_connections, daemon=True)
        self.server_thread.start()

    def stop_server(self):
        """Gracefully stop the server and clean up resources"""
        self.running = False
        # Create a temporary connection to unblock accept()
        try:
            tmp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tmp_socket.connect(('localhost', self.server.getsockname()[1]))
            tmp_socket.close()
        except:
            pass
        self.server.close()
        for peer in self.peers:
            peer.close()
        self.peers.clear()

    def listen_for_connections(self):
        while self.running:
            client, address = self.server.accept()
            print(f"Connection from {address}")
            threading.Thread(target=self.handle_client, args=(client,), daemon=True).start()

    def handle_client(self, client_socket):
        while True:
            try:
                data = client_socket.recv(4096)
                if not data:
                    break
                # Handle incoming data (e.g., new blocks or transactions)
                self.node.process_data(data)
            except:
                break
        client_socket.close()

    def connect_to_peer(self, host, port):
        peer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        peer.connect((host, port))
        self.peers.append(peer)
        threading.Thread(target=self.handle_client, args=(peer,), daemon=True).start()

    def broadcast(self, data):
        for peer in self.peers:
            try:
                peer.sendall(data)
            except:
                self.peers.remove(peer)
