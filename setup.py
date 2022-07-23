from distutils.core import setup
from Cython.Build import cythonize
from setuptools import Extension, setup

ext_modules=[
    Extension(
      'simulation',
      ['simulation.pyx'],
      extra_compile_args=['/O3'],
      language='c++'
    )
]

setup(
    name='MainGUI',
    ext_modules=cythonize(ext_modules),
)