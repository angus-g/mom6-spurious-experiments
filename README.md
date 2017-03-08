# MOM6 Spurious Experiments

This project sets up and runs a suite of idealised experiments for evaluating spurious mixing in MOM6. This occurs in two phases:

- the *build* phase is intended to be run from a head node, and is responsible for building libFMS.a and MOM6, as well as setting up the directory structure for experiments
- the *run* phase is intended to be run from a batch node, and actually runs the model for each experiment

## Directory Structure
The top-level `CMakeLists.txt` drives the building of the model, and collects all experiments for setting up their directory structure at generation time.

Within an experiment, for each parameter combination we can generate an input file (`MOM_override`), and copy files that must be in the experiment directory (`diag_table` and `input.nml`). We then add a CMake *target*, which is added to the global list of targets so that we can run all experiments from the top-level: e.g. `make lock_exchange`.