# vPSIJ
Job scheduler interface through Python-based library

### How to submit job at local cluster

```py
import vPSIJ import Job, job_spec, Executor

# Create Job object and supply with job scheduler name for this job
job = Job( 'scheduler temaplte name' )

# Declare as argument
spec = job_spec( 
  # Will list the argument below
)

# Can change value after create job_spec object
spec.paramerters_name = 'change value'

# Bind job spce with job
job.spec = spec

# Create Executor object with job
ex = Executor( job )

# Call submission
ex.submit(
  # Arguments will list below
)

# User can call wait for the job to finished
res = ex.wait( )

print( res )
```

### How to submit job to remote cluster
```py
import vPSIJ import Job, job_spec, Executor

# Create Job object and supply with job scheduler name for this job
job = Job( 'scheduler temaplte name' )

# Declare as argument
spec = job_spec( 
  # Will list the argument below
)

# Can change value after create job_spec object
spec.paramerters_name = 'change value'

# Bind job spce with job
job.spec = spec

# Create Executor object with job
ex = Executor( job )

# Call remote submission
ex.remote_submit(
  # Arguments will list below
)

# User can call wait for the job to finished
res = ex.wait( )

print( res )
```

### Job spec arguments

| Argument name | Type | Default | Description |
| --- | --- | --- | --- |
| name | str | None | Name of the job |
| directory | str, pathlib.Path | None | To-do |
| environments | dict[ str: str ] | None | To-do |
| executable | str | None | The main executatble or command |
| arguments | list[ str ] | None | The argument for the executable |
| pre_execution | list[ str ] | None | The list of command that will execute before the main executable |
| post_execution | list[ str ] | None | |
| stdin_path | str, pathlib.Path | None | |
| stdout_path | str, pathlib.Path | None | |
| stderr_path | str, pathlib.Path | None | |
| queue_name | str | None | |
| duration | str, datetime.timedelta | None | |
| node_count | int | None | |
| process_count | int | None | |
| process_per_node | int | None | |
| cpu_cores_per_process | int | None | |
| memory | str | None | |
| execlusive_node_use | bool | False | |
| billing_account | str | None | |
| reservation_id | str | None | |
| custom_key_value | dict[ str: str ] | None | |
| custom_value | list[ str ] | None | |
| cleanup_flag | bool | False | |

### submit function arguments

| Argument name | Type | Default | Description |
| --- | --- | --- | ---|
| secure_channel | bool | False | |
| mode | 'local', 'remote' | 'local' | |
| callback_address | 'hostname', 'ip', 'custom' | 'hostname' | | 
| custom_callback_address | str | None | |
| custom_callback_port | str | None | |
| updater_ssh_user_address | str | None | |

### remote_submit function arguments

| Argument name | Type | Default | Description |
| --- | --- | --- | ---|
| host | str | <span style="color:red">mandatory</span> | | 
| username | str | None | | 
| port | str | None | |
| pkey_loc | str, pathlib.Path | None | | 
| data | str, pathlib.Path | None | <span style="color:red">****</span>Not implement yet | 
| allow_agent | bool | True | |
| identity_auth | bool | True | | 
| ssh_timeout | int, float | None | |
| secure_channel | bool | False | |
| mode | 'local', 'remote' | 'local' | |
| callback_address | 'hostname', 'ip', 'custom' | 'hostname' | | 
| custom_callback_address | str | None | |
| custom_callback_port | str | None | |
| updater_ssh_user_address | str | None | |

### More detail later...