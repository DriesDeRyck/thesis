# Master thesis
## How to use DML_parallel.py?
Required arguments:
- **microbes**:     path to microbe (.tsv) file (rows = microbes, columns = samples)
- **metabolites**:  path to metabolite (.tsv) file (rows = metabolites, columns = samples)
- **results**:      path to results directory (must not exist)
- **config**:       path to config (.ini) file

An example might look like this:
```
python3 DML_parallel.py microbes.tsv metabolites.tsv ./results settings.ini
```
The **results** directory must not exist, it will be created. In this directory the 
results will be saved. The **config** file will also be copied and saved in the **results** directory.

### Config file
The config file must follow the .ini format.\
It has one required section: `[general]`.\
The `[general]` section has 2 required keys:
- `seed` must be an integer
- `learner` must be one of the following options:
  - `lr` for a linear regression learner
  - `rf` for a random forest learner
  - `boost` for a gradient boost regressor learner

Parameters for the learner can be specified in an optional section named `[lr]`, `[rf]` or `[boost]`

Values for the seed and learner parameters will be automatically converted from string to int if possible.

Example of the .ini file:
```ini
;always specify seed and learner
[general]
seed = 4131
;learner can be 'lr', 'rf', or 'boost'
learner = rf

;only the selected learner settings will be used, other learner settings will be ignored
;if parameters are not included, default values are used
[rf]
n_estimators = 50
max_depth = 10
max_features = sqrt

[boost]
n_iter_no_change = 10
```