from job import Job
from job_spec import job_spec
from executor import Executor

job = Job( 'pjsub' )

job_spec_test = job_spec(
  name = 'test_slurm',
  environments =  None,
  executable = 'ls -la > ~/test.txt',
  # arguments = '-la',
  queue_name = 'small',
  node_count = 1,
  process_count = 1,
  process_per_node = 1,
  cpu_cores_per_process = 1,
  billing_account = 'XXX'
)

job.spec = job_spec_test

ex = Executor( job )
ex.test_remote( callback_address = 'ip' )
# res = ex.wait()
# print( res )
