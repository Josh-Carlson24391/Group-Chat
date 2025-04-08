import tkinter as tk
import threading
import socket
import queue

class App:
    def __init__(self, master):
        self.master = master
        master.title("Group Chat Client")

        #Label Text displaying the most recent message
        self.label_text = tk.StringVar()
        self.label = tk.Label(master, textvariable = self.label_text)
        self.label.pack()

        #Initializes the input text box
        self.input_text = tk.Text(master=master, height=2, width=40)

        #Initilizes the send button to clear the input box and send it to the server
        self.send_button = tk.Button(master=master, text="SEND!", command=self.self.format_and_send())

        #Initializes Queue
        self.data_queue = queue.Queue()
        self.running = True

        #Starts new thread to read from server socket in background
        self.socket_thread = threading.Thread(target=self.read_socket)
        self.socket_thread.daemon = True  # Allow program to exit even if thread is running
        self.socket_thread.start()

        


        #Updates all the gui
        self.update_gui()

    def read_socket(self):
        host = '127.0.0.1'  # Or "localhost"
        port = 65432         # Replace with your port

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                #Saves a reference to the server socket in order to also send data to the server
                self.server_socket = s
                s.connect((host, port))
                while self.running:
                    data = s.recv(1024)
                    #Debugging print
                    print(data.decode())
                    if not data:
                        break
                    self.data_queue.put(data.decode())
        except Exception as e:
             self.data_queue.put(f"Error: {e}")

    def update_gui(self):
        try:
            data = self.data_queue.get_nowait()
            self.label_text.set(data)
        except queue.Empty:
            pass  # No data yet, ignore
        if self.running:
            self.master.after(100, self.update_gui) # Check every 100 ms

    def close(self):
        self.running = False
        self.master.destroy()

    def send_data(self, message):
        #Tries to send data to server socket, if there is no server socket it will print an error message
        try:
            if hasattr(self, 'server_socket'):
                self.server_socket.sendall(message)
        except Exception:
            print("Connection to server has been lost while sending data")
    def format_and_send(self, data):

        #Extracts the whole text from input box
        input_text = self.text_input.get("1.0", tk.END).strip()

        #Creates a list of the first two lines
        lines = input_text.splitlines()[:2]

        #Rejoins the two lines together as 
        message = "\n".join(lines) 

        #Clears the input box after extracting the first two lines of text
        self.text_input.delete("1.0", tk.END)

        #Calls send data function to send the message to the server
        self.send_data(message)

root = tk.Tk()
app = App(root)
root.protocol("WM_DELETE_WINDOW", app.close) # Handle window close event
root.mainloop()