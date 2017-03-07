cmake_minimum_required(VERSION 2.8)

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

endforeach()
endforeach()
