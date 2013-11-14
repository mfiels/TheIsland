import api

print('Connecting to API...')
api.connect_as_application('application', 'response')

print('Requesting vertical paxos...')
api.request('vertical-paxos', 0, 0, 3)

print('Waiting for response from vertical paxos...')
response = api.wait_for_response()

print('Got response from vertical paxos...')
print(str(response))
