from distutils.core import setup, Extension

main_module = Extension(
    "agamim",
    sources = ["src/agamim.c", ]
    )

setup(
    name = "agamim",
    version = "4.0",
    description = "The Agamim values.",
    ext_modules = [main_module, ]
    )
