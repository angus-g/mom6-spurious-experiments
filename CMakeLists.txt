cmake_minimum_required(VERSION 2.8)
# top-level doesn't need any language definitions
project(spurious NONE)

# lock exchange experiments
add_subdirectory(config/lock_exchange run/lock_exchange)
