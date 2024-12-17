#!/bin/bash
set -e

# Compiler and flags
CXX="g++"
CXXFLAGS="-Wall -std=c++11 -O3 -g"
INCLUDES="-I./src"

# Target folder for fast_align executable
PROJECT_FOLDER="./fast_align"
TARGET_REL_FOLDER="build"

# Check for OpenMP support
if $CXX -fopenmp -dM -E - < /dev/null 2>/dev/null | grep -q _OPENMP; then
    CXXFLAGS+=" -fopenmp"
fi

# Check for SparseHash support
if pkg-config --exists sparsehash 2>/dev/null; then
    CXXFLAGS+=" -DHAVE_SPARSEHASH"
    INCLUDES+=" $(pkg-config --cflags sparsehash)"
fi

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
    #echo "Compiling $src -> $obj"
    echo $INCLUDES
    $CXX $CXXFLAGS -I./ $INCLUDES -c $src -o $obj
    echo "$obj"
}

# Function to move the fast_align executable to the target folder
cd_to_project_folder() {
    local executable="$1"
    if [ ! -d "$PROJECT_FOLDER" ]; then
	git clone https://github.com/clab/fast_align.git "$PROJECT_FOLDER"
    fi
    cd $PROJECT_FOLDER 
}

# Build fast_align
build_fast_align() {
    echo $PWD
    echo "Building fast_align..."
    for src in $FAST_ALIGN_SRCS; do
	echo $src
        FAST_ALIGN_OBJS+=" $(compile $src)"
    done
    $CXX $CXXFLAGS $INCLUDES -o fast_align $FAST_ALIGN_OBJS
    echo "fast_align built successfully!"
}

# Build atools
build_atools() {
    echo "Building atools..."
    for src in $ATOOLS_SRCS; do
        ATOOLS_OBJS+=" $(compile $src)"
    done
    $CXX $CXXFLAGS -I./ $INCLUDES -o atools $ATOOLS_OBJS
    echo "atools built successfully!"
}

# Clean up build files
clean() {
    echo "Cleaning up..."
    rm -f fast_align atools $(find . -name "*.o")
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
        build_fast_align
        ;;
    atools)
        build_atools
        ;;
    clean)
        clean
        ;;
    *)
        echo "Usage: $0 {all|fast_align|atools|clean}"
        exit 1
        ;;
esac
