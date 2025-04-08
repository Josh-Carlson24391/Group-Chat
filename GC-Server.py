from threading import Thread

def handleClient(sock):
  # Handle communication with one client

  # Remember to close the socket when done
  sock.close()

server_socket.listen(___)
while some_condition_to_check_here:
  connection_socket, _ = server_socket.accept()
  t = Thread(target = handleClient, args=(connection_socket,))
  t.start()
server_socket.close()