import socket
import sys
import json
import time
import random
from queue import Queue
from time import strftime
from threading import Thread


def get_from_buffer(sequence_number, data_buffer):
    return data_buffer[sequence_number]


def remove_from_buffer(packet, data_buffer):
    data_buffer[packet['seq']] = None  ##### test if 32 bit can be used like this!!!!!!


class MyTimer:
    def __init__(self):
        self.time = None
        self.status = False

    def start(self):
        self.time = time.time()
        self.status = True

    def stop(self):
        self.status = False

    def timeout(self):
        return self.status and (time.time() - self.time) > 0.5


class MyException(Exception):
    pass


def init():
    if len(sys.argv) == 6:
        try:
            self_port, peer_port, window_size = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
        except:
            raise MyException("port number and window size should be integer")
            sys.exit()
        if sys.argv[4] != '-d' and sys.argv[4] != '-p':
            raise MyException('-d for deterministic way to drop packet, -p for probabilistic way to drop packet')
            sys.exit()
        else:
            drop_mode = sys.argv[4]
            drop_value = float(sys.argv[5])
    else:
        raise MyException(
            "please input as the following format:\n>>> python gbnnode.py <self_port> <peer_port> <window_size> [-d "
            "<value_of_n>|-p <value_of_n>]")
        sys.exit()
    return self_port, peer_port, window_size, drop_mode, drop_value


def input_message(message_queue):
    while True:
        try:
            print('node> '),
            input_data = input()
            if input_data.startswith('send '):
                message = input_data[5:]
                message_queue.put(message)
            else:
                raise MyException("please input as the following format:\n>>> send <message>")
                sys.exit()
        except Exception as x:
            print(str(x))
            sys.exit()


def put_into_buffer(message_queue, data_buffer):
    while True:
        message = message_queue.get()
        window_list['message_length'] = window_list['message_length'] + len(message)
        for i in range(0, len(message)):
            sequence_number = window_list['message_length'] - len(message) + i
            data = message[i]
            data_buffer[window_list['message_length'] - len(message) + i] = {'seq': sequence_number, 'data': str(data),
                                                                             'ack': False}


def send_packet(packet, peer_port):
    s.sendto(bytes(json.dumps(packet), 'utf-8'), ('', peer_port))
    if not packet['ack']:
        print('[' + str(time.time()) + ']' + 'packet' + str(packet['seq']) + ' ' + packet['data'] + ' sent')
    else:
        print('[' + str(time.time()) + ']' + 'ACK' + str(packet['seq']) + ' sent, expecting packet' + str(
            packet['seq'] + 1))


def discard_packet(received_number_list, packet, drop_mode, drop_value):
    ### return boolean value, True: discard, False: not_discard
    if drop_mode == '-d':

        if (received_number_list[0]) % int(drop_value) != 0:
            return False
        else:
            if not packet['ack']:
                print(
                    '[' + str(time.time()) + ']' + 'packet' + str(packet['seq']) + ' ' + packet['data'] + ' discarded')
            elif packet['ack']:
                print('[' + str(time.time()) + ']' + 'ACK' + str(packet['seq']) + ' discarded')
            return True
    if drop_mode == '-p':
        if random.random() > drop_value:
            return False
        else:
            if not packet['ack']:
                print(
                    '[' + str(time.time()) + ']' + 'packet' + str(packet['seq']) + ' ' + packet['data'] + ' discarded')
            elif packet['ack']:
                print('[' + str(time.time()) + ']' + 'ACK' + str(packet['seq']) + ' discarded')
            return True


def loss_rate_calculation(dropped, total):
    loss_rate = float(dropped) / total
    print('[Summary] ' + str(dropped) + '/' + str(total) + ' packets dropped, loss rate = ' + str(loss_rate))
    print('node> '),
    sys.stdout.flush()


def send(peer_port, window_size, drop_mode, drop_value, ack_list, data_buffer, timer, window_list):
    while True:
        if timer.timeout():
            print('[' + str(time.time()) + ']' + 'packet' + str(window_list['base']) + ' timeout')
            for i in range(window_list['base'], window_list['nextseq']):  ## python it means to nextseq - 1
                packet = get_from_buffer(i, data_buffer)
                send_packet(packet, peer_port)
            timer.start()
        if window_list['nextseq'] < window_list['base'] + window_size:
            if data_buffer[window_list['nextseq']] != None:
                packet = get_from_buffer(window_list['nextseq'], data_buffer)
                window_list['nextseq'] = window_list['nextseq'] + 1
                send_packet(packet, peer_port)
                timer.start()


def receive(peer_port, timer_list, window_list, data_buffer, received_seq_list, drop_mode, drop_value):
    global last_received_seq
    received_number_list = [0]
    dropped = 0
    while True:
        try:
            data, clientaddress = s.recvfrom(2048)
        except socket.error:
            continue
        packet = json.loads(data.decode('utf-8'))
        if packet['ack'] == False and packet['seq'] == -2:
            loss_rate_calculation(dropped, received_number_list[0])
            timer.stop()
        else:
            received_number_list[0] = received_number_list[0] + 1
            if not discard_packet(received_number_list, packet, drop_mode, drop_value):
                if packet['ack'] == False and packet['seq'] != -2:
                    print('[' + str(time.time()) + ']' + 'packet' + str(packet['seq']) + ' ' + packet[
                        'data'] + ' received')
                    if packet['seq'] == 0 or received_seq_list[packet['seq'] - 1] == True:
                        ack_packet = {'seq': packet['seq'], 'data': None, 'ack': True}
                        received_seq_list[packet['seq']] = True
                        send_packet(ack_packet, peer_port)
                    else:
                        for i in range(len(received_seq_list)):
                            if not received_seq_list[i]:
                                last_received_seq = i - 1
                                break
                        ack_packet = {'seq': last_received_seq, 'data': None, 'ack': True}
                        send_packet(ack_packet, peer_port)


                elif packet['ack'] == True:
                    ### sender
                    print(
                        '[' + str(time.time()) + ']' + 'ACK' + str(packet['seq']) + ' received, window moves to ' + str(
                            packet['seq'] + 1))
                    if data_buffer[packet['seq']] is None:
                        pass
                    else:  ### ack means all previous packet has been received
                        data_buffer[packet['seq']] = None
                        window_list['base'] = packet['seq'] + 1
                        if window_list['base'] != window_list['nextseq']:
                            timer.start()
                        elif window_list['base'] == window_list['nextseq']:
                            timer.stop()
                            if window_list['base'] == window_list['message_length']:
                                loss_rate_calculation(dropped, received_number_list[0])
                                timer.stop()
                                s.sendto(bytes(json.dumps({'seq': -2, 'data': None, 'ack': False}), 'utf-8'),
                                         ('', peer_port))


            else:
                dropped = dropped + 1


if __name__ == '__main__':
    try:
        self_port, peer_port, window_size, drop_mode, drop_value = init()
        data_buffer = [None for i in range(2000)]
        window_list = {'base': 0, 'nextseq': 0, 'message_length': 0, 'expected': 0}
        timer = MyTimer()
        ack_list = {'seq': -1, 'status': False}
        received_seq_list = [False for i in range(2000)]
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(('', self_port))
        send_thread = Thread(target=send,
                             args=(
                                 peer_port, window_size, drop_mode, drop_value, ack_list, data_buffer, timer,
                                 window_list))
        receive_thread = Thread(target=receive,
                                args=(
                                    peer_port, timer, window_list, data_buffer, received_seq_list, drop_mode,
                                    drop_value))
        send_thread.setDaemon(True)
        receive_thread.setDaemon(True)
        send_thread.start()
        receive_thread.start()
        message_queue = Queue()
        t3 = Thread(target=input_message, args=(message_queue,))
        t3.setDaemon(True)
        t3.start()
        t0 = Thread(target=put_into_buffer, args=(message_queue, data_buffer))  ### to be modify
        t0.setDaemon(True)
        t0.start()
        while 1:
            pass
    except KeyboardInterrupt:
        print(">>> Bye")
        raise KeyboardInterrupt
        sys.exit()
    except Exception as x:
        print(">>> " + str(x))
        sys.exit()
    finally:
        sys.exit()
