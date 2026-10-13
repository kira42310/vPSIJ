
import os
import sys
import shutil
import zipfile
import json
import subprocess
from pathlib import Path

def setup():

  print( f"{ '#' * 10 } Script start! { '#' * 10 }" )
  template_url = 'https://github.com/kira42310/vPSIJ_scheduler_template/archive/refs/heads/main.zip'
  
  home_dir = os.getenv( 'HOME' )
  util_dir = f'{ home_dir }/vPSIJ_util/'
  template_dir = f'{ util_dir }/sche_template'
  zip_loc = f'{ util_dir }/vpsij-template.zip'

  print( f"{ '#' * 10 } mdkir vPSIJ_util directory in home directory { '#' * 10 }" )
  util_path = Path( util_dir )
  if util_path.is_dir():
    print( "# {HOME}/vPSIJ_util directory exist! >> Skip makeing vPSIJ_util directory" )
  elif util_path.exists():
    print( "# {HOME}/vPSIJ_util found but not directory")
    print( "# Abort setup!!")
    sys.exit( 1 )
  else:
    util_path.mkdir( parents = True, exist_ok = True )
    print( "# Make {HOME}/vPSIJ_util directory: Success!" )

  # Check previous zip file and if exist remove previous zip file
  if Path( zip_loc ).is_file():
    shutil.rmtree( zip_loc )
  print( f"{ '#' * 10 } Download vPSIJ template repository from GitHub { '#' * 10 }" )
  download_cmd = [ 'curl', '-L', '-o', zip_loc, template_url ]
  r = subprocess.run( download_cmd )
  print( "# Download vPSIJ template: Success!" )
  
  # print( f"{ '#' * 10 } Unzip repository zip file and move sche_template directory to the vPSIJ_util dirctory { '#' * 10 }" )
  print( f"{ '#' * 10 } Unzip repository zip file { '#' * 10 }" )
  with zipfile.ZipFile( zip_loc, 'r' ) as zipf:
    zipf.extractall( util_dir )
  print( "# Unzip vpsij-template.zip: Success!")

  print( f"{ '#' * 10 } Checking template directory { '#' * 10 }" )
  # Check template directory exist
  if Path( template_dir ).is_dir():
    print( "# Scheduler template directory exist!")
    # local_sche_list = [ d.name for d in Path( template_dir ).iterdir() if d.is_dir() ]
  elif Path( template_dir ).exists():
    print( "# Scheduler template directory path exist but not directory!!")
    print( ">> Removing!!")
    shutil.rmtree( template_dir )
    print( "# Removing: Sucess!")
  else:
    print( "# Scheduler template does not exist!")

  # List scheduler from the repository
  repo_sche_list = [ d.name for d in Path( f'{ util_dir }/vPSIJ_scheduler_template-main/sche_template' ).iterdir() if d.is_dir() ]
  # Check existing each template directory
  for sche_temp in repo_sche_list:
    if Path( f"{ template_dir }/{ sche_temp }" ).is_dir():
      print( f"# { sche_temp } template will be replace in vPSIJ_util/sche_template directory!" )
      shutil.rmtree( f"{ template_dir }/{ sche_temp }" )
    else:
      print( f"# { sche_temp } template will be add to vPSIJ_util/sche_template directory!" )

  print( f"{ '#' * 10 } Copy template directory to vPSIJ_util { '#' * 10 }" )
  shutil.copytree( f'{ util_dir }/vPSIJ_scheduler_template-main/sche_template', template_dir, dirs_exist_ok = True )
  print( "# Copy template directory: Success!")

  print( f"{ '#' * 10 } Check template_location.json in vPSIJ_util { '#' * 10 }" )
  templatefile_exist = Path( f'{ util_dir }/template_location.json' ).is_file()
  if templatefile_exist: 
    print( f"# Found template_location.json")
    print( f"{ '#' * 10 } Editing template_location.json in vPSIJ_util { '#' * 10 }" )
    template_list = { d.name: str( d ) for d in Path( template_dir ).iterdir() if d.is_dir() }
    with open( f'{ util_dir }/template_location.json', 'r' ) as in_f:
      json_sche_list = json.load( in_f )
    for sche in template_list:
      json_sche_list[ sche ] = template_list[ sche ]
    with open( f'{ util_dir }/template_location.json', 'w' ) as out_f:
      json.dump( json_sche_list, out_f )
    print( "# Success!")
  else:
    print( "# {HOME}/vPSIJ_util/template_location.json: Not found!")
    print( f"{ '#' * 10 } Generating template_location.json in vPSIJ_util { '#' * 10 }" )
    template_list = { d.name: str( d ) for d in Path( template_dir ).iterdir() if d.is_dir() }
    with open( f'{ util_dir }/template_location.json', 'w' ) as out_f:
      json.dump( template_list, out_f )
    print( "# Generating template_location.json: Success!")
  
  print( f"{ '#' * 10 } Clean up { '#' * 10 }" )
  shutil.rmtree( f'{ util_dir }/vPSIJ_scheduler_template-main' )
  os.remove( zip_loc )
  print( "# Clean up: Success!")

  print( "# Script run successful!")

if __name__ == '__main__':
  setup()