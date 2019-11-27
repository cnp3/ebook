#!/bin/bash

# install the required python extensions
mkdir python
cd python
git clone https://github.com/obonaventure/mscgen.git
pip3 install -e mscgen
git clone https://github.com/obonaventure/tikz.git
pip3 install -U -e tikz
cd ..
# on error exit
set -e
# Flags used here, not in `make html`:
#  -n   Run in nit-picky mode. Currently, this generates warnings for all missing references.
#  -W   Turn warnings into errors. This means that the build stops at the first warning and sphinx-build exits with exit status 1.
#  -N   Do not emit colors
#  -T   output full traceback

# Build images
cd pkt
make
cd ..
# Spell checker
sphinx-build --keep-going -b spelling . /tmp
# --keep-going continue the processing after a warning
sphinx-build  -WNT --keep-going -b html . /tmp

