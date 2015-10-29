#!/bin/bash
export PYTHONPATH=/Users/paramvirdehal/KBase/Trimmomatic/lib:$PATH:$PYTHONPATH
python /Users/paramvirdehal/KBase/Trimmomatic/lib/Trimmomatic/TrimmomaticServer.py $1 $2 $3
