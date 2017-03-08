cmake_minimum_required(VERSION 2.8)

# top-level doesn't need any language definitions
project(spurious NONE)

# MOM6 ocean_only build
add_subdirectory(build)

# lock exchange experiments
add_subdirectory(config/lock_exchange run/lock_exchange)
