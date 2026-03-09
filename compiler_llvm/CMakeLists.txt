cmake_minimum_required(VERSION 3.10)
project(qisa_compiler)

# Find LLVM
# Hint: If LLVM is not found, you might need to set LLVM_DIR
# e.g. cmake -DLLVM_DIR=/opt/homebrew/opt/llvm/lib/cmake/llvm ..
find_package(LLVM REQUIRED CONFIG)

message(STATUS "Found LLVM ${LLVM_PACKAGE_VERSION}")
message(STATUS "Using LLVMConfig.cmake in: ${LLVM_DIR}")

list(APPEND CMAKE_MODULE_PATH "${LLVM_CMAKE_DIR}")
include(AddLLVM)

include_directories(${LLVM_INCLUDE_DIRS})
add_definitions(${LLVM_DEFINITIONS})

add_executable(qisa_parser src/qisa_parser.cpp)

# Link against LLVM libraries
# We need Core, IRReader, Support, etc.
llvm_map_components_to_libnames(llvm_libs Core Support IRReader)

target_link_libraries(qisa_parser ${llvm_libs})

set_target_properties(qisa_parser PROPERTIES
    CXX_STANDARD 17
    CXX_STANDARD_REQUIRED ON
)
