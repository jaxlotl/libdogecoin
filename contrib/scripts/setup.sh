#!/bin/bash
export LC_ALL=C
set -e -o pipefail

if [ $# -eq 0 ]; then
    echo "No arguments provided"
    exit 1
fi

has_param() {
    local term="$1"
    shift
    for arg; do
        if [[ $arg == "$term" ]]; then
            return 0
        fi
    done
    return 1
}

COMMON_PACKAGES="autoconf automake bison build-essential curl ca-certificates libtool libtool-bin pkg-config procps python3 rsync valgrind"
ARCH_PACKAGES=""
DEPENDS=""
TARGET_HOST_TRIPLET=""
TARGET_ARCH=""

if has_param '--depends' "$@"; then
    DEPENDS=1
else
    COMMON_PACKAGES+=" libevent-dev"
fi

if has_param '--host' "$@"; then
    case "$2" in
        "arm-linux-gnueabihf") 
            if [ $DEPENDS ]; then
                ARCH_PACKAGES+="g++-arm-linux-gnueabihf "
            fi
            ARCH_PACKAGES+="qemu-user-static qemu-user"
            TARGET_ARCH="armhf"
        ;;
        "aarch64-linux-gnu")
            if [ $DEPENDS ]; then
                ARCH_PACKAGES+="g++-aarch64-linux-gnu "
            fi
            ARCH_PACKAGES+="qemu-user-static qemu-user"
            TARGET_ARCH="arm64"
        ;;
        "x86_64-w64-mingw32")
            if [ $DEPENDS ]; then
                ARCH_PACKAGES+="g++-mingw-w64 "
            fi
            ARCH_PACKAGES+="nsis wine32 wine-stable bc wine-binfmt"
            TARGET_ARCH="amd64"
        ;;
        "i686-w64-mingw32")
            if [ $DEPENDS ]; then
                ARCH_PACKAGES+="g++-mingw-w64 "
            fi
            ARCH_PACKAGES+="nsis wine32 wine-stable bc wine-binfmt"
            TARGET_ARCH="i386"
        ;;
        "x86_64-apple-darwin14")
            ARCH_PACKAGES="cmake zlib xorriso"
            TARGET_ARCH="amd64"
        ;;
        "x86_64-pc-linux-gnu") 
            ARCH_PACKAGES="python3-dev python3-dbg python"
            TARGET_ARCH="amd64"
        ;;
        "i686-pc-linux-gnu")
            if [ $DEPENDS ]; then
                ARCH_PACKAGES+="g++-multilib "
            fi
            ARCH_PACKAGES+="bc"
            TARGET_ARCH="i386"
        ;;
    esac
    TARGET_HOST_TRIPLET=$2
fi

OPTIONS=""
sudo dpkg --add-architecture $TARGET_ARCH
if [[ $TARGET_HOST_TRIPLET == "x86_64-apple-darwin14" ]]; then
    brew update
    brew install automake coreutils libtool python3 $ARCH_PACKAGES
    SDK_VERSION=10.14
    SDK_URL=https://bitcoincore.org/depends-sources/sdks
    SDK_SHASUM="be17f48fd0b08fb4dcd229f55a6ae48d9f781d210839b4ea313ef17dd12d6ea5"
    mkdir -p ./depends/sdk-sources
    mkdir -p ./depends/SDKs
    echo "$SDK_SHASUM depends/sdk-sources/Xcode-12.1-12A7403-extracted-SDK-with-libcxx-headers.tar.gz" | sha256sum -c || \
    curl --location --fail $SDK_URL/Xcode-12.1-12A7403-extracted-SDK-with-libcxx-headers.tar.gz -o depends/sdk-sources/Xcode-12.1-12A7403-extracted-SDK-with-libcxx-headers.tar.gz && \
    echo "$SDK_SHASUM depends/sdk-sources/Xcode-12.1-12A7403-extracted-SDK-with-libcxx-headers.tar.gz" | sha256sum -c
    tar -C depends/SDKs -xf depends/sdk-sources/Xcode-12.1-12A7403-extracted-SDK-with-libcxx-headers.tar.gz
else
    sudo apt-get update
    DEBIAN_FRONTEND=noninteractive sudo apt-get install --no-install-recommends -y $COMMON_PACKAGES $ARCH_PACKAGES
    if ([ "$TARGET_HOST_TRIPLET" == "i686-w64-mingw32" ]); then
        sudo update-alternatives --set i686-w64-mingw32-gcc /usr/bin/i686-w64-mingw32-gcc-posix
        sudo update-alternatives --set i686-w64-mingw32-g++  /usr/bin/i686-w64-mingw32-g++-posix
        sudo update-binfmts --import /usr/share/binfmts/wine
        exit
    elif ([ "$TARGET_HOST_TRIPLET" == "x86_64-w64-mingw32" ]); then
        sudo update-alternatives --set x86_64-w64-mingw32-gcc  /usr/bin/x86_64-w64-mingw32-gcc-posix
        sudo update-alternatives --set x86_64-w64-mingw32-g++  /usr/bin/x86_64-w64-mingw32-g++-posix
        sudo update-binfmts --import /usr/share/binfmts/wine
        exit
    fi
fi
NO_X_COMPILE=("x86_64-pc-linux-gnu" "i686-pc-linux-gnu" "x86_64-apple-darwin14");

if [ "$DEPENDS" = "1" ]; then
    match=0
    for str in ${NO_X_COMPILE[@]}; do
        if [[ "$HOST" == "$str" ]]; then
            match=1
            break
        fi
    done
    if [[ $match = 0 ]]; then
        OPTIONS="CROSS_COMPILE='yes' "
    fi
    OPTIONS+="SPEED=slow V=1"
    make -C depends HOST=$TARGET_HOST_TRIPLET $OPTIONS
fi
