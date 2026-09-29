#!/usr/bin/env bash

echo "Starting EduGenie..."

source .venv/bin/activate

uvicorn main:app --reload