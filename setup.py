from setuptools import setup, Extension
from Cython.Build import cythonize
import os

# Define the extension module
extensions = [
    Extension(
        "neuronet",
        sources=["cython/neuronet.pyx", "src/GrafoDisperso.cpp"],
        include_dirs=["src"],  # Include the src directory for headers
        language="c++",
        extra_compile_args=["-std=c++11", "-O3"],
    )
]

setup(
    name="neuronet",
    ext_modules=cythonize(extensions),
)
