#!/bin/bash

echo "=============="
ls
echo "=============="
ls ..
cd /workspace
python3 findTestbox.py "$@"