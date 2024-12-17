#!/bin/bash
# #### FROM source
# requirements
# cmake
# clang
# ninja
# python3
#git clone --recursive https://github.com/WebAssembly/wasi-sdk.git
# cd wasi-sdk
#cmake -G Ninja -B build/toolchain -S . -DWASI_SDK_BUILD_TOOLCHAIN=ON -DCMAKE_INSTALL_PREFIX=build/install
#cmake --build build/toolchain --target install

### FROM binary
WASI_OS=linux
WASI_ARCH=x86_64
WASI_VERSION=24
WASI_VERSION_FULL=${WASI_VERSION}.0
wget https://github.com/WebAssembly/wasi-sdk/releases/download/wasi-sdk-${WASI_VERSION}/wasi-sdk-${WASI_VERSION_FULL}-${WASI_ARCH}-${WASI_OS}.tar.gz
tar xvf wasi-sdk-${WASI_VERSION_FULL}-${WASI_ARCH}-${WASI_OS}.tar.gz
