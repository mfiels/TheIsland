import api

print('Connecting to API...')
api.connect_as_algorithm(
  'vertical-paxos', 
  [0, 1, 2], 
  [3, 4, 5, 6, 7], 
  [8, 9, 10, 11])

print('Waiting for requests...')
request = api.wait_for_request()

print('Got request...')
print(str(request))

print('Sending a dummy algorithmic step message...')
# A proposal is sent from process 0 -> process 1
api.propose(0, 0, 1, 0, request['id'], request['cid'], request['value'])
api.propose(1, 0, 1, 0, request['id'], request['cid'], request['value'])

# An accept is sent from process 1 -> process 0
api.accept(1, 1, 0, 0, request['id'], request['cid'], request['value'])
api.accept(0, 1, 0, 0, request['id'], request['cid'], request['value'])

print('Sending response...')
api.response(request['id'], request['cid'], request['value'])
