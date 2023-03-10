import argparse
import logging
import socket
import sys
import select
import threading
import json
import time
import os
from pathlib import Path

import Redis



BUFSIZE = 8192 # Tamaño máximo del buffer que se puede utilizar
TIMEOUT_CONNECTION = 3600 # Timout para la conexión persistente
BACKUP_TIME = 60        #Time between backups in seconds
JSON_FILE = '.pyredis.json'


def save(map):
    with open(JSON_FILE, "w") as write_file:
        json.dump(map, write_file)

def load():
    with open(JSON_FILE, "r+") as json_file:
        data = json.load(json_file)
        return data

redis = None
if not os.path.exists(JSON_FILE):
    Path(JSON_FILE).touch(exist_ok=True)
    redis = Redis.Redis()
else: 
    redis = Redis.Redis(load())





def cerrar_conexion(cs):
    """ Esta función cierra una conexión activa.
    """
    try: 
        cs.close()
    except socket.error:
        pass


def recibir_mensaje(cs):
    """ Esta función recibe datos a través del socket cs
        Leemos la información que nos llega. recv() devuelve un string con los datos.
    """
    try:
        datos = cs.recv(BUFSIZE)
    except BlockingIOError:
        print("Exception: recibir_mensaje(). Resource temporarily unaviable.", file=sys.stderr)
    
    return datos.decode()

def enviar_mensaje(cs, data):
    """ Esta función envía datos (data) a través del socket cs
        Devuelve el número de bytes enviados.
    """
    try: 
        return cs.send(data.encode())
    except BlockingIOError:
        print("Exception: enviar_mensaje(). Resource temporarily unaviable.", file=sys.stderr)

def process_web_request(cs):

    while(True):
        rsublist, wsublist, xsublist = select.select([cs], [], [], TIMEOUT_CONNECTION)

        # * Si es por timeout, se cierra el socket tras el período de persistencia.
        if(not rsublist):    
            print("\n\nHa saltado el Timeout.", file=sys.stderr)
            cerrar_conexion(cs)
            sys.exit(-1)
            

        data = recibir_mensaje(cs)

        if(not data):
            cerrar_conexion(cs)
            sys.exit(1)

        print(f"+ cmd: {data.strip()}")
        if data.strip() == "EXIT":
            enviar_mensaje(cs, f"pyredis> exiting...\n")
            cerrar_conexion(cs)
            sys.exit(0)

        res = redis.execute(data)

        if res:
            print(f"+ res: {res}")
            enviar_mensaje(cs, f"pyredis> {res}\n")
        else:
            enviar_mensaje(cs, f"pyredis> please enter a valid command - SET key value, GET key, DEL key, EXIT\n")



def save_thread(t):

    if t == None:
        t = BACKUP_TIME

    while True:
        time.sleep(t)
        print('Persistence Thread saved current data.')
        save(redis.map)

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", help="Puerto del servidor", type=int, required=True)
    parser.add_argument("-t", "--time", help="time rate between backups", type=int, required=False)
    parser.add_argument("-s", "--save", help="Enable persistence", action='store_true', required=False)
    parser.add_argument('--verbose', '-v', action='store_true', help='Incluir mensajes de depuración en la salida')
    args = parser.parse_args()

    logger = logging.getLogger()

    t = None
    if args.time:
        t = args.time

    if args.save:
        save_t = threading.Thread(target=save_thread, args=[t])
        save_t.start()



    if args.verbose:
        logger.setLevel(logging.DEBUG)

    logger.info('Enabling server in port {}.'.format(args.port))


    #Con with, se gestiona tambien los try except.
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as s1:
        
        s1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        s1.bind(("0.0.0.0", args.port))

        s1.listen(64)


        while(True):
            try:
                new_socket, addr_cliente = s1.accept()

            except socket.error:
                print("Error: accept del socket", file = sys.stderr)
                s1.close()
            
            print(f"- Request from {addr_cliente}")
            x = threading.Thread(target= process_web_request, args=[new_socket])
            x.start()



if __name__ == "__main__":
    main()

