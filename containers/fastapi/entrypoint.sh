#!/bin/bash

set -eu

poetry run uvicorn main:app --reload --host 0.0.0.0 --port 8000
