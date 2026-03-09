cmake_minimum_required(VERSION 3.10)
project(hal_drivers)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include_directories(include)

add_library(hal_drivers_mock STATIC src/mock_driver.cpp)

# Optional: Build a small test executable to verify the mock driver
add_executable(test_hal src/test_hal.cpp)
target_link_libraries(test_hal hal_drivers_mock)
