cmake_minimum_required(VERSION 2.8)

# top-level doesn't need any language definitions
project(spurious NONE)

# MOM6 ocean_only build
add_subdirectory(build)

# set cache variables
set(MPI_CMD aprun -j1 CACHE STRING "Command line for MPI execution")

# experiments
add_subdirectory(config/lock_exchange run/lock_exchange)
add_subdirectory(config/internal_waves run/internal_waves)
