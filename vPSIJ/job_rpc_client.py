from os import getenv
from sys import argv
import grpc
import executor_pb2
import executor_pb2_grpc

# grpc_server = getenv( 'GRPC_SERVER' )
# secure = int( getenv( 'SECURE_CHANNEL' ) )
grpc_server = argv[1]
secure = bool( int( argv[2] ) )
response = argv[3]
# print( grpc_server, secure, response )

if secure:
  sechannel = grpc.secure_channel
else:
  sechannel = grpc.insecure_channel

with sechannel( grpc_server ) as channel:
  stub = executor_pb2_grpc.UpdateServiceStub( channel )
  request = executor_pb2.UpdateRequest( state = response )
  print( f'{request.state}' )
  response = stub.UpdateStatus( request )
  print( f'{response.result}' )