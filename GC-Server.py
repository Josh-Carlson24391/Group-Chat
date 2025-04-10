from threading import Thread
import threading
import socket

#Server Setup
condition = True
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clients = []
HOST = '127.0.0.1'
PORT = 5000

#Creates a lock for threads to prevent two threads from modifing the clients list at the same time
client_lock = threading.Lock()


#Binding socket to Port
server_socket.bind((HOST, PORT))

#Function which takes in 1024 bytes of data and sends it to all active clients
def echo_to_clients(data):
    #Prevents threads from modifying the list of clients while the server is actively echoing
    with client_lock:
        #For each client that is currenly connected:
        for client in clients:
            #Send the most recent message
            client.sendall(data)

def handleClient(client_sock, client_addr):
    print("Handling Connection")
  # Handle communication with one client
  
    try:
        with client_lock:
            clients.append(client_sock)
        while True:
            data = client_sock.recv(1024)
            if not data:
                 #Exits the data reading loop if the client stops sending data or client disconnects
                break
            else:
                #Sends data to all clients inlcuding this one if there is new data to send
                echo_to_clients(data)

    except ConnectionResetError:
        print("Connection Abruptly Stopped\n")
    except socket.timeout:
       print("Connection Timed out\n")
    finally:
       #Remove Client from list of active clients, and close client socket
       clients.remove(client_sock)
       client_sock.close()
  # Remember to close the socket when done
  

server_socket.listen()
while condition:
  connection_socket, client_addr = server_socket.accept()
  t = Thread(target = handleClient, args=(connection_socket, client_addr))
  t.start()
  #Debug
  #print(threading.enumerate())
server_socket.close()