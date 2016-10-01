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
import numpy as np

class build_clib(_build_clib):
    def configure_liquid(self):
        SOURCE_DIR = os.path.join(os.getcwd(), 'liquid-dsp')
        subprocess.call(['sh', 'bootstrap.sh'], cwd=SOURCE_DIR)
        subprocess.call(['sh', 'configure', '--enable-simdoverride', '--prefix='], cwd=SOURCE_DIR)

    def build_libraries(self, libraries):
        self.configure_liquid()
        _build_clib.build_libraries(self, libraries)

extensions = cythonize([
    Extension('pyliquiddsp.libliquid',
        sources=['pyliquiddsp/libliquid.pyx'],
    )
])

libraries = [
    ('liquid', {
        'include_dirs': ['liquid-dsp', 'liquid-dsp/include'],
        'sources': open('liquid-dsp.files').read().splitlines(),
    })
]

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
