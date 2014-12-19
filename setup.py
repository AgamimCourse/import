#! /usr/bin/env python

from distutils.core import setup, Extension

main_module = Extension(
    "agamim",
    define_macros = [
        ("SERVER_HOST", "\"54.213.213.104\""),
        ("SERVER_PORT", 4000),
        ],
    sources = ["src/agamim.c", ]
    )

setup(
    name = "agamim",
    version = "4.0",
    description = "The Agamim values.",
    ext_modules = [main_module, ]
    )
