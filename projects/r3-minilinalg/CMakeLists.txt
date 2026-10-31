cmake_minimum_required(VERSION 3.20)
project(minilinalg LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

add_library(minilinalg src/vector.cpp)
target_include_directories(minilinalg PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include)
target_compile_options(minilinalg PRIVATE -Wall -Wextra -Wpedantic)

add_executable(demo apps/demo.cpp)
target_link_libraries(demo PRIVATE minilinalg)

enable_testing()
include(FetchContent)
FetchContent_Declare(
  googletest
  GIT_REPOSITORY https://github.com/google/googletest.git
  GIT_TAG v1.15.2
  GIT_SHALLOW TRUE
)
set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
FetchContent_MakeAvailable(googletest)

add_executable(tests tests/test_vector.cpp)
target_link_libraries(tests PRIVATE minilinalg GTest::gtest_main)
include(GoogleTest)
gtest_discover_tests(tests)