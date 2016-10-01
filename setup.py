try:
    from setuptools import setup, Extension, Command
except ImportError:
    from distutils.core import setup, Extension, Command

try:
    from Cython.Build import cythonize
except ImportError:
    def cythonize(paths):
        return paths

import subprocess
import os
import shutil
import numpy as np
from distutils.command.build_clib import build_clib as _build_clib
from distutils.command.sdist import sdist

class bootstrap(Command):
    description = "bootstrap by automake and autoconf"
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        subprocess.call(['bootstrap.sh'], cwd='liquid-dsp', env={'ACLOCAL_PATH': './scripts'})

class build_clib(_build_clib):
    def configure_liquid(self):
        if os.path.exists('liquid-dsp/configure'):
            subprocess.call(['bootstrap.sh'], cwd='liquid-dsp', env={'ACLOCAL_PATH': './scripts'})
        subprocess.call(['sh', 'configure'], cwd='liquid-dsp')
        subprocess.call(['make', 'libliquid.a'], cwd='liquid-dsp')

    def install_liquid(self):
        shutil.copyfile('liquid-dsp/libliquid.a', os.path.join(self.build_clib, 'libliquid.a'))

    def build_libraries(self, libraries):
        self.configure_liquid()
        _build_clib.build_libraries(self, libraries)
        self.install_liquid()

extensions = cythonize([
    Extension('pyliquiddsp.libliquid',
        sources=['pyliquiddsp/libliquid.pyx'],
    )
])

libraries = [('liquid', {
    'sources': ['liquid-dsp/src/libliquid.c'],
    'include_dirs': ['liquid-dsp', 'liquid-dsp/include'],
})]

setup(
    name='pyliquiddsp',
    packages=['pyliquiddsp'],
    ext_modules=extensions,
    libraries=libraries,
    include_dirs=[np.get_include(), 'pyliquiddsp/include'],
    cmdclass={
        'bootstrap': bootstrap,
        'build_clib': build_clib,
    },
)
