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

Rebuild wheel by using `ml_metadata-1.14.0/ml_metadata` and `ml_metadata-1.14.0/ml_metadata-1.14.0.dist-info` in a temporary directory:

```
(venv) ml-metadata-remote % wheel pack temp
Repacking wheel as ./ml_metadata-1.14.0-py3-none-any.whl...creating './ml_metadata-1.14.0-py3-none-any.whl' and adding 'temp' to it
adding 'ml_metadata/__init__.py'
adding 'ml_metadata/errors.py'
adding 'ml_metadata/version.py'
adding 'ml_metadata/metadata_store/__init__.py'
adding 'ml_metadata/metadata_store/metadata_store.py'
adding 'ml_metadata/metadata_store/metadata_store_test.py'
adding 'ml_metadata/metadata_store/mlmd_types.py'
adding 'ml_metadata/metadata_store/mlmd_types_test.py'
adding 'ml_metadata/metadata_store/types.py'
adding 'ml_metadata/metadata_store/types_test.py'
adding 'ml_metadata/proto/__init__.py'
adding 'ml_metadata/proto/metadata_store_pb2.py'
adding 'ml_metadata/proto/metadata_store_service_pb2.py'
adding 'ml_metadata/proto/metadata_store_service_pb2_grpc.py'
adding 'ml_metadata/simple_types/__init__.py'
adding 'ml_metadata/simple_types/proto/__init__.py'
adding 'ml_metadata/simple_types/proto/simple_types_pb2.py'
adding 'ml_metadata-1.14.0.dist-info/LICENSE'
adding 'ml_metadata-1.14.0.dist-info/METADATA'
adding 'ml_metadata-1.14.0.dist-info/WHEEL'
adding 'ml_metadata-1.14.0.dist-info/namespace_packages.txt'
adding 'ml_metadata-1.14.0.dist-info/top_level.txt'
adding 'ml_metadata-1.14.0.dist-info/RECORD'
OK
```

Installing with `pip install ml_metadata-1.14.0-py3-none-any.whl`:

```
(venv) ml-metadata-remote % pip install ml_metadata-1.14.0-py3-none-any.whl 
Processing ./ml_metadata-1.14.0-py3-none-any.whl
Requirement already satisfied: attrs<22,>=20.3 in ./venv/lib/python3.9/site-packages (from ml-metadata==1.14.0) (21.4.0)
Requirement already satisfied: grpcio<2,>=1.8.6 in ./venv/lib/python3.9/site-packages (from ml-metadata==1.14.0) (1.59.3)
Requirement already satisfied: absl-py<2.0.0,>=0.9 in ./venv/lib/python3.9/site-packages (from ml-metadata==1.14.0) (1.4.0)
Requirement already satisfied: six<2,>=1.10 in ./venv/lib/python3.9/site-packages (from ml-metadata==1.14.0) (1.16.0)
Requirement already satisfied: protobuf<4,>=3.13 in ./venv/lib/python3.9/site-packages (from ml-metadata==1.14.0) (3.20.3)
Installing collected packages: ml-metadata
Successfully installed ml-metadata-1.14.0
```

## References

Inspiration for manual wheel file writing: https://github.com/uranusjr/packaging-the-hard-way
