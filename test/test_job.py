from job import Job
from job_spec import job_spec
from datetime import timedelta

job = Job( 'slurm' )

print( job.id )
print( job.submit_cmd )
print( job.cancel_cmd )

job_spec_test = job_spec(
  name = 'test_slurm',
  environments =  None,
  executable = 'ls',
  arguments = '-la',
  queue_name = 'small',
  node_count = 1,
  process_count = 1,
  process_per_node = 1,
  cpu_cores_per_process = 1,
	duration = timedelta( hours = 36 )
)

job.spec = job_spec_test
job.generate_template()
print( job.script )
#job.output_script()

job_pj = Job( 'pjsub' )

job_spec_test.name = 'test_pjsub'
job_spec_test.duration = timedelta( minutes = 30 )
job_spec_test.custom_key_value = {  "-x": "ABCD" }
job_spec_test.custom_value = ['-S']
job_spec_test.billing_account = 'group01'

job_pj.spec = job_spec_test
job_pj.generate_template()
print( job_pj.script )
