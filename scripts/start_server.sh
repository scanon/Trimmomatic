#!/bin/bash
export KB_DEPLOYMENT_CONFIG=/Users/paramvirdehal/KBase/Trimmomatic/deploy.cfg
export PYTHONPATH=/Users/paramvirdehal/KBase/Trimmomatic/lib:$PATH:$PYTHONPATH
uwsgi --master --processes 5 --threads 5 --http :5000 --wsgi-file /Users/paramvirdehal/KBase/Trimmomatic/lib/Trimmomatic/TrimmomaticServer.py
