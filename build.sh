#!/bin/bash

platform=$1
package=$2

# Extract latest ADB version from
# reading HTTP Location header as it
# includes the version name in URL.
ver=$(curl -L --head -s https://dl.google.com/android/repository/platform-tools-latest-${platform}.zip | grep location -m 1)
version=$(python -c "print(\"\"\"${ver}\"\"\".strip('\n\r\t').replace('r', '').replace(' ', '').replace('_', '-').split('-')[-2])")

# Change version code in setup.cfg
sed -i s/0.0.1/${version}/g setup.cfg

# Download ADB files from official source.
curl -L -o adb.zip https://dl.google.com/android/repository/platform-tools-latest-${platform}.zip

# Create dummy files/directories required for creating Python package.
#
# adbx
# ├─ adb
# │  └─ (Binaries will be added here.)
# ├─ __main__.py
# └─ __init__.py 
mkdir adbx
touch adbx/__init__.py
cp scripts/__main__.py adbx/__main__.py
mkdir adbx/adb
echo '__version__ = "'"${version}"'"' >> adbx/__init__.py
echo '__adb_path__ = "..\/Lib\/site-packages\/adbx\/adb\/adb"' >> adbx/__init__.py

# Use adb.bat instead of adb in Windows.
if [[ ${platform} == "windows" ]]
then
    sed -i 's/scripts\/adb/scripts\/adb.bat/g' setup.cfg
fi

# Extract the ADB and move the inner files
# inside to "adb" folder.
#
# extracted/platform-tools -> adbx/adb
mkdir extracted
unzip -qq adb.zip -d extracted
mv extracted/platform-tools/* adbx/adb/

# Change platform name to current platform.
sed -i 's/plat-name=any/plat-name='"${package}"'/g' setup.cfg

# Build Python wheel and
# drop the wheel to "dist" folder.
pip wheel . --wheel-dir dist --no-cache-dir

# Cleanup
rm -rf adbx
rm -rf extracted
rm adb.zip
sed -i 's/scripts\/adb.bat/scripts\/adb/g' setup.cfg
sed -i s/${version}/0.0.1/g setup.cfg
sed -i 's/plat-name='"${package}"'/plat-name=any/g' setup.cfg