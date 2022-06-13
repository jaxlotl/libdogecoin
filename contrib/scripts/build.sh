#!/bin/bash

# build depends: contrib/scripts/build.sh --host <host triple> --depends
# build: contrib/scripts/build.sh --host <host triple>

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

DEPENDS=""
TARGET_HOST_TRIPLET=""
TARGET_ARCH=""
CONFIGURE_OPTIONS=""
PREFIX="/usr/local"

if has_param '--host' "$@"; then
    TARGET_HOST_TRIPLET=$2
    LIBS+="-levent -levent_core"
    case "$2" in
        "arm-linux-gnueabihf") 
            TARGET_ARCH="armhf"
        ;;
        "aarch64-linux-gnu")
            TARGET_ARCH="arm64"
        ;;
        "x86_64-w64-mingw32")
            TARGET_ARCH="amd64"
            export CFLAGS+="-I`pwd`/depends/$TARGET_HOST_TRIPLET/include/"
            export LDFLAGS+="-I`pwd`/depends/$TARGET_HOST_TRIPLET/lib/"
            export LDFLAGS+="-s -static --static -static-libgcc -static-libstdc++"
            export LD_LIBRARY_PATH+=`pwd`/depends/$TARGET_HOST_TRIPLET/lib
            export PKG_CONFIG_PATH+=`pwd`/depends/$TARGET_HOST_TRIPLET/lib/pkgconfig
            LIBS+=" -lpthread -lwinpthread"
        ;;
        "i686-w64-mingw32")
            TARGET_ARCH="i386"
            LDFLAGS+=-no-undefined
            LIBS+=" -lpthread -lwinpthread -lshell32 -ladvapi32 -liphlpapi -lws2_32 -lbcrypt -lcrypt32 -DWIN32"
        ;;
        "x86_64-apple-darwin14")
            TARGET_ARCH="amd64"
        ;;
        "x86_64-pc-linux-gnu")
            TARGET_ARCH="amd64"
        ;;
        "i686-pc-linux-gnu")
            TARGET_ARCH="i386"
        ;;
    esac
fi

if has_param '--depends' "$@"; then
    DEPENDS=1
    PREFIX=`pwd`/depends/$TARGET_HOST_TRIPLET
    export LIBS
    export LIBTOOL_APP_LDFLAGS="-all-static"
fi

./autogen.sh
if [ $DEPENDS ]; then
    echo $PREFIX
    ./configure \
    --prefix=$PREFIX --enable-reduce-exports --enable-static --disable-shared
else
    ./configure
fi
make