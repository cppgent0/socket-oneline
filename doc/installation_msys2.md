* ensure pacman is installed

  * open browser to https://www.msys2.org/wiki/MSYS2-installation/
  * follow instructions to install update MSYS2 and pacman
  
```bash
% pacman --version
# confirm it is v6.0.1 or later
```

* ensure python 3.10.9 is installed
   * go to  https://www.python.org/downloads/

* update .bashrc for PATH
```bash
# ensure these are before the msys2 directories
PATH="/c/Program Files/Python310/Scripts":$PATH
PATH="/c/Program Files/Python310":$PATH
```

```bash
python --version
# confirm it is 3.10.9
```

* install on Win MSYS2

```bash
./do_install_msys2
```
