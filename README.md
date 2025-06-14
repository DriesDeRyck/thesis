# Master's Thesis: Double Machine Learning to Uncover Causal Microbe-Metabolite Relationships

## Structure of this repository
This repository is structured as follows:
- `src`: this directory holds the python files containing the main functionality
- `sim_new`: directory including notebooks and files related to the simulated dataset
  - `data`: simulation data
  - `figures`: figures related to the simulation data
  - `results`: results of the models trained on the simulation data
    - `CF_sims`: results of the methods tested by Morton et al.
    - `DML`: results of the DML models
  - `scripts`: scripts used to run the models on the VSC
    - `out`: output of running the models
  - Several notebooks used for preparing the simulation data and processing the results
- `soil`: directory including notebooks and files related to the soil dataset
  - `data`: soil data
  - `figures`: figures related to the soil data
  - `results`: results of the models trained on the soil data
  - `scripts`: scripts used to run the models on the VSC
    - `out`: output of running the models
  - Several notebooks used for preparing the soil data and processing the results
- `figures`: this directory contains additional figures that were created for the thesis.
- `settings`: the settings files that were used to specify the model parameters

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

## Evaluation
Evaluating the ranks and creating the visualization is done in the 
`evaluate-biocrust.ipynb` and `evaluate-sim.ipynb` files in the respective 
subdirectories `soil/`and `sim_new/`.