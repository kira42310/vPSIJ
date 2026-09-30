from typing import Optional
from threading import Condition
from uuid import uuid4
from pathlib import Path
from os import getcwd

import importlib.util
import importlib.machinery
import json
import sys

from .job_spec import job_spec
# from job_status import job_status

class Job:
  
  def __init__( self, scheduler, spec: Optional[ job_spec ] = None, work_directory: Optional[ Path ] = None, custom_sche_template_dir: Optional[ Path ] = None ):
    
    self.id = str( uuid4() )
    self.scheduler = scheduler
    self.spec = spec
    if work_directory:
      self.work_directory = work_directory
    else:
      self.work_directory = Path( getcwd() )
    self.native_id = None
    self.submit_cmd = None
    self.status_cmd = None
    self.cancel_cmd = None
    self.script_name = f"{ self.scheduler }_{ self.id }.sh"
    self.script = None
    sche_template_dir = self._get_sche_template_dir( self.scheduler )
    if sche_template_dir is None: sche_template_dir = custom_sche_template_dir
    self.sche = self.load_module_from_path( self.scheduler, sche_template_dir )
    self.get_cmd()
    
    # self._status = job_status.new
    # self._callback = None # for calling the workflow process Optional
    # self._cv = Condition()

  # Get the submit, cancel, and status query command from the template repository
  def get_cmd( self ):
    self.submit_cmd = self.sche.get_submit_cmd()
    self.status_cmd = self.sche.get_status_cmd()
    self.cancel_cmd = self.sche.get_cancel_cmd()

  def generate_template( self, grpc_server = 'localhost:50051', secure_channel = 0 ):
    tmp = self.spec.__dict__
    tmp[ 'grpc_server' ] = grpc_server
    tmp[ 'secure_channel' ] = secure_channel
    self.script = self.sche.generate_script( tmp )

  def output_script( self, output_dir: Optional[ Path ] = None ):
    if output_dir is None:
      _output_file = self.work_directory / self.script_name
    else:
      _output_file = output_dir / self.script_name
    with open( _output_file, 'w' ) as f:
      f.write( self.script )

  def load_module_from_path( self, module_name, module_path: Path):
    spec = importlib.util.spec_from_file_location( module_name, module_path / f'{ module_name }.py' )
    module = importlib.util.module_from_spec( spec )
    sys.modules[ module_name ] = module
    spec.loader.exec_module( module )
    return module

  def _get_sche_template_dir( self, scheduler_name ):
    template_info_file = Path.home() / 'vPSIJ_util/template_location.json'
    with open( template_info_file, 'r' ) as f:
      template_info = json.load( f )
    if scheduler_name in template_info.keys():
      return Path( template_info[ scheduler_name ] )
    else:
      return None

  def check_and_get_native_id_from_submit( self, response ):
    if self.sche.is_submitted( response ):
      self.native_id = self.sche.get_job_id_from_submit( response )
      return True
    else:
      return False
  # @property
  # def status( self ) -> job_status:
  #   return self._status

  # @status.setter
  # def status( self, state: job_status ) -> None:
  #   with self._cv:
  #     current = self.status
  #     new_state = state
  #     if current >= new_state:
  #       return
  #     self._status = new_state
  #     self._cv.notify_all()
    
  #   if self._callback:
  #     pass

  # def submit():
  #   #
  #   # This fucntion is for the local job scheduler, remote function will be implement later
  #   #
  #   # load job scheduler command from template repo
  #   # check job_spec
  #   # change the job_spec variables to the specification if need
  #   # convert job_spec object to jinja2 context(dict)
  #   # generate script
  #   # call submit command
  #   # get submit status from job scheduler
  #   # update the job status
  #   # 
  #   pass
  
  # def cancel():
  #   #
  #   # This fucntion is for the local job scheduler, remote function will be implement later
  #   #
  #   pass
