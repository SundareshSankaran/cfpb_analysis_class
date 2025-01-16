#!/usr/bin/env bash

set -euo pipefail

python -m venv cfpb
. cfpb/bin/activate

pip install --upgrade pip uv
uv pip install -r requirements.txt --force-reinstall --upgrade

python -m ipykernel install --user --name=cfpb


deactivate

rm -rf cfpb