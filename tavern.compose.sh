#!/bin/bash

set -Ceu

docker compose exec tavern pytest -vv $@