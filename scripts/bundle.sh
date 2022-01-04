#! /bin/bash
die () {
    echo >&2 "$@"
    exit 1
}

[ "$#" -eq 1 ] || die "1 argument required, $# provided"
version=$1 

# Cleanup existing builds and artifacts
rm -rf ./dist
rm -rf ./build

# Build
pyinstaller --name floatingfile --add-data '.env:.' --paths env/lib/python3.10/site-packages main.py

# Compress
tar -C ./dist -czf "floatingfile-$version.tar.gz" floatingfile