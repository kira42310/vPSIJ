
import sys
import shutil
from os import getenv
from pathlib import Path

import vPSIJ

def setup():
  home_dir = getenv( 'HOME' )
  gRPC_dir = f'{ home_dir }/vPSIJ_util/grpc/'
  vPSIJ_dir = vPSIJ.__path__
  python_bin_dir = '/'.join(sys.executable.split('/')[:-1])

  Path( gRPC_dir ).mkdir( parents = True, exist_ok = True )  
  shutil.copy2( f'{ vPSIJ_dir }/job_rpc_client.py', gRPC_dir )
  shutil.copy2( f'{ vPSIJ_dir }/updater_pb2.py', gRPC_dir )
  shutil.copy2( f'{ vPSIJ_dir }/updater_pb2_grpc.py', gRPC_dir )

  shutil.copy2( f'{ python_bin_dir }/vpsij-updater' )

if __name__ == '__main__':
  setup()