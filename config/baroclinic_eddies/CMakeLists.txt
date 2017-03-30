cmake_minimum_required(VERSION 2.8)

# get MOM6 exe
set(MOM6_EXE $<TARGET_FILE:MOM6>)
# set cache variables
set(NPROC_BAROCLINIC_EDDIES 6 CACHE STRING "Number of processors for baroclinic eddies runs")

# add empty custom target for this experiment
# which doesn't run at build time
add_custom_target(baroclinic_eddies)

# configure MOM_input for this experiment
configure_file(MOM_input.in "${CMAKE_CURRENT_SOURCE_DIR}/MOM_input")

# viscosity parameters
set(PARAMS_KH 1 5 10 20 200)
set(PARAMS_DX 1 4 10)

# loop over parameter space
foreach(PARAM_DX IN LISTS PARAMS_DX)
foreach(PARAM_KH IN LISTS PARAMS_KH)
foreach(PARAM_AD IN ITEMS PPM PPM:H3)
foreach(PARAM_CO IN ITEMS Z* RHO)

# sanitise colon in parameter value
string(REPLACE ":" "" PARAM_AD_CLEAN "${PARAM_AD}")
string(REPLACE "*" "" PARAM_CO_CLEAN "${PARAM_CO}")

set(EXPT "DX${PARAM_DX}_KH${PARAM_KH}_AD${PARAM_AD_CLEAN}_CO${PARAM_CO_CLEAN}")
set(EXPT_DIR "${CMAKE_CURRENT_BINARY_DIR}/${EXPT}")

# create experiment directory
file(MAKE_DIRECTORY ${EXPT_DIR})
# generate input.nml
configure_file(input.nml.in "${EXPT_DIR}/input.nml")
# copy diag_table
file(COPY diag_table DESTINATION "${EXPT_DIR}")

# generate param file
unset(OVERRIDE_DT)
if(PARAM_DX EQUAL 1)
  # override DT for high resolution experiments
  set(OVERRIDE_DT "#override DT = 300.0")
elseif(PARAM_DX EQUAL 10 AND PARAM_CO STREQUAL RHO)
  # override DT for low res rho experiments
  set(OVERRIDE_DT "#override DT = 1200.0")
endif(PARAM_DX EQUAL 1)

# calculate number of points
math(EXPR NIGLOBAL "160 / ${PARAM_DX}")
math(EXPR NJGLOBAL "500 / ${PARAM_DX}")
configure_file(MOM_override_${PARAM_CO_CLEAN}.in "${EXPT_DIR}/MOM_override")

# use twice as many processors for DX1 cases
set(NPROC ${NPROC_BAROCLINIC_EDDIES})
if(PARAM_DX EQUAL 1)
math(EXPR NPROC "${NPROC} * 16")
elseif(PARAM_DX EQUAL 4)
math(EXPR NPROC "${NPROC} * 4")
endif()

# specify how to generate output file
add_custom_target("baroclinic_eddies_${EXPT}"
	COMMAND ${MPI_CMD} -n ${NPROC} ${MOM6_EXE} > mom6.out 2> mom6.err
	WORKING_DIRECTORY "${EXPT_DIR}"
	DEPENDS MOM6)

# add target to list
list(APPEND EXPTS_${PARAM_DX} "baroclinic_eddies_${EXPT}")
endforeach()
endforeach()
endforeach()

# create a custom for each horizontal resolution, for practicality
add_custom_target(baroclinic_eddies_${PARAM_DX} DEPENDS ${EXPTS_${PARAM_DX}})
add_dependencies(baroclinic_eddies baroclinic_eddies_${PARAM_DX})
endforeach()
