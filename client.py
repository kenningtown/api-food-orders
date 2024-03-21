import socket
import random

server_ip = '127.0.0.1'
server_port = 8080

clients_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

did_order = False

try:
    
    clients_socket.connect((server_ip, server_port)) #connecting to the server

    while True:

        
        request_id = random.randint(0, 2**32-1)   #generating id

        print(f"\nRequest ID: #{request_id}")    #header part
        request_type = input(f"Enter request (MENU, ORDR, PAYM) or type 'exit': ").strip().upper()     #entering request type, header part
        
        if request_type.lower() == 'exit':                    #session stops
            clients_socket.sendall(request_type.encode('utf-8'))
            break

        elif request_type == 'MENU':                    #displaying menu
            msg = f"{request_id}:{request_type}"
            clients_socket.sendall(msg.encode('utf-8'))
           

        elif request_type == 'ORDR' and not did_order:            #making an order, boolean did_order makes sure that user doesn't make consecutive order, he should pay right away
            print("------")
            name = input("Enter the item: ").lower()       #body starts here (---- is a delimiter between header and body)
            amount = int(input("Enter the amount: "))
            msg = f"{request_id}:{request_type}:{name}:{amount}"
            clients_socket.sendall(msg.encode('utf-8'))

        elif request_type == 'PAYM' and did_order:               #payment option is available only if the order is done succesfully
            print("------")
            customer = input("Enter your name: ")          #body starts here (---- is a delimiter between header and body)
            address = input("Enter your address: ")
            card_num = input("Enter your card number: ")
            money = int(input("Type the amount: "))
            msg = f"{request_id}:{request_type}:{customer}:{address}:{card_num}:{money}"
            clients_socket.sendall(msg.encode('utf-8'))
            

        else:
            msg = "Your request is incorrect!"     #if user enters request type other than above, terminal will keep asking until the correct option is chosen
            print(msg)
            continue


        # receiving response from server
        response = clients_socket.recv(1024).decode('utf-8')

        if "Successfully" in response:                      #cases that decide did-order value, it is needed to a proper work of ordr and paym
            did_order = True
        elif "not found" in response:
            did_order = False
        elif "Successful" in response:
            did_order = False

       #server responds:
        print(response)

finally:
     #connection closes
    clients_socket.close()
    print("Connection closed.")