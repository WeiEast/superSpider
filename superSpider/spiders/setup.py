from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = [], excludes = ["collections.sys","collections._weakref"])

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('SuperSpider.py', base=base)
]

setup(name='SuperSpider',
      version = '1.0',
      description = 'Crawler',
      options = dict(build_exe = buildOptions),
      executables = executables)
