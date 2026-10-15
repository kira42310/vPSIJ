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
| directory | str, pathlib.Path | None | Path for job's working directory to the job scheduler (not vPSIJ working directory) |
| environments | dict[ str: str ] | None | Dict of key-value to load the environment on the job script  |
| executable | str | None | The main executatble or command |
| arguments | list[ str ] | None | The argument for the main executable |
| pre_execution | list[ str ] | None | The list of command that will execute before the main executable |
| post_execution | list[ str ] | None | The list of command that will execute after the main executable |
| stdin_path | str, pathlib.Path | None | Path of STDIN (In progress)  |
| stdout_path | str, pathlib.Path | None | Path of STDOUT (In progress) |
| stderr_path | str, pathlib.Path | None | Path of STDERR (IN Progress) |
| queue_name | str | None | Name of the partition or queue |
| duration | str, datetime.timedelta | None | Duration of the job execution  |
| node_count | int | None | Number of nodes allocation |
| process_count | int | None | Number of processes allocation |
| process_per_node | int | None | Number of processes per node allocation |
| cpu_cores_per_process | int | None | Number of CPU cores per process allocation |
| memory | str | None | Memory allocation for the job |
| execlusive_node_use | bool | False | Enable execlusive node allocation flag |
| billing_account | str | None | Account name or group name for accounting propose |
| reservation_id | str | None | Reservation ID |
| custom_key_value | dict[ str: str ] | None | Dict of key-value to use as declare flags with argument to job scheduler |
| custom_value | list[ str ] | None | List of str to use as declare flags to job scheduler |
| cleanup_flag | bool | False | Enable for clean up the vPSIJ file after the job finished |

### Job auguments

| Argument name | Type | Default | Description |
| --- | --- | --- | --- |
| scheduler | str | <span style="color:red">Mandatory</span> | Scheduler name  |
| spec | vPSIJ.job_spec | None | Job specification |
| work_directory | pathlib.Path | None | Path to vPSIJ working dirctory |

### Executor auguments

| Argument name | Type | Default | Description |
| --- | --- | --- | --- |
| job | vPSIJ.Job | <span style="color:red">Mandatory</span> | Initialize the Executor with a Job |

### submit function arguments

| Argument name | Type | Default | Description |
| --- | --- | --- | ---|
| secure_channel | bool | False | Enable gRPC secure channel |
| callback_address | 'hostname', 'ip', 'custom' | 'hostname' | The connection address for update the job status as hostname or ip, if the hostname cannot resolve, hostname and ip will translate to hostname or ip of the initialize machine. custom will handle the user select hostname/ip address to the initialize machine | 
| custom_callback_address | str | None | Address argument when use custom in callback_address |
| custom_callback_port | str | None | Port argument when use custom in callback_address (If no dedicate port, do not use this parameter the Executor will automatically find the available port) |
| updater_ssh_user_address | str | None | user@address to update job status through SSH and in case of the job cannot execute '~/vPSIJ_util/grpc/vpsij-updater' |

### remote_submit function arguments

| Argument name | Type | Default | Description |
| --- | --- | --- | ---|
| host | str | <span style="color:red">Mandatory</span> | Address to the remote cluster | 
| username | str | None | Username to the remote cluster | 
| port | str | None | If the remote cluster does not use default port number |
| pkey_loc | str, pathlib.Path | None | Path to private key for authentication | 
| data | str, pathlib.Path | None | <span style="color:red">****</span>Not implement yet | 
| allow_agent | bool | True | Enable agent for SSH |
| identity_auth | bool | True | Enable identity authentication | 
| ssh_timeout | int, float | None | SSH connection timeout |
| secure_channel | bool | False | Enable gRPC secure channel |
| callback_address | 'hostname', 'ip', 'custom' | 'hostname' | The connection address for update the job status as hostname or ip, if the hostname cannot resolve, hostname and ip will translate to hostname or ip of the initialize machine. custom will handle the user select hostname/ip address to the initialize machine | 
| custom_callback_address | str | None | Address argument when use custom in callback_address |
| custom_callback_port | str | None | Port argument when use custom in callback_address (If no dedicate port, do not use this parameter the Executor will automatically find the available port) |
| updater_ssh_user_address | str | None | user@address to update job status through SSH and in case of the job cannot execute '~/vPSIJ_util/grpc/vpsij-updater' |

### More detail later...