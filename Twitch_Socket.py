import socket
import logging
from emoji import demojize
import Controle_Inputs
import time

server = 'irc.chat.twitch.tv'
port = 6667
nickname = 'RodssOliveira'
token = 'oauth:ahcfw1lu5mjbhy2kzsjg2a5k7g1196'
channel = '#rodssoliveira'

'''
Direita = Seta para Direita = 0x4D
Esquerda = Seta para Esquerda = 0x4B
Pular = Espaço = 0x39
'''

def main():
    sock = socket.socket()
    sock.connect((server, port))
    sock.send(f"PASS {token}\r\n".encode('utf-8'))
    sock.send(f"NICK {nickname}\r\n".encode('utf-8'))
    sock.send(f"JOIN {channel}\r\n".encode('utf-8'))

    try:
        while True:
            resp = sock.recv(2048).decode('utf-8')

            user = None
            if resp.startswith('PING'):
                # sock.send("PONG :tmi.twitch.tv\n".encode('utf-8'))
                sock.send("PONG\n".encode('utf-8'))
            elif len(resp) > 0:
                msg = demojize(resp)
                user_msg = msg.split('G #')
                action = msg.split(' :')

                try:
                    user_msg = user_msg[1].split(" :")
                    user = user_msg[0]
                    msg = user_msg[1].split('\r')

                    jPower = '.' + str(msg[0][2:])
                except Exception as ex:
                    pass
                
                if user:
                    if jPower == '.100':
                        jPower = 1

                    if action[1].startswith('r') and len(msg[0]) == 1: #Right
                        print(f'{user}: Direita')
                        Controle_Inputs.PressKey(0x4D)
                        time.sleep(.25)
                        Controle_Inputs.ReleaseKey(0x4D)
                        time.sleep(.25)
                    elif action[1].startswith('l') and len(msg[0]) == 1: #Left
                        print(f'{user}: Esquerda')
                        Controle_Inputs.PressKey(0x4B)
                        time.sleep(.25)
                        Controle_Inputs.ReleaseKey(0x4B)
                        time.sleep(.25)
                    elif action[1].startswith('j') and len(msg[0]) == 2: # Pulo fraco
                        print(f'{user}: Pulo')
                        Controle_Inputs.PressKey(0x39)
                        time.sleep(float(jPower))
                        Controle_Inputs.ReleaseKey(0x39)
                        time.sleep(.5)
                    elif action[1].startswith('jr') and len(msg[0]) >= 3 and len(msg[0]) <= 5:
                        print(f'{user}: Pulo para Direita')
                        Controle_Inputs.PressKey(0x39)
                        Controle_Inputs.PressKey(0x4D)
                        time.sleep(float(jPower))
                        Controle_Inputs.ReleaseKey(0x39)
                        Controle_Inputs.ReleaseKey(0x4D)
                        time.sleep(.5)
                    elif action[1].startswith('jl') and len(msg[0]) >= 3 and len(msg[0]) <= 5:
                        print(f'{user}: Pulo para Esquerda')
                        Controle_Inputs.PressKey(0x39)
                        Controle_Inputs.PressKey(0x4B)
                        time.sleep(float(jPower))
                        Controle_Inputs.ReleaseKey(0x39)
                        Controle_Inputs.ReleaseKey(0x4B)
                        time.sleep(.5)


    except KeyboardInterrupt:
        sock.close()
        exit()

if __name__ == '__main__':
    main()