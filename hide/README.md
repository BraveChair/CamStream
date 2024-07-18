# DACERI

## Env Setup
On Raspberry PI, after cloning this repo, setup a Python virtual environment at the root.
```bash
## Bash 
$ python3 -m venv .venv   # setup a Python virtual environment whose name is ".venv". Use `ls -a` to find the .venv repo
$ source .venv/bin/activate  # activate the virtual environment

## Virtual environment .venv
 (.venv)$ pip install pithermalcam  # install the package
```

## Notes
- The trick to make [PiThermalCam](https://github.com/tomshaffner/PiThermalCam) running

  After `pip install pithermacam`, find the `cmapy.py` file and update it as following:
  1. Replace `matplotlib.cm.get_cmap()` with `matplotlib.pyplot.get_cmap()`
  2. At the top of the file, add `import matplotlib.pyplot`

  After that, run the camera test to check if there is any error.
  ```
  (.venv)$ python3 PiThermalCam/examples/cam_test.py 
  ```
  
