#!/bin/bash

EXPECTED_DIR="REST_API_Messaging"
CURRENT_DIR=$(basename "$PWD")

if [[ "$CURRENT_DIR" != "$EXPECTED_DIR" ]]; then
    echo "Please run this script from the project root directory: $EXPECTED_DIR"
    exit 1
fi

PYTHONPATH=$(pwd) pytest tests/
