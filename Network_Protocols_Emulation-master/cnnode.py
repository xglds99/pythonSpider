import socket
import sys
import json
import time
import random
from queue import Queue
from time import strftime
from threading import Thread


class MyException(Exception): pass


class Timer():
    def __init__(self, interval):
        self.time = None
        self.status = False
        self.interval = interval

    def start(self):
        self.time = time.time()
        self.status = True

    def stop(self):
        self.status = False

    def timeout(self):
        return self.status and (time.time() - self.time) > self.interval


class Probe():
    def __init__(self, seq, ack, port):
        self.seq = seq
        self.ack = False
        self.port = port

    def send(self):
        ### has sending interval
        port = int(self.port)
        s.sendto(bytes(
            json.dumps({'tag': 'probe', 'seq': self.seq, 'ack': self.ack, 'local_port': routing_table['local_port']}),
            'utf-8'), ('127.0.0.1', port))


class Window():
    def __init__(self, port):
        self.base = 0
        self.nextseq = 0
        self.size = 5
        self.timer = Timer(0.5)
        self.probe_list = []
        self.port = port

    def reset(self):
        self.base = 0
        self.nextseq = 0
        window.timer.stop()
        self.probe_list = []  ### like a buffer

    def move_list(self, original_base, message_length):
        ### a new packet acked
        for i in range(original_base, self.base):
            if self.probe_list:
                self.probe_list.pop(0)

    ### don't need to append since this list is put all message at the begining
    def increase_nextseq(self):
        ### a new packet sent
        self.nextseq = self.nextseq + 1


def send_probe(window, Summary_timer, DV_timer):
    while info_table['setup'] == False:
        pass
    Summary_timer.start()
    DV_timer.start()
    while True:
        ### reinitialize for the next round
        window.reset()
        end = window.base + info_table['message_length']
        while window.base < end:
            if window.nextseq < window.base + window.size and window.nextseq < 10:
                probe = Probe(window.nextseq, False, window.port)
                window.probe_list.append(probe)
                probe.send()
                if window.base == window.nextseq:
                    window.timer.start()
                window.nextseq += 1
            if window.timer.timeout():
                window.timer.start()
                for probe in window.probe_list:
                    probe.send()
        time.sleep(1)  ## sending interval


def receive_ack(window):
    while True:
        for port, queue in queue_table.items():
            if port == window.port:
                packet = queue.get()
        if packet['tag'] == 'probe' and packet['ack'] == True and int(window.port) == packet['local_port'] and packet[
            'seq'] != -1:  ### ack never drop
            # ### should judge the port
            tmpbase = window.base
            window.base = packet['seq'] + 1
            window.move_list(tmpbase, info_table['message_length'])
            if window.base == window.nextseq:
                window.timer.stop()
            else:
                window.timer.start()


def update_routing_table(packet):
    update_table['dv_update'] = False
    client_port = packet['local_port']
    for port, value in packet.items():
        if isinstance(value, dict):
            if int(port) == routing_table['local_port']:
                if routing_table[str(client_port)]['distance'] != value['distance'] and routing_table[str(client_port)][
                    'nexthop'] == None:  ### update distance
                    routing_table[str(client_port)]['distance'] = value['distance']
                    update_table['distance_update'] = True

    for port, value in packet.items():
        if isinstance(value, dict):
            distance = value['distance'] + routing_table[str(client_port)]['distance']
            if int(port) != routing_table['local_port']:
                if port in routing_table:
                    if routing_table[port]['distance'] > distance or routing_table[port]['nexthop'] == client_port:
                        update_table['dv_update'] = True
                        routing_table[port]['distance'] = distance
                        routing_table[port]['nexthop'] = client_port
                else:
                    update_table['dv_update'] = True
                    routing_table[port] = {'receive_from': False, 'send_to': False, 'distance': distance,
                                           'received_number': 0, 'discarded_number': 0, 'nexthop': client_port,
                                           'probability': None}


def receive_probe_DV():
    while True:
        data, clientaddress = s.recvfrom(2048)
        packet = json.loads(data.decode('utf-8'))
        if packet['tag'] == 'probe' and packet['ack'] == True:
            for port, queue in queue_table.items():
                queue_table[port].put(packet)
        elif packet['tag'] == 'probe' and packet['ack'] == False:
            port = packet['local_port']
            if discard_or_not(packet) == False:
                if packet['seq'] == info_table[str(port)]:
                    info_table[str(port)] += 1
                s.sendto(bytes(json.dumps({'tag': 'probe', 'seq': info_table[str(port)] - 1, 'ack': True,
                                           'local_port': routing_table['local_port']}), 'utf-8'), ('127.0.0.1', port))
            else:
                pass
            if packet['seq'] == info_table['message_length'] - 1:
                info_table[str(port)] = 0
                loss_rate = cal_link_loss(routing_table[str(port)]['received_number'],
                                          routing_table[str(port)]['discarded_number'])
                if loss_rate != 0 and routing_table[str(port)]['nexthop'] == None:
                    routing_table[str(port)]['distance'] = loss_rate
        elif packet['tag'] == 'routing_table':
            if info_table['setup'] == False:
                info_table['setup'] = True
                receive_or_not = True
                broadcast_to_neighbor()
            else:
                update_routing_table(packet)
            if update_table['dv_update'] == True:
                print('[' + str(time.time()) + '] Node ' + str(routing_table['local_port']) + ' Rounting Table')
                sys.stdout.flush()
                for port, value in routing_table.items():
                    if isinstance(value, dict):
                        if value['nexthop']:
                            print(
                                '- (' + str(value['distance']) + ') -> Node ' + str(port) + '; Next hop -> Node ' + str(
                                    value['nexthop']))
                            sys.stdout.flush()
                        else:
                            print('- (' + str(value['distance']) + ') -> Node ' + str(port))
                            sys.stdout.flush()


def timer_update(Summary_timer, DV_timer):
    while True:
        if Summary_timer.timeout():
            for port, value in routing_table.items():
                if isinstance(value, dict):
                    if value['receive_from'] == True:
                        loss_rate = cal_link_loss(value['received_number'], value['discarded_number'])
                        print('[' + str(time.time()) + '] Link to ' + str(port) + ': ' + str(
                            value['received_number']) + 'packets received, ' + str(
                            value['discarded_number']) + ' packets lost, lost rate ' + str(loss_rate))
                        sys.stdout.flush()
            Summary_timer.start()
        if DV_timer.timeout():
            update_table['distance_update'] = False
            print('[' + str(time.time()) + '] Node ' + str(routing_table['local_port']) + ' Rounting Table')
            sys.stdout.flush()
            for port, value in routing_table.items():
                if isinstance(value, dict):
                    if value['nexthop']:
                        print('- (' + str(value['distance']) + ') -> Node ' + str(port) + '; Next hop -> Node ' + str(
                            value['nexthop']))
                        sys.stdout.flush()
                    else:
                        print('- (' + str(value['distance']) + ') -> Node ' + str(port))
                        sys.stdout.flush()
                    if value['receive_from'] or value['send_to']:  ## if it is neighor
                        if original_distance[port] != value['distance']:  ## if update, update itself is not here!!
                            original_distance[port] = value['distance']
                            s.sendto(bytes(json.dumps(routing_table), 'utf-8'), ('', int(port)))
            DV_timer.start()


def discard_or_not(packet):
    ### receiver side
    #### ack and DV will never be dropped!!!!!!!
    #### index is the index in receive_from list
    port = str(packet['local_port'])
    routing_table[port]['received_number'] += 1
    if random.random() > routing_table[port]['probability']:
        return False
    else:
        routing_table[port]['discarded_number'] += 1
        return True


def cal_link_loss(receive, drop):
    if receive == 0:
        return 0
    else:
        return round(float(drop) / receive, 2)


def initialization():
    input_info = sys.argv
    local_port = None
    try:
        local_port = int(sys.argv[1])
    except:
        raise MyException("port number should be integer between 1024 and 65534")
    i = 1
    while i < len(input_info):
        i = i + 1
        if input_info[i] == 'receive':
            while True:
                i = i + 1
                try:
                    port = int(input_info[i])
                    routing_table[str(port)] = {'receive_from': True, 'send_to': False, 'distance': 100,
                                                'received_number': 0, 'discarded_number': 0, 'nexthop': None,
                                                'probability': 0}
                except:
                    try:
                        probability = float(input_info[i])
                        routing_table[str(port)]['probability'] = probability
                    except:
                        break
        if input_info[i] == 'send':
            while True:
                i = i + 1
                try:
                    port = int(input_info[i])
                    if str(port) in routing_table:
                        routing_table[str(port)]['send_to'] = True
                    else:
                        routing_table[str(port)] = {'receive_from': False, 'send_to': True, 'distance': 100,
                                                    'received_number': 0, 'discarded_number': 0, 'nexthop': None,
                                                    'probability': 0}
                except:
                    if i == len(input_info):
                        break
                    elif input_info[i] == 'last':
                        info_table['setup'] = True
                        info_table['is_last'] = True
    routing_table['local_port'] = local_port


def broadcast_to_neighbor():
    for port, value in routing_table.items():
        if isinstance(value, dict):
            port = int(port)
            s.sendto(bytes(json.dumps(routing_table), 'utf-8'), ('', int(port)))


if __name__ == '__main__':
    info_table = {'setup': False, 'message_length': 10,
                  'is_last': False}
    routing_table = {'tag': 'routing_table', 'local_port': None,
                     'timestamp': None}
    queue_table = {}
    original_distance = {}
    update_table = {'dv_update': False, 'distance_update': False}
    initialization()
    for port, value in routing_table.items():
        if isinstance(value, dict):
            original_distance[port] = value['distance']
            if value['receive_from']:
                info_table[port] = 0
            if value['send_to']:
                queue = Queue()
                queue_table[port] = queue
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', routing_table['local_port']))
    if info_table['is_last']:
        broadcast_to_neighbor()
        print('[' + str(time.time()) + '] Node ' + str(routing_table['local_port']) + ' Rounting Table')
        sys.stdout.flush()
        for port, value in routing_table.items():
            if isinstance(value, dict):
                if value['nexthop']:
                    print('- (' + str(value['distance']) + ') -> Node ' + str(port) + '; Next hop -> Node ' + str(
                        value['nexthop']))
                    sys.stdout.flush()
                else:
                    print('- (' + str(value['distance']) + ') -> Node ' + str(port))
                    sys.stdout.flush()
    Summary_timer = Timer(1)
    DV_timer = Timer(3)
    t0 = Thread(target=timer_update, args=(Summary_timer, DV_timer,))
    t0.setDaemon(True)
    t0.start()
    t1 = Thread(target=receive_probe_DV, args=())
    t1.setDaemon(True)
    t1.start()
    for port, value in routing_table.items():
        if isinstance(value, dict):
            if value['send_to']:
                window = Window(port)
                t2 = Thread(target=send_probe, args=(window, Summary_timer, DV_timer,))
                t3 = Thread(target=receive_ack, args=(window,))
                t2.setDaemon(True)
                t3.setDaemon(True)
                t2.start()
                t3.start()
            elif info_table['setup']:
                if not info_table['is_last']:
                    print('[' + str(time.time()) + '] Node ' + str(routing_table['local_port']) + ' Rounting Table')
                    sys.stdout.flush()
                    for port, value in routing_table.items():
                        if isinstance(value, dict):
                            if value['nexthop']:
                                print('- (' + str(value['distance']) + ') -> Node ' + str(
                                    port) + '; Next hop -> Node ' + str(value['nexthop']))
                                sys.stdout.flush()
                            else:
                                print('- (' + str(value['distance']) + ') -> Node ' + str(port))
                                sys.stdout.flush()
                Summary_timer.start()
                DV_timer.start()
    while True:
        pass
