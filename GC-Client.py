import tkinter as tk
from tkinter import simpledialog
import threading
import socket
import queue

class App:
    def __init__(self, master):
        self.master = master
        


        #Pop up to prompt user for thier name:
        self.username = tk.simpledialog.askstring("Enter Name", "Please enter your name:")
        
        if not self.username:  # If no name is entered, set default name to guest
            self.username = "Guest"

        master.title("Group Chat Client: " + self.username)
        master.config(bg="black")
        

        #Creating a labeled frame to hold the message board and a scroll bar
        self.output_frame = tk.LabelFrame(master, text="Message Board", padx=5, pady=5, bg="black", fg="white")
        self.output_frame.pack(fill="x")

        self.input_frame = tk.LabelFrame(master, text="Enter Your Message Below:", bg="black", fg="white")
        self.input_frame.pack()
        #Initializing the message board
        self.label_text = tk.StringVar()
        #Setting editinng to disabled so that it is only ever edited inside of the update messageboard function
        #Message board is attatched to output frame widget so that it can have a label and be grouped with the scroll bar
        self.message_board = tk.Text(self.output_frame, height=20, width=20, wrap=tk.WORD, state=tk.DISABLED, background="green", fg="white")
        self.message_board.pack(side="left", fill="x", expand=True)

        #Initializing scroll bar
        self.scrollbar = tk.Scrollbar(self.output_frame, orient='vertical', background="purple")
        #Align it on the right and make it fill the y axis of the frame
        self.scrollbar.pack(side="right",fill="y")
        
        #Syncing scroll bar with text box 

        #When the scroll bar is moved, it updates the yview of the message board causing it to scroll with the scroll bar
        self.scrollbar.config(command=self.message_board.yview)
        #When the text box is scrolled with the mouse, sync the scroll bar with the textbox
        self.message_board.config(yscrollcommand=self.scrollbar.set)

        #Initializes Queue
        self.data_queue = queue.Queue()
        self.running = True

        #Starts new thread to read from server socket in background
        self.socket_thread = threading.Thread(target=self.read_socket)
        self.socket_thread.daemon = True  # Allow program to exit even if thread is running
        self.socket_thread.start()

        #Initializes the input text box
        self.input_text = tk.Text(master=self.input_frame, height=2, width=40, background="green", fg="white")
        self.input_text.pack()

        #Initilizes the send button to clear the input box and send it to the server
        self.send_button = tk.Button(master=master, text="SEND!", command=self.format_and_send, background="white")
        self.send_button.pack()
        

        #Updates all the gui
        self.update_gui()

    def read_socket(self):
        host = '127.0.0.1'  # Or "localhost"
        port = 5000         # Replace with your port

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                #Saves a reference to the server socket in order to also send data to the server
                self.server_socket = s
                #Debug
                #print("Connected to server")
                s.connect((host, port))
                while self.running:
                    data = s.recv(1024)
                    #Debugging print
                    if not data:
                        break
                    self.data_queue.put(data.decode())
        except Exception as e:
             self.data_queue.put(f"Error: {e}")
             #DEBUG + FEATURe
             self.close()
             #Add a line that closes the connection app if the connection to the server is lost

    def update_gui(self):
        try:
            data = self.data_queue.get_nowait()
            self.update_messageboard(data)
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
            if self.server_socket:
                self.server_socket.sendall(message)
        except Exception as e:
            print(f"{e}")
    def format_and_send(self):
        #Debugging code
        #print("Formatting and sending!")
        #Extracts the whole text from input box
        input_text = self.input_text.get("1.0", tk.END).strip()

        #Creates a list of the first two lines
        lines = input_text.splitlines()[:2]

        #Rejoins the two lines together
        message = "\n".join(lines) 
        
        #Adds username tag to message (username: message)
        message = self.username + ": " + message
        #Clears the input box after extracting the first two lines of text
        self.input_text.delete("1.0", tk.END)

        #Debug
        #print(f"Sent: {message}")

        #Calls send data function to send the message to the server
        self.send_data(message.encode('utf-8'))
    
    def update_messageboard(self, message):
        #Enable editing to insert text
        self.message_board.config(state=tk.NORMAL)  
        self.message_board.insert(tk.END, message + '\n\n')  # Insert the message
        self.message_board.config(state=tk.DISABLED)  # Disable editing to make it read-only
        self.message_board.yview(tk.END)  # Scroll to the bottom to show the latest message
root = tk.Tk()
app = App(root)
root.protocol("WM_DELETE_WINDOW", app.close) # Handle window close event
root.mainloop()