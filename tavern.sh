#!/bin/bash
set -Ceu

docker run -it --rm -v $PWD/tests:/usr/local/tavern/tests tavern pytest $@