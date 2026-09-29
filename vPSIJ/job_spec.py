from typing import Optional, Union, List, Dict
from datetime import timedelta

import pathlib

class job_spec:

  def __init__( self,
      name: Optional[ str ] = None,
      directory: Optional[ Union[ str, pathlib.Path ] ] = None,
      environments: Optional[ Dict[ str, object ] ] = None,
      executable: Optional[ str ] = None,
      arguments: Optional[ List[ str ] ] = None,
      pre_execution: Optional[ List[ str ] ] = None,
      post_execution: Optional[ List[ str ] ] = None,
      stdin_path: Optional[ Union[ str, pathlib.Path ] ] = None,
      stdout_path: Optional[ Union[ str, pathlib.Path ] ] = None,
      stderr_path: Optional[ Union[ str, pathlib.Path ] ] = None,
      queue_name: Optional[ str ] = None,
      duration: Optional[ Union[ str, timedelta ] ] = None,
      node_count: Optional[ int ] = None,
      process_count: Optional[ int ] = None,
      process_per_node: Optional[ int ] = None,
      cpu_cores_per_process: Optional[ int ] = None,
      memory: Optional[ str ] = None,
      exclusive_node_use: bool = False,
      billing_account: Optional[ str ] = None,
      reservation_id: Optional[ str ] = None,
      custom_key_value: Optional[ Dict[ str, str ] ] = None,
      custom_value: Optional[ List[ str ] ] = None,
      cleanup_flag = None ):

    self.name = name
    self.directory = directory
    self.environments = environments
    self.executable = executable
    self.arguments = arguments
    self.pre_execution = pre_execution
    self.post_execution = post_execution
    self.stdin_path = stdin_path
    self.stdout_path = stdout_path
    self.stderr_path = stderr_path
    self.queue_name = queue_name
    self.duration = duration
    self.node_count = node_count
    self.process_count = process_count
    self.process_per_node = process_per_node
    self.cpu_cores_per_process = cpu_cores_per_process
    self.memory = memory
    self.exclusive_node_use = exclusive_node_use
    self.billing_account = billing_account
    self.reservation_id = reservation_id
    self.custom_key_value = custom_key_value
    self.custom_value = custom_value
    self.cleanup_flag = cleanup_flag
