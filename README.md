A fork of ml-metadata supporting ONLY remote gRPC connection,
at the same time the resulting Python wheel is more platform and architecture agnostic.

## v1.14.0

Downloaded wheel for x86 with:

```sh
python -m pip download \
   --no-deps \
   --only-binary=:all: \
   --platform macosx_12_0_x86_64 \
   --python-version 39 \
   --implementation cp \
   --abi cp39 \
   "ml-metadata==1.14.0"
```

Extracted wheel content with: 

```sh
pip install wheel
wheel unpack ml_metadata-1.14.0-cp39-cp39-macosx_12_0_x86_64.whl
```

## References

Inspiration for manual wheel file writing: https://github.com/uranusjr/packaging-the-hard-way
