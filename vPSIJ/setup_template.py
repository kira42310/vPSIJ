
import os
import shutil
import urllib3
import zipfile
import json
from pathlib import Path

def setup():

  print( f'{ '#' * 10 } Script start! { '#' * 10 }' )
  template_url = 'https://github.com/kira42310/vPSIJ_scheduler_template/archive/refs/heads/main.zip'
  
  home_dir = os.getenv( 'HOME' )
  util_dir = f'{ home_dir }/vPSIJ_util/'
  template_dir = f'{ util_dir }/sche_template'
  zip_loc = f'{ util_dir }/vpsij-template.zip'
  
  print( f'{ '#' * 10 } mdkir vPSIJ_util directory in home directory { '#' * 10 }' )
  Path( util_dir ).mkdir( parents = True, exist_ok = True )
  print( "# Success!")
  
  print( f'{ '#' * 10 } Download vPSIJ template repository from GitHub { '#' * 10 }' )
  http = urllib3.PoolManager()
  with http.request( "GET", template_url, preload_content = False ) as response:
    with open( zip_loc, 'wb' ) as outf:
      shutil.copyfileobj( response, outf )
  print( "# Success!")
  
  print( f'{ '#' * 10 } Unzip repository zip file and move sche_template directory to the vPSIJ_util dirctory { '#' * 10 }' )
  with zipfile.ZipFile( zip_loc, 'r' ) as zipf:
    zipf.extractall( util_dir )
  shutil.move( f'{ util_dir }/vPSIJ_scheduler_template-main/sche_template', util_dir )
  print( "# Success!")
  
  print( f'{ '#' * 10 } Generate template_location.json in vPSIJ_util { '#' * 10 }' )
  sche_dict = { d.name: str( d ) for d in Path( template_dir ).iterdir() if d.is_dir() }
  with open( f'{ util_dir }/template_location.json', 'w' ) as outf:
    json.dump( sche_dict, outf )
  print( "# Success!")
  
  print( f'{ '#' * 10 } Remove vPSIJ template repository zip file and extracted directory { '#' * 10 }' )
  shutil.rmtree( f'{ util_dir }/vPSIJ_scheduler_template-main' )
  os.remove( zip_loc )
  print( "# Success!")

if __name__ == '__main__':
  setup()