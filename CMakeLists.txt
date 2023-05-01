cmake_minimum_required(VERSION 3.22)

#Project name
project(codeviz_main)

#System check
if(CMAKE_COMPILER_IS_GNUCC OR CMAKE_COMPILER_IS_GNUCXX)
find_package(Threads) #For -pthread linker flag when compiling in Linux
endif()

# print GC version
if (CMAKE_COMPILER_IS_GNUCC AND CMAKE_CXX_COMPILER_VERSION VERSION_GREATER 6.1)
	message(INFO "GCC ver > 6.1")
elseif(CMAKE_COMPILER_IS_GNUCC)
	message(FATAL_ERROR "GCC ver < 6.1")
endif()

####FLEX AND BISON####



###BUILD###
#set(CMAKE_CXX_FLAGS "-std=c++17 ${CMAKE_CXX_FLAGS}")
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_BUILD_TYPE Debug)
#add_compile_options(-fdump-rtl-all-graph)

#Include directories; header files
include_directories(
    include
	include/parsernodes
	include/file_mgmt
	include/lexparse	
)	

#Create a C++ library from the available .cpp files except main
add_library(codeviz_main_lib
	src/parsernodes/parsernodetypes.cpp
	src/file_mgmt/filedeleter.cpp
	src/file_mgmt/fileopener.cpp
	src/file_mgmt/filefinder.cpp
	src/file_mgmt/filewriter.cpp
	src/lexparse/tokenizer.cpp
)


add_executable(codeviz_main src/main.cpp)

target_link_libraries(codeviz_main
    codeviz_main_lib	
)