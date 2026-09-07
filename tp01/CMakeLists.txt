cmake_minimum_required(VERSION 3.16)

project(qglviewer_test LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

find_package(Qt5 REQUIRED COMPONENTS
    Widgets
    OpenGL
    Xml
)

find_package(OpenGL REQUIRED)

find_path(QGLVIEWER_INCLUDE_DIR
    NAMES QGLViewer/qglviewer.h
    PATHS /usr/include
)

find_library(QGLVIEWER_LIBRARY
    NAMES QGLViewer-qt5 QGLViewer
    PATHS /usr/lib
)

if(NOT QGLVIEWER_INCLUDE_DIR OR NOT QGLVIEWER_LIBRARY)
    message(FATAL_ERROR "QGLViewer not found")
endif()

file(GLOB_RECURSE SOURCES CONFIGURE_DEPENDS
    "${CMAKE_SOURCE_DIR}/src/*.cpp"
)

add_executable(qglviewer_test
    ${SOURCES}
)

target_include_directories(qglviewer_test PRIVATE
    ${CMAKE_SOURCE_DIR}/include
    ${QGLVIEWER_INCLUDE_DIR}
)

target_link_libraries(qglviewer_test PRIVATE
    Qt5::Widgets
    Qt5::OpenGL
    Qt5::Xml
    OpenGL::GL
    ${QGLVIEWER_LIBRARY}
)
