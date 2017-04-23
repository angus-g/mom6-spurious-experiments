cmake_minimum_required(VERSION 2.8)

# top-level doesn't need any language definitions
project(spurious NONE)
include(lib.cmake)

# MOM6 ocean_only build
add_subdirectory(build EXCLUDE_FROM_ALL)

add_custom_target(Executables ALL)
add_dependencies(Executables MOM6)

# set cache variables
set(MPI_CMD aprun -j1 CACHE STRING "Command line for MPI execution")
set(RUN_PATH run CACHE PATH "Run directory for experiments")

# experiments
add_experiment(lock_exchange)
add_experiment(internal_waves)
add_experiment(baroclinic_eddies)
