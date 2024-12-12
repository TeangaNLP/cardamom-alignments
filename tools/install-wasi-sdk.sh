#!/bin/bash
# requirements
# cmake
# clang
# ninja
# python3
git clone --recursive https://github.com/WebAssembly/wasi-sdk.git
cd wasi-sdk
cmake -G Ninja -B build/toolchain -S . -DWASI_SDK_BUILD_TOOLCHAIN=ON -DCMAKE_INSTALL_PREFIX=build/install
cmake --build build/toolchain --target install
