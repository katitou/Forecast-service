#!/bin/bash

uvicorn lib.api.routes:app --host 0.0.0.0 --port 8000 --reload