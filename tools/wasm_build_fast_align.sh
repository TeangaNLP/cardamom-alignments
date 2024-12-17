#!/bin/bash
set -e

# Base folder for wasi-sdk
BASE_FOLDER=../wasi-sdk-24.0-x86_64-linux

# Compiler and flags
CXX="$BASE_FOLDER/bin/clang++"  # Use clang++ from wasi-sdk
CXXFLAGS="--target=wasm32-wasi -O3 -g"  # Target Wasm and enable optimizations
INCLUDES="-I./"  # Include the 'src' directory for header files

# Linker flags for Wasm
LINKER_FLAGS="-lc -lm -Wl,--export-all -Wl,--no-entry"

# Target folder for Wasm executables
PROJECT_FOLDER="./fast_align"
TARGET_REL_FOLDER="build_wasm"

# Source files
FAST_ALIGN_SRCS="src/fast_align.cc src/ttables.cc"
ATOOLS_SRCS="src/alignment_io.cc src/atools.cc"

# Object files
FAST_ALIGN_OBJS=""
ATOOLS_OBJS=""

# Function to compile source files into object files
compile() {
    local src="$1"
    local obj="${src%.cc}.o"
    #echo "Compiling $src to $obj"
    $CXX $CXXFLAGS $INCLUDES -c $src -o $obj --sysroot=$BASE_FOLDER/share/wasi-sysroot
}

# Function to move the Wasm executables to the target folder
cd_to_project_folder() {
    if [ ! -d "$PROJECT_FOLDER" ]; then
        echo "fast_align folder not found. Cloning the repository..."
        git clone https://github.com/clab/fast_align.git "$PROJECT_FOLDER"
    fi
    cd "$PROJECT_FOLDER" || { echo "Failed to enter the fast_align directory."; exit 1; }
}

# Build fast_align
build_fast_align() {
    echo "Building fast_align..."
    for src in $FAST_ALIGN_SRCS; do
        FAST_ALIGN_OBJS+=" $(compile $src)"
    done
    $CXX $CXXFLAGS $INCLUDES -o fast_align.wasm $FAST_ALIGN_OBJS $LINKER_FLAGS --sysroot=$BASE_FOLDER/share/wasi-sysroot
    echo "fast_align.wasm built successfully!"
}

# Build atools
build_atools() {
    echo "Building atools..."
    for src in $ATOOLS_SRCS; do
        ATOOLS_OBJS+=" $(compile $src)"
    done
    $CXX $CXXFLAGS $INCLUDES -o atools.wasm $ATOOLS_OBJS $LINKER_FLAGS --sysroot=$BASE_FOLDER/share/wasi-sysroot
    echo "atools.wasm built successfully!"
}

# Clean up build files
clean() {
    echo "Cleaning up..."
    rm -f fast_align.wasm atools.wasm $(find . -name "*.o")
    rm -rf "$TARGET_REL_FOLDER"
    echo "Clean complete!"
}

# Main script logic
case "$1" in
    all)
        cd_to_project_folder
        build_fast_align
        build_atools
        ;;
    fast_align)
        cd_to_project_folder
        build_fast_align
        ;;
    atools)
        cd_to_project_folder
        build_atools
        ;;
    clean)
        cd_to_project_folder
        clean
        ;;
    *)
        echo "Usage: $0 {all|fast_align|atools|clean}"
        exit 1
        ;;
esac
