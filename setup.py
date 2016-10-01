try:
    from setuptools import setup, Extension
except ImportError:
    from distutils.core import setup, Extension

try:
    from Cython.Build import cythonize
except ImportError:
    def cythonize(paths):
        return paths

from distutils.command.build_clib import build_clib as _build_clib

import subprocess
import os
import shutil
import numpy as np

class build_clib(_build_clib):
    def configure_liquid(self):
        subprocess.call(['sh', 'bootstrap.sh'], cwd='liquid-dsp')
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
        'build_clib': build_clib,
    },
)
