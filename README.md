# adbx

A dummy Python package that contains [ADB](https://developer.android.com/studio/releases/platform-tools) binaries which will be registered in PATH, so you don't have to do yourself.

```
python -m pip install adbx
```

```
$ adb --version
Android Debug Bridge version 1.0.41
Version 33.0.0-8141338
```

Package version equals to ADB version, it is dynamically set before building the wheel.

```
$ python
>>> import adbx
>>> adbx.__version__
33.0.0
```

And as this is an actual package like other Python packages, you can update and uninstall it with `pip`.

```
python -m pip uninstall adbx
```

```
python -m pip install adbx --upgrade
```

If you want to build wheel yourself:

```
python -m pip install -r requirements.txt
python ./pack.py win32 windows
```

> First argument: Platform tag which will be used in `pip wheel`, (`win32` builds wheel named in `adbx-33.0.0-py3-none-win32.whl`)<br>
> Second argument: Which platform ADB binaries needs to download for. (`windows` downloads `platform-tools-latest-windows.zip`)

---

Code is licensed with CC0 1.0. However, this doesn't apply for ADB binaries which licensed with Apache License 2.0. 