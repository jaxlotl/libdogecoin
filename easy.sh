make clean
make -C depends HOST=x86_64-pc-linux-gnu
./autogen.sh
./configure --prefix=`pwd`/depends/x86_64-pc-linux-gnu  LD_LIBRARY_PATH='`pwd`/depends/x86_64-pc-linux-gnu/lib/' CFLAGS='-I`pwd`/depends/x86_64-pc-linux-gnu/include/ -fPIC' LDFLAGS='-L`pwd`/depends/x86_64-pc-linux-gnu/lib' PKG_CONFIG_PATH=`pwd`/depends/x86_64-pc-linux-gnu/lib/pkgconfig LIBS='-levent -levent_core -lm -levent_pthreads' --enable-static --disable-shared
make
rm bindings/py_wrappers/libdogecoin/libdogecoin.c
python3 setup.py build_ext --inplace
python3 test.py
