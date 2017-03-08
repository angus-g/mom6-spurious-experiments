cmake_minimum_required(VERSION 2.8)

# top-level doesn't need any language definitions
project(spurious NONE)

# MOM6 ocean_only build
add_subdirectory(build)

# set cache variables
set(NPROC_LOCK_EXCHANGE "4" CACHE STRING "Number of processors for lock exchange runs")
set(NPROC_INTERNAL_WAVES "4" CACHE STRING "Number of processors for internal waves runs")
set(MPI_CMD "aprun -j1" CACHE STRING "Command line for MPI execution")

# experiments
add_subdirectory(config/lock_exchange run/lock_exchange)
add_subdirectory(config/internal_waves run/internal_waves)
