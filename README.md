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

Removed pywrap module and imports, making note in the code also with trowing RuntimeError.

Testing with launching a local server:

```sh
docker run -p 8080:8080 --env METADATA_STORE_SERVER_CONFIG_FILE=/tmp/shared/conn_config.pb --volume ./ml_metadata-1.14.0:/tmp/shared gcr.io/tfx-oss-public/ml_metadata_store_server:1.14.0
```

In another terminal: `pytest ml_metadata-1.14.0/demo_test.py -vv -s`

```
1 passed in 0.85s
```

Please notice the demo can only work once as creating the MLMD entities twice is not allowed. You might erase the `.sqlite.db` file.

Erase all Docker image running (CAREFUL if using this command where other Docker images are needed/running):
```sh
docker rm -f $(docker ps -a -q)
rm ml_metadata-1.14.0/metadata.sqlite.db
```

Recomputed checksum in `ml_metadata-1.14.0/ml_metadata-1.14.0.dist-info` directory.

## References

Inspiration for manual wheel file writing: https://github.com/uranusjr/packaging-the-hard-way
