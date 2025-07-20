#!/bin/bash

echo "=============="
ls
echo "=============="
cd /workspace
ls
echo "=============="
ls /workspace/repo
echo "--------------"
python3 testExecutor.py "$@"