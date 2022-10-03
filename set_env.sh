#! /usr/bin/env bash
echo "=== OSTYPE     : ${OSTYPE}"
echo "=== pwd        : $(pwd)"

if [ "$OSTYPE" = 'msys' ]; then
  pyexe=python
  pybin=venv/Scripts
else
  # ubuntu
  pyexe=python3
  pybin=venv/bin
fi
