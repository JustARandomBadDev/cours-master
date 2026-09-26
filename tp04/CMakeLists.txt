cmake_minimum_required(VERSION 3.28)

project(
    ParticlesSystem
    VERSION 1.0.0
    LANGUAGES CXX
)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# ---------------------------------------------------------------------------
# clangd
# ---------------------------------------------------------------------------

file(
    WRITE "${CMAKE_CURRENT_SOURCE_DIR}/.clangd"
    "CompileFlags:\n"
    "  Remove:\n"
    "    - -mno-direct-extern-access\n"
)

# ---------------------------------------------------------------------------
# Qt
# ---------------------------------------------------------------------------

set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTOUIC OFF)
set(CMAKE_AUTORCC OFF)

# ---------------------------------------------------------------------------
# Dependencies
# ---------------------------------------------------------------------------

find_package(Qt6 REQUIRED COMPONENTS
    Core
    Gui
    Widgets
    Xml
    OpenGL
    OpenGLWidgets
)

find_package(OpenGL REQUIRED)

include(FetchContent)

# libQGLViewer
FetchContent_Declare(
    libQGLViewer
    GIT_REPOSITORY https://github.com/GillesDebunne/libQGLViewer.git
    GIT_TAG da4bfad6c53b234088492ba4bae62e736a12f8f5
    EXCLUDE_FROM_ALL
)

# GLM 1.0.3
FetchContent_Declare(
    glm
    GIT_REPOSITORY https://github.com/g-truc/glm.git
    GIT_TAG 1.0.3
    EXCLUDE_FROM_ALL
)

FetchContent_MakeAvailable(
    libQGLViewer
    glm
)

# ---------------------------------------------------------------------------
# Sources
# ---------------------------------------------------------------------------

file(GLOB_RECURSE PROJECT_SOURCES CONFIGURE_DEPENDS
    "${CMAKE_CURRENT_SOURCE_DIR}/src/*.cpp"
)

file(GLOB_RECURSE PROJECT_HEADERS CONFIGURE_DEPENDS
    "${CMAKE_CURRENT_SOURCE_DIR}/include/*.h"
    "${CMAKE_CURRENT_SOURCE_DIR}/include/*.hpp"
)

# ---------------------------------------------------------------------------
# Executable
# ---------------------------------------------------------------------------

add_executable(${PROJECT_NAME}
    ${PROJECT_SOURCES}
    ${PROJECT_HEADERS}
)

target_include_directories(${PROJECT_NAME}
    PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/include
)

target_link_libraries(${PROJECT_NAME}
    PRIVATE
        QGLViewer
        glm::glm

        Qt6::Core
        Qt6::Gui
        Qt6::Widgets
        Qt6::Xml
        Qt6::OpenGL
        Qt6::OpenGLWidgets

        OpenGL::GL
)

target_compile_options(${PROJECT_NAME}
    PRIVATE
        -Wall
        -Wextra
        -Wpedantic
)