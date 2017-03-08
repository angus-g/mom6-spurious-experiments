cmake_minimum_required(VERSION 2.8)

# get MOM6 exe
set(MOM6_EXE $<TARGET_FILE:MOM6>)

# configure MOM_input for this experiment
configure_file(MOM_input.in "${CMAKE_CURRENT_SOURCE_DIR}/MOM_input")

# viscosity parameters
set(PARAMS_KH 0.01 0.1 1 10 100 200)

# loop over parameter space
foreach(PARAM_KH IN LISTS PARAMS_KH)
foreach(PARAM_AD IN ITEMS PPM PPM:H3)

# sanitise colon in parameter value
string(REPLACE ":" "" PARAM_AD_CLEAN "${PARAM_AD}")

set(EXPT_DIR "${CMAKE_CURRENT_BINARY_DIR}/KH${PARAM_KH}_AD${PARAM_AD_CLEAN}")

# create experiment directory
file(MAKE_DIRECTORY ${EXPT_DIR})
# generate input.nml
configure_file(input.nml.in "${EXPT_DIR}/input.nml")
# copy diag_table
file(COPY diag_table DESTINATION "${EXPT_DIR}")
# generate param file
configure_file(MOM_override.in "${EXPT_DIR}/MOM_override")

set(OUT_FILE "${EXPT_DIR}/prog.nc")

# specify how to generate output file
add_custom_command(OUTPUT "${OUT_FILE}"
	COMMAND mpirun -n ${NPROC} ${MOM6_EXE} > mom6.out 2> mom6.err
	WORKING_DIRECTORY "${EXPT_DIR}"
	DEPENDS MOM6)

# add target to list
list(APPEND EXPT_RESULTS ${OUT_FILE})
endforeach()
endforeach()

add_custom_target(lock_exchange DEPENDS ${EXPT_RESULTS})
# don't run the experiments by default
set_target_properties(lock_exchange PROPERTIES EXCLUDE_FROM_ALL true)
