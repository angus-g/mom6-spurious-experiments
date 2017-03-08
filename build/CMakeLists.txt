# require 3.7 because it can do the right compiler checks for Cray
cmake_minimum_required(VERSION 3.6)
project(MOM6 C Fortran)

# put cray libraries in our search path
string(REPLACE ":" ";" CMAKE_LIBRARY_PATH "$ENV{CRAY_LD_LIBRARY_PATH}")
# look for netcdf
find_library(NETCDF netcdf)

# abort if netcdf not found
if(NETCDF STREQUAL NETCDF-NOTFOUND)
message(FATAL_ERROR "NetCDF library not found!")
endif()

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
