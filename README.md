# adbx

A dummy Python package that contains [ADB](https://developer.android.com/studio/releases/platform-tools) binaries which will be registered in PATH, so you don't have to do yourself.

> Only Windows and Linux supported at the moment.

```
pip install adbx
```

```
adb devices
```

At 00:00 on every Monday, a new ADB version will be checked and will be published as a new version to PyPI. If you don't want to wait, you can [build the wheel yourself.](#build)

### Details

Along with binaries, the package also contains a script that runs ADB executable with passing arguments as-it-is. And when you install the package, `pip` automatically copies the script to Python's `Scripts` folder. And as `Scripts` folder are added already to PATH when you installed Python<sup>[1]</sup>, you don't need to do anything on your end.

<sup>[1]</sup> Only if you selected "Add to PATH" option in Python setup, otherwise you will need to modify your PATH manually.

```
$ adb --version
Android Debug Bridge version 1.0.41
Version 33.0.0-8141338
Installed as C:\Users\ycdem\AppData\Local\Programs\Python\Python39\Lib\site-packages\adbx\adb\adb.exe
```

If `adb` is reserved or used for another command in the system, you can alternatively use:

```
python -m adbx --version
```

Package version equals to ADB version, it is determined before building the wheel. You can also read `__version__` attribute to use in Python.

```
$ python -c "import adbx; print(adbx.__version__)"
33.0.0
```

And as this is an actual package like other Python packages, you can update and uninstall it with `pip`.

```
pip uninstall adbx
```

```
pip install adbx --upgrade
```

### How?

Take a look to [build.sh](build.sh)

### Why?

Because it looks nicer when installed as a package. But if you still want to download and add to PATH manually, then it's your choice.

### License

The scripts are licensed with CC0 1.0. However, this doesn't apply for ADB binaries which licensed with Apache License 2.0. 

### Build

Install and/or update `pip` and run:

```
./build.sh windows win32
```

First argument: Platform name that will be appended to download URL. (e.g `windows` > `platform-tools-latest-windows.zip`)<br>
Second argument: Platform tag which will be used in `pip wheel`, (e.g `win32` > `adbx-33.0.0-py3-none-win32.whl`)
