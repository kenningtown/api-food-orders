import socket
import math
import threading
import random

def dict_menu(txt):                 #function which loads menu.txt content to dictionary
    menu = {}
    with open(txt, "r") as file:           
        for line in file:
            elements = line.strip().split(':')          #splitting item and cost into separate parts
            food = elements[0]
            cost = elements[1]
            menu[food.lower()] = int(cost)
    return menu    





def client_processing(connection, client_address, menu):
    global response_id
    
    try:
        while True:
            
            request = connection.recv(1024).decode('utf-8').strip() #receiving the request
            response_id = random.randint(0, 2**32-1)              #generating id


            if request.lower() == 'exit':        #session stops if 'exit' is typed
                print("Session stopped.")
                break

            elem = request.split(':')
            request_id = elem[0]
            request_type = elem[1]

            if request_type == "MENU":
                #handling MENU request
                menu_content = '\n'.join([f"{food}: {cost}" for food, cost in menu.items()])
                response = f"\nResponse ID: {response_id}\nRequest ID: {request_id}\nRequest type: MENU\n-------\n{menu_content}"
                connection.sendall(response.encode('utf-8'))
                
            elif request_type == "ORDR":  #handling orders
                food, amnt = elem[2], elem[3]
                if food in menu:
                    total_price = menu[food] * int(amnt)
                    response = f"\nResponse ID: {response_id}\nRequest ID: {request_id}\nRequest type: ORDR\n-------\n<200> Successfully processed: {food} x {amnt}\nTotal: {total_price}"
                else:
                    response = "ERROR 404! Item is not found!"
                connection.sendall(response.encode('utf-8'))
            
            elif request_type == "PAYM":       #handling payments
                nm, addr, card, money = elem[2], elem[3], elem[4], elem[5]
                if int(money) >= total_price: 
                    response = f"\nResponse ID: {response_id}\nRequest ID: {request_id}\nRequest type: PAYM\n-------\n<200> Successfull payment!\nThank you!"
                else:
                    response = "ERROR 404! Not enough for payment!"
                connection.sendall(response.encode('utf-8'))




    finally:
            #cleaning the connection
        connection.close()



server_ip = '127.0.0.1'
server_port = 8080

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip, server_port))    #binding socket to ip and port
server_socket.listen()                          #waiting for new connections



print("At your service!")    #opening message from server

menu = dict_menu("menu.txt")   #loading text file content to a menu





while True:
    
    connection, client_address = server_socket.accept()  #connection wait

    #opening new thread to handle the connection
    thread = threading.Thread(target=client_processing, args=(connection, client_address, menu))
    thread.start()



client_socket.close()
server_socket.close()
