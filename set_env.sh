#! /usr/bin/env bash
echo "=== OSTYPE     : ${OSTYPE}"
echo "=== pwd        : $(pwd)"

if [ "$OSTYPE" = 'msys' ]; then
  pyexe=python
  pybin=venv/Scripts
elif [ $(uname) = 'Darwin' ]; then
  # macos
  pyexe=python3.9
  pybin=venv/bin
elif [ "$OSTYPE" = 'linux-gnu' ]; then
  # ubuntu
  pyexe=python3
  pybin=venv/bin
else
  echo OS/terminal must be one of MSYS2, MacOS or Ubuntu
  echo unknown: "$OSTYPE" $(uname)
  return 1
fi

return 0
