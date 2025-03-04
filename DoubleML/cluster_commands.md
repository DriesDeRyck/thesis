# Cluster Commands

## Connecting

To connect to the cluster: `ssh calcua` and provide password. \
Change config file for other options, like which cluster to connect to.

## Move to other file system

```
cd $VSC_DATA
```

## Module Management

To list all loaded modules:

```
module list
```

To load a module:

```
module load calcua/2024a
```

To unload all modules:

```
module purge
```

## Globus

In the GlobusConnectPersonal directory, open globus installation folder, then:

```
./globusconnectpersonal
```

## Slurm Commands

Submit a script:

```
sbatch <sbatch arguments> jobscript <jobscript arguments>
```

Check status of your own jobs:

``` 
squeue
```

ST (Status) abbreviations:

- PD: Pending – waiting for resources
- F: Failed job – non-zero exit code
- CF: Configuring – nodes becoming ready
- TO: Timeout – wall time exceeded
- R: Running
- OOM: Job experienced out-of-memory error
- CD: Successful completion – exit code zero
- NF: Job terminated due to node failure

Cancel a job:

```
scancel <jobid>
```

Information about running jobs:
```
sstat -a -j 12345 -o JobID,MinCPU,AveCPU
```