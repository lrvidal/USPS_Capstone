import socket
import datetime

# The IP address of the server (this should be the IP address of the receiving machine)
HOST = '0.0.0.0'  # This will listen on all available network interfaces
PORT = 5000

# Create a socket
s = socket.socket()

# Bind the socket to the IP address and port
s.bind((HOST, PORT))

# Listen for incoming connections
s.listen()

print('Server is listening...')

# Accept an incoming connection
conn, addr = s.accept()

print('Connected by', addr)
date = datetime.now()
# Open a file in binary mode to write the incoming data
with open('data_{}_{}_{}.csv'.format(date.month(), date.day(), date.year()), 'wb') as f:
    while True:
        # Receive data from the client
        data = conn.recv(1024)

        # If no more data is received, break the loop
        if not data:
            break

        # Write the received data to the file
        f.write(data)

# Close the connection
conn.close()

print('File received.')