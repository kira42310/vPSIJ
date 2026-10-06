
import sys
import shutil
from os import getenv
from pathlib import Path

import vPSIJ

def setup():
  print( f"{ '#' * 10 } Script start! { '#' * 10 }" )
  home_dir = getenv( 'HOME' )
  gRPC_dir = f'{ home_dir }/vPSIJ_util/grpc/'
  vPSIJ_dir = vPSIJ.__path__[0]
  python_bin_dir = '/'.join(sys.executable.split('/')[:-1])

  print( f"{ '#' * 10 } mkdir grpc directory in ~/vPSIJ_util/ { '#' * 10 }" )
  Path( gRPC_dir ).mkdir( parents = True, exist_ok = True )  
  print( "# Success!")

  print( f"{ '#' * 10 } Copy job_rpc_client.py and depecdencies to ~/vPSIJ_util/grpc/  { '#' * 10 }" )
  shutil.copy2( f'{ vPSIJ_dir }/job_rpc_client.py', gRPC_dir )
  shutil.copy2( f'{ vPSIJ_dir }/updater_pb2.py', gRPC_dir )
  shutil.copy2( f'{ vPSIJ_dir }/updater_pb2_grpc.py', gRPC_dir )
  print( "# Success!")

  print( f"{ '#' * 10 } Copy vpsij-updater cmd to ~/vPSIJ_util/grpc/  { '#' * 10 }" )
  shutil.copy2( f'{ python_bin_dir }/vpsij-updater', gRPC_dir )
  print( "# Success!")

if __name__ == '__main__':
  setup()