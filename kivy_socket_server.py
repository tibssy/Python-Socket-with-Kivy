import socket
import threading
import pickle
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout


class MyLayout(BoxLayout):
    pass


class ServerApp(App):
    COLOR_DARK = (0.2, 0.2, 0.2, 1)
    COLOR_LIGHT = (0.6, 0.6, 0.6, 1)
    SERVER = socket.gethostbyname(socket.gethostname())
    PORT = 5050
    ADDR = (SERVER, PORT)
    HEADER = 64
    server = None
    addr = None

    def build(self):
        return MyLayout()

    def on_start(self):
        self.create_socket()
        thread = threading.Thread(target=self.client_listener, daemon=True)
        thread.start()

    def create_socket(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDR)
        self.update_info(self.ADDR)

    def client_listener(self):
        self.server.listen()
        while True:
            conn, self.addr = self.server.accept()
            self.receive_data(conn)

    def receive_data(self, conn):
        msg_length = pickle.loads(conn.recv(self.HEADER))
        if msg_length:
            msg = pickle.loads(conn.recv(int(msg_length)))
            self.show_message(msg)
        conn.close()

    def update_info(self, addr):
        self.root.ids.info.addr = addr

    def show_message(self, msg):
        self.root.ids.messages.data.append({'name': self.addr[0], 'text': msg})
        self.root.ids.messages.scroll_y = 0


if __name__ == "__main__":
    ServerApp().run()
