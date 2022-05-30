#!/bin/bash
# helper script to install dependencies, clean, build and run cython unit tests:

# install:
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade cython setuptools

# clean:
FILE=`pwd`/bindings/python/libdogecoin/libdogecoin.c
if test -f "$FILE"; then
    rm `pwd`/bindings/python/libdogecoin/libdogecoin.c `pwd`/bindings/python/libdogecoin/libdogecoin.o
fi

# build:
python3 bindings/python/libdogecoin/setup.py build_ext --build-lib `pwd`/bindings/python/pytest/ --build-temp `pwd`/ --force --user

# # run:
python3 bindings/python/pytest/address_test.py 
# PYTHONDEBUG=1 PYTHONMALLOC=debug valgrind --tool=memcheck --leak-check=full --track-origins=yes -s \
# --suppressions=`pwd`/bindings/py_wrappers/pytest/valgrind-python3.supp \
# --log-file=`pwd`/bindings/py_wrappers/pytest/minimal.valgrind.log \
# python33-dbg -Wd -X tracemalloc=5 bindings/py_wrappers/pytest/transaction_test.py -v
python3 bindings/python/pytest/transaction_test.py -v
deactivate
rm -rf .venv
