# sudo apt-get install libgoogle-perftools-dev libsparsehash-dev
# sudo apt install cmake
TARGET_FOLDER=fast_align
BUILD_FOLDER=build
cd $TARGET_FOLDER
mkdir -p $BUILD_FOLDER
cd $BUILD_FOLDER
cmake ..
make
