#!/bin/bash

echo "=============="
ls
echo "=============="
cd /workspace
ls
echo "=============="
ls repo
python3 testExecutor.py "$@"