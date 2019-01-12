#!/usr/bin/env python3
import os
from setuptools import setup

setup(
  name = "edapack",
  packages=['edapack'],
  author = "Matthew Ballance",
  author_email = "matt.ballance@gmail.com",
  description = ("EDAPack is a pre-compiled collection of open source EDA tools"),
  license = "Apache 2.0",
  keywords = ["Electronic Design Automation"],
  url = "https://github.com/EDAPack/edapack",
  # TODO
  entry_points={
    'console_scripts': [
      'edapack = edapack.__main__:main'
    ]
  }
)

