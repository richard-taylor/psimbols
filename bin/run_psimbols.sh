#!/bin/bash

TOP=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)

export PYTHONPATH=$TOP

# run the psimbols python script with the parameters from this script appended.

python3 $TOP/bin/psimbols $*
