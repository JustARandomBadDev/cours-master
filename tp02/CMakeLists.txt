cmake_minimum_required(VERSION 3.28)

project(
    blendshape
    VERSION 1.0.0
    LANGUAGES CXX
)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Generate compile_commands.json for clangd.
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# ---------------------------------------------------------------------------
# clangd
# ---------------------------------------------------------------------------

# Some dependencies/toolchains can add GCC-specific flags to
# compile_commands.json that clangd does not understand.
#
# Keep the real compilation command intact and only ask clangd to ignore
# those flags during code analysis.
file(
    WRITE "${CMAKE_CURRENT_SOURCE_DIR}/.clangd"
    "CompileFlags:\n"
    "  Remove:\n"
    "    - -mno-direct-extern-access\n"
)

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

# libQGLViewer 3.0.0
#
# Pinned to a specific commit instead of "main" so the project remains
# reproducible.
FetchContent_Declare(
    libQGLViewer
    GIT_REPOSITORY https://github.com/GillesDebunne/libQGLViewer.git
    GIT_TAG da4bfad6c53b234088492ba4bae62e736a12f8f5
    EXCLUDE_FROM_ALL
)

FetchContent_MakeAvailable(libQGLViewer)

# ---------------------------------------------------------------------------
# Executable
# ---------------------------------------------------------------------------

add_executable(blendshape
    src/main.cpp
    src/Viewer.cpp
    src/BlendShape.cpp
    src/Vertex.cpp
    src/glm.cpp

    include/Viewer.h
    include/BlendShape.h
    include/Vertex.h
    include/glm.h
    include/ui_viewerInterface.h
)

target_include_directories(blendshape
    PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/include
)

target_link_libraries(blendshape
    PRIVATE
        QGLViewer

        Qt6::Core
        Qt6::Gui
        Qt6::Widgets
        Qt6::Xml
        Qt6::OpenGL
        Qt6::OpenGLWidgets

        OpenGL::GL
)

# Absolute path to the project's assets directory.
#
# Can be used in C++ as:
#
#   std::string path = ASSETS_DIR "/bs/body.obj";
#
target_compile_definitions(blendshape
    PRIVATE
        ASSETS_DIR="${CMAKE_CURRENT_SOURCE_DIR}/assets"
)

# Copy assets next to the executable as well.
add_custom_command(
    TARGET blendshape
    POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy_directory
        ${CMAKE_CURRENT_SOURCE_DIR}/assets
        $<TARGET_FILE_DIR:blendshape>/assets
)