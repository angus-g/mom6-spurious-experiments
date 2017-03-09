macro(add_experiment EXPT_NAME)
add_subdirectory("config/${EXPT_NAME}" "run/${EXPT_NAME}")
endmacro()
