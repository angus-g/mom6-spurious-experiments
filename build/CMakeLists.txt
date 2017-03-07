# we need at least 3.7 to generate Ninja output
# that will deal with the preprocessing to get dependencies
# correct in FMS
cmake_minimum_required(VERSION 2.8)
project(MOM6 C Fortran)

# intel compiler stuff
#include(intel-fortran.cmake)
#include(intel-c.cmake)
include(Compiler/Intel-Fortran)
include(Compiler/Intel-C)

set(CMAKE_Fortran_COMPILER ftn)
set(CMAKE_C_COMPILER cc)

set(CMAKE_Fortran_FLAGS "-fno-alias -auto -safe-cray-ptr -ftz -assume byterecl -i4 -r8 -nowarn -sox -traceback -O2 -debug minimal -fp-model source")
set(CMAKE_C_FLAGS "-sox -traceback -O2 -debug minimal")
add_definitions(-Duse_libMPI -Duse_netCDF -Duse_LARGEFILE -DSPMD -D__IFC)

# FMS static library
file(GLOB_RECURSE FMS_SOURCE LIST_DIRECTORIES false
  ../src/FMS/*.[fF]90 ../src/FMS/*.c)
add_library(FMS ${FMS_SOURCE})
target_include_directories(FMS PRIVATE
  /usr/include ../src/FMS/include ../src/FMS/mosaic ../src/FMS/drifters ../src/FMS/fms ../src/FMS/mpp/include)
set_target_properties(FMS PROPERTIES Fortran_MODULE_DIRECTORY FMS-modules)

# common files for both builds
file(GLOB_RECURSE MOM6_SOURCE LIST_DIRECTORIES false FOLLOW_SYMLINKS
  ../src/MOM6/src/*.[fF]90 ../src/MOM6/src/*.c)
# MOM6 ocean only
file(GLOB_RECURSE MOM6_SOLO_SOURCE LIST_DIRECTORIES false
  ../src/MOM6/config_src/solo_driver/*.[fF]90)
add_executable(MOM6 ${MOM6_SOURCE} ${MOM6_SOLO_SOURCE})
target_include_directories(MOM6 PRIVATE
  FMS-modules ../src/MOM6/config_src/dynamic ../src/MOM6/src/framework)
target_link_libraries(MOM6 FMS netcdff netcdf hdf5_hl hdf5 z)
# output modules in separate directory so parallel builds don't clash
# there's a race condition with MOM6 and MOM6-SIS2 otherwise
set_target_properties(MOM6 PROPERTIES Fortran_MODULE_DIRECTORY MOM6-modules)
