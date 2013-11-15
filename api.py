import socket
import json
import time

connection = None

def connect_as_algorithm(name, proposer_ids, acceptor_ids, learner_ids):
  base = dict()
  base['configuration'] = dict()
  base['configuration']['proposers'] = proposer_ids
  base['configuration']['acceptors'] = acceptor_ids
  base['configuration']['learners'] = learner_ids
  __connect__('algorithm', name, base)

def connect_as_application(name, *interests):
  base = dict()
  base['interests'] = interests
  __connect__('application', name, base)

def __connect__(type, name, base):
  try:
    global connection
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.connect(('localhost', 9000))

    message = base
    message['action'] = 'connect'
    message['type'] = type
    message['name'] = name

    __send__(message)
  except Exception as e:
    print('Error connecting to API: ' + str(e))

def request(algorithm, id, cid, value):
  message = dict()
  message['action'] = 'request'
  message['algorithm'] = algorithm
  message['id'] = id
  message['cid'] = cid
  message['value'] = value

  __send__(message)

def response(id, cid, value):
  message = dict()
  message['action'] = 'response'
  message['id'] = id
  message['cid'] = cid
  message['value'] = value

  __send__(message)

def prepare(emitter, src, dest, pid):
  message = dict()
  __send_inc__('prepare', emitter, src, dest, pid, message)

def promise(emitter, src, dest, pid, value):
  message = dict()
  message['value'] = value
  __send_inc__('promise', emitter, src, dest, pid, message)

def propose(emitter, src, dest, pid, id, cid, value):
  message = dict()
  message['id'] = id
  message['cid'] = cid
  message['value'] = value
  __send_inc__('propose', emitter, src, dest, pid, message)

def accept(emitter, src, dest, pid, id, cid, value):
  message = dict()
  message['id'] = id
  message['cid'] = cid
  message['value'] = value
  __send_inc__('accept', emitter, src, dest, pid, message)

def nack(emitter, src, dest, pid, id, cid, value):
  message = dict()
  message['id'] = id
  message['cid'] = cid
  message['value'] = value
  __send_inc__('nack', emitter, src, dest, pid, message)

def __send_inc__(action, emitter, src, dest, pid, base):
  base['action'] = action
  base['emitter'] = emitter
  base['src'] = src
  base['dest'] = dest
  base['pid'] = pid
  __send__(base)

def __send__(base):
  try:
    global connection
    base['time'] = int(time.time())
    json_str = json.dumps(base) + '\r\n'
    connection.send(json_str.encode('ascii'))
  except Exception as e:
    print('Error sending to API: ' + str(e))

def wait_for_request():
  return __recv__('request')

def wait_for_response():
  return __recv__('response')

def __recv__(type):
  try:
    global connection
    while True:
      message = json.loads(connection.recv(4096).decode('ascii'))
      if message['action'] == type:
        return message
  except Exception as e:
    print('Error receiving from API: ' + str(e))


def disconnect():
  try:
    global connection
    connection.close()
    connection = None
  except Exception as e:
    print('Error disconnecting from API: ' + str(e))
