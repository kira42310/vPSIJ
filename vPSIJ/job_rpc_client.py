from os import getenv
from sys import argv
import grpc
from . import updater_pb2
from . import updater_pb2_grpc


def update():
  grpc_server = argv[1]
  secure = bool( int( argv[2] ) )
  response = argv[3]

  if secure:
    sechannel = grpc.secure_channel
  else:
    sechannel = grpc.insecure_channel

  with sechannel( grpc_server ) as channel:
    stub = updater_pb2_grpc.UpdateServiceStub( channel )
    request = updater_pb2.UpdateRequest( state = response )
    print( f'{request.state}' )
    response = stub.UpdateStatus( request )
    print( f'{response.result}' )