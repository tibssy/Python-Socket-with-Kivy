import socket
import pickle
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout


class MyLayout(BoxLayout):
    pass


class ClientApp(App):
    COLOR_DARK = (0.2, 0.2, 0.2, 1)
    COLOR_MID = (0.4, 0.4, 0.4, 1)
    COLOR_LIGHT = (0.6, 0.6, 0.6, 1)
    SERVER = '127.0.1.1'  # IP Address of the Server
    PORT = 5050
    ADDR = (SERVER, PORT)
    HEADER = 64
    client = None

    def build(self):
        return MyLayout()

    def connect_to_server(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(self.ADDR)

    def send_to_server(self, msg):
        message = pickle.dumps(msg)
        msg_length = len(message)
        send_length = pickle.dumps(msg_length)
        send_length += b' ' * (self.HEADER - len(send_length))
        self.client.send(send_length)
        self.client.send(message)

    def submit(self, msg):
        try:
            self.connect_to_server()
        except OSError:
            self.root.ids.npt.text = ''
            self.root.ids.npt.hint_text = 'Destination Unreachable'
        else:
            self.root.ids.npt.text = ''
            self.root.ids.npt.hint_text = ''
            self.root.ids.history.data.append({'text': msg})
            self.root.ids.history.scroll_y = 0
            self.send_to_server(msg)


if __name__ == "__main__":
    ClientApp().run()
