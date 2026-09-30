from concurrent import futures
from threading import Condition
from typing import Literal, Optional
from datetime import timedelta, datetime
from pathlib import Path
from pssh.clients import SSHClient
from gevent import joinall

# import os
import grpc
import updater_pb2
import updater_pb2_grpc
import socket
import subprocess
import shutil
import tarfile

from job import Job
from job_status import status

LARGE_TIMEOUT = timedelta( weeks = 12 )
rpc_client_loc = './dist/job_rpc_client'
default_base_dir = '~/vPSIJ'

class Executor:

  def __init__(self, job: Job):
    self.job = job
    self._cv = Condition()
    self._callback = None
    self._server = grpc.server( futures.ThreadPoolExecutor( max_workers = 1 ) )
    self._state = status.new
    updater_pb2_grpc.add_UpdateServiceServicer_to_server( self.executor_servicer( self ), self._server )

  def submit( self, 
      secure_channel = False, 
      mode: Literal[ 'local', 'remote' ] = 'local', 
      callback_address: Literal[ 'hostname', 'ip', 'custom' ] = 'hostname', 
      custom_callback_address: Optional[ str ] = None,
      custom_callback_port: Optional[ str ] = None 
      ):

    # Set status to submiiting
    self.status = status.submitting

    # Formatting the host and port for start a gRPC server and information for call back to update the status
    host_port = self.format_host_port( callback_address = callback_address, custom_callback_address = custom_callback_address, custom_callback_port = custom_callback_port )

    # Make directory at local site
    if self.job.work_directory is None:
      _working_dir = f'{ default_base_dir }/{ self.job.id }'
    else:
      _working_dir = self.job.work_directory + f'/{ self.job.id }'
    Path( _working_dir ).mkdir( parents = True, exist_ok = True )

    # Generate job scheduler script
    self.job.generate_template( f'{host_port[0]}:{host_port[1]}' , int( secure_channel ) )
    self.job.output_script( output_dir = _working_dir )

    # Start gRPC server
    self.start_grpc_server( '[::]:' + str( host_port[1] ), secure_channel )

    # Submit job
    execute_cmd = self.job.submit_cmd + [ f"{ _working_dir }/{ self.job.script_name }" ]
    response = subprocess.run( execute_cmd, capture_output = True, text = True )
    if self.job.check_and_get_native_id_from_submit( response.stdout ):
      self.status = status.queuing
    else:
      self.status = status.failed
      raise Exception( response )

  def remote_submit( self, 
      host, 
      username = None, 
      port = None, 
      pkey_loc = None, 
      data = None, 
      allow_agent = True, 
      identity_auth = True, 
      ssh_timeout = None,
      secure_channel = False,
      remote_working_dir: Optional[ str ] = None,
      callback_address: Literal[ 'hostname', 'ip', 'custom' ] = 'hostname', 
      custom_callback_address: Optional[ str ] = None,
      custom_callback_port: Optional[ str ] = None
    ):
    # arguments: host, port, username, pkey_loc, data, allow_agent, identity_auth, ssh_timeout
    # prepare parameters
    # start gRPC server
    # create directory for zip/tar
    # (notyet) copy data in the ./data directory
    # (notyet) zip/tar the directory (create new fn)
    # generate script
    # with ssh
    #   create directory with job.id
    #   transfer file to the vPSIJ or remote work directory
    #   unzip
    #   submit 
    #   check submit result
    #   

    # Set status to submiiting
    self.status = status.submitting

    # Formatting the host and port for start a gRPC server and information for call back to update the status
    host_port = self.format_host_port( callback_address = callback_address, custom_callback_address = custom_callback_address, custom_callback_port = custom_callback_port )

    # Make directory at local site
    if self.job.work_directory is None:
      _working_dir = f'{ default_base_dir }/{ self.job.id }'
    else:
      _working_dir = self.job.work_directory + f'/vPSIJ/{ self.job.id }'
    Path( _working_dir ).mkdir( parents = True, exist_ok = True )

    # Make directory at the server side in the ~/.vPSIJ/uuid
    if remote_working_dir is None:
      # _remote_dir_base = f'~/vPSIJ/{self.job.id}'
      _remote_dir_base = f'~/vPSIJ/'
    else:
      # _remote_dir_base = remote_working_dir + f'/vPSIJ/{self.job.id}'
      _remote_dir_base = remote_working_dir + f'/vPSIJ/'

    # Generate job scheduler script
    self.job.generate_template( f'{host_port[0]}:{host_port[1]}' , int( secure_channel ) )
    self.job.output_script( output_dir = _working_dir )

    # Start gRPC server
    self.start_grpc_server( '[::]:' + str( host_port[1] ), secure_channel )

    # Create submit command at remote
    submit_cmd = f'{ ' '.join( self.job.submit_cmd ) } { _remote_dir_base }/{ self.job.script_name }' 

    # Start remote submission
    with SSHClient( host = host, port = port, user = username, pkey = pkey_loc, allow_agent = allow_agent, identity_auth = identity_auth, ssh_timeout = ssh_timeout  ) as client:
      # Create directory at remote site
      mkdir_out = client.run_command( f'mkdir -p { _remote_dir_base }' )
      client.wait_finished( mkdir_out, timeout = 300 )
      if mkdir_out.exit_code != 0:
        raise Exception( mkdir_out.stderr )

      # Transfer file to remote site
      client.copy_file( _working_dir, _remote_dir_base )
      # client.copy_file( self.job.work_directory / self.job.script_name, f'{ _remote_dir_base }/{self.job.script_name}' )
      # client.copy_file( rpc_client_loc, f'{ _remote_dir_base }/job_rpc_client' )

      # Submit job
      cmd_out = client.run_command( submit_cmd )
      client.wait_finished( cmd_out, timeout = 300 )
      if cmd_out.exit_code != 0:
        raise Exception( next( cmd_out.stderr ) )
      # response = subprocess.run( execute_cmd, capture_output = True, text = True )
      # response = next( cmd_out.stdout )
      if self.job.check_and_get_native_id_from_submit( next( cmd_out.stdout ) ):
        self.status = status.queuing
      else:
        self.status = status.failed
        raise Exception( cmd_out.stderr )

  def wait( self, timeout: Optional[ timedelta ] = None, target_state: Optional[ status ] = None ):
    start = datetime.now()
    if not timeout:
      timeout = LARGE_TIMEOUT
    end = start + timeout

    while True:
      with self._cv:
        status = self.status

        if status.value >= status.completed.value:
          self.stop_grpc_server()
          return status
        else:
          pass

        left = end - datetime.now()
        left_seconds = left.total_seconds()
        if left_seconds <= 0:
          self.stop_grpc_server()
          return None
        self._cv.wait( left_seconds )


  def cancel():
    pass

  def start_grpc_server( self, server_port: str, secure: bool = False ):
    if secure:
      self._server.add_secure_port( server_port )
    else:
      self._server.add_insecure_port( server_port )

    try:
      self._server.start()
    except KeyboardInterrupt:
      self.stop_grpc_server()
    except:
      self.stop_grpc_server()
    
  def stop_grpc_server( self, delay = 5 ):
    self._server.stop( grace = delay )

  @property
  def state( self ):
    return self._state

  @state.setter
  def status( self, state ):
    with self._cv:
      crt_status = self._state
      new_status = status( state )
      if crt_status == new_status or crt_status.value > new_status.value:
        return
      self._state = new_status
      self._cv.notify_all()

  def _get_hostname_port( self ):
    hostname = socket.gethostname()
    port = self.get_port( address = hostname )
    return ( hostname, port )

  def _get_ip_port( self ):
    ip = socket.gethostbyname( socket.gethostname() )
    port = self.get_port( address = ip )
    return ( ip, port )

  def _get_port( self, address = 'localhost' ):
    with socket.socket( socket.AF_INET, socket.SOCK_STREAM ) as sock:
      sock.bind( ( address, 0 ) )
      port = sock.getsockname()[1]
    return port

  def format_host_port( self,
      callback_address: Literal[ 'hostnmae', 'ip', 'custom' ] = 'hostname',
      custom_callback_address: Optional[ str ] = None,
      custom_callback_port: Optional[ str ] = None
    ):
    if callback_address == 'hostname':
      host_port = self._get_hostname_port()
    elif callback_address == 'ip':
      host_port = self._get_ip_port()
    elif callback_address == 'custom':
      if custom_callback_address == None:
        host = socket.gethostname()
      else:
        host = custom_callback_address
      if custom_callback_port == None:
        port = self._get_port( address = host )
      else:
        port = custom_callback_port
      host_port = ( host, port )
    else:
      raise Exception( "Please select the callback address by 'hostname' or 'ip' or 'custom' and provide hostname or ip address you want to use")
    return host_port

  # def initialize_remote( self, host_ip_port, username, public_key, remote_directory = 'vPSIJ/' ):
    # argument: nuPSIJ directory
    # return list of mkdir command
    # with ssh
    #   reate vPSIJ directory
    #   copy grpc client to the vPSIJ/gRPC_client
    # with SSHClient( host = host_ip_port, user = username, pkey = public_key ) as client:
    #   mkdir_out = client.run_command( f"mkdir -p { remote_directory }rpc_client/" )
    #   client.wait_finished( mkdir_out, timeout = 300 )
    #   if mkdir_out.exit_code != 0:
    #     raise Exception( mkdir_out.stderr )
    #   cp_cmd = client.copy_file( rpc_client_loc, f'{ remote_directory }rpc_client/job_rpc_client' )
    #   joinall( cp_cmd, raise_error = True )
    # return [ f"mkdir -p { remote_directory }", ]

  # def reinitialize_remote():
    # arguments: host_ip_port, username, ssh_key
    # wtih ssh
    #   remove the vPSIJ directory
    #   call initialize_rermote function
    # pass

  class updater_servicer( updater_pb2_grpc.UpdateServiceServicer ):

    def __init__( self, ex ):
      self.ex = ex

    def UpdateStatus(self, request, context):
      self.ex.status = status( int( request.state ) )
      return updater_pb2.UpdateResponse( result = 'S' )

# def serve( job ):

  # server = grpc.server( futures.ThreadPoolExecutor( max_workers = 1 ) )
  # test_pb2_grpc.add_UpdateServiceServicer_to_server( executor_servicer( job ), server )
  # test_pb2_grpc.add_UpdateServiceServicer_to_server( executor_servicer(), server )
  # with socket.socket( socket.AF_INET, socket.SOCK_STREAM ) as sock:
  #   sock.bind( ( 'localhost', 0 ) )
  #   port = sock.getsockname()[1]
  # server_port = '[::]:'+port
  # server.add_insecure_port( server_port )
  # print( f'{server_port}' )
  # server.start()

  # server.stop( grace = 10 )
  # server.wait_for_termination()