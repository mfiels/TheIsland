import socket
import json
import time

connection = None

def connect_as_algorithm(name, num_proposers, num_acceptors, num_learners):
  base = dict()
  base['configuration'] = dict()
  base['configuration']['proposers'] = num_proposers
  base['configuration']['acceptors'] = num_acceptors
  base['configuration']['learners'] = num_learners
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
  except:
    print('Error connecting to API')

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
  except:
    print('Error sending to API')

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
  except:
    print('Error receiving from API')


def disconnect():
  try:
    global connection
    connection.close()
    connection = None
  except:
    print('Error disconnecting from API')
