#!/bin/bash
set -e

# Install with only pre-built wheels, no compilation
pip install --upgrade pip setuptools
pip install --no-build-isolation --only-binary :all: -r requirements.txt || pip install -r requirements.txt

echo "Build completed successfully"
