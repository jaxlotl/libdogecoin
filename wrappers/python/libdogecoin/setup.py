from setuptools import setup, Extension, Command
from Cython.Build import cythonize
from Cython.Distutils import build_ext

depends_lib = ""

class BuildDepends(Command):
    user_options = [
        ('host=', None, "Specify the host architecture.")
    ]
    def initialize_options(self):
        self.host = "x86_64-pc-linux-gnu"
    def finalize_options(self):
        assert self.host in ("arm-linux-gnueabihf",
                            "aarch64-linux-gnu",
                            "x86_64-pc-linux-gnu",
                            "x86_64-apple-darwin14",
                            "x86_64-w64-mingw32",
                            "i686-w64-mingw32",
                            "i686-pc-linux-gnu",), "Invalid architecture."
    def run(self):
        depends_lib = self.host
        
libdoge_extension = [Extension(
    name=               "libdogecoin",
    language=           "c",
    sources=            ["wrappers/python/libdogecoin/libdogecoin.pyx"],
    include_dirs=       [".",
                        "include",
                        "include/dogecoin",
                        "secp256k1/include"],
    libraries =         ["event", "event_core", "pthread", "m"],
    library_dirs =      ["depends/" + depends_lib + "/lib"],
    extra_objects=      [".libs/libdogecoin.a"],
    extra_compile_args= ["--static", "-fPIC"]
)]

setup(
    name=               "libdogecoin",
    version=            "0.0.1",
    description=        "Python interface for the libdogecoin C library",
    author=             "Jackie McAninch",
    author_email=       "jackie.mcaninch.2019@gmail.com",
    license=            "MIT",
    cmdclass =          {'build_ext': build_ext,
                         'build_depends': BuildDepends},
    ext_modules=        cythonize(libdoge_extension, language_level = "3")
)
