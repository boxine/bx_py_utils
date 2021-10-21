""" A simple mock for Boto3's S3 modules. """

import io
import pathlib


class PseudoBotoPaginator:
    def __init__(self, func):
        self.func = func

    def paginate(self, **kwargs):
        yield from self.func(**kwargs)


class PseudoS3Exceptions:
    class NoSuchKey(BaseException):
        def __init__(self, key):
            self.key = key

        def __repr__(self):
            return f'PseudoNoSuchKey({self.key!r})'


class PseudoBotoIO:
    # boto3's object file handle is EXTREMELY restricted. Simulate that.
    def __init__(self, content: bytes):
        assert isinstance(content, bytes)
        self._io = io.BytesIO(content)

    def read(self, *args, **kwargs):
        return self._io.read(*args, **kwargs)

    def close(self):
        return self._io.close()

    # No other properties!


class PseudoS3Client:
    """ Simulates a boto3 S3 client object in tests """

    exceptions = PseudoS3Exceptions

    def __init__(self, *, origin_client=None, init_buckets=[]):
        self.origin_client = origin_client

        self.buckets = {}
        for bucket_name in init_buckets:
            self.buckets[bucket_name] = {}

    def download_file(self, bucket, s3_key, local_file):
        bucket = self.buckets[bucket]
        storage = getattr(bucket, 'bucket_storage', bucket)
        if s3_key not in storage:
            raise self.exceptions.NoSuchKey(s3_key)
        with open(local_file, 'wb') as f:
            f.write(storage[s3_key])

    # non-standard variable names for Boto3 compatibility
    def get_object(self, *, Bucket, Key):
        storage = self.buckets[Bucket]
        if Key not in storage:
            raise self.exceptions.NoSuchKey(Key)

        content = storage[Key]
        return {
            'Body': PseudoBotoIO(content),
            'ContentLength': len(content),
        }

    # noqa non-standard variable names from https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.upload_fileobj
    def upload_fileobj(self, Fileobj, Bucket, Key, *, ExtraArgs=None, Callback=None, Config=None):
        if Callback:
            Callback(0)
            Callback(1)
        bucket = self.buckets[Bucket]
        contents = Fileobj.read()
        assert isinstance(bucket, dict)
        bucket[Key] = contents
        if Callback:
            Callback(len(contents))

    # noqa non-standard variable names from https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.upload_file
    def upload_file(self, Filename, Bucket, Key, *, ExtraArgs=None, Callback=None, Config=None):
        contents = pathlib.Path(Filename).read_bytes()
        buf = io.BytesIO(contents)
        self.upload_fileobj(
            Fileobj=buf, Bucket=Bucket, Key=Key, ExtraArgs=ExtraArgs, Callback=Callback,
            Config=Config)

    def mock_set_content(self, Bucket, Key, content: bytes):
        assert isinstance(content, bytes)
        self.buckets[Bucket][Key] = content

    # noqa non-standard variable names from https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.delete_object
    def delete_object(self, Bucket, Key):
        del self.buckets[Bucket][Key]

    def generate_presigned_url(self, *args, **kwargs):
        return self.origin_client.generate_presigned_url(*args, **kwargs)

    def _list_objects_v2(self, Bucket, Prefix=None):
        bucket = self.buckets.get(Bucket, {})
        keys = bucket.keys()
        if Prefix is not None:
            keys = (k for k in keys if k.startswith(Prefix))
        yield {
            'Contents': [{'Key': k, 'Size': len(bucket[k])} for k in keys],
        }

    def get_paginator(self, operation_name):
        assert operation_name == 'list_objects_v2', f'Unsupported operation name {operation_name}'
        return PseudoBotoPaginator(self._list_objects_v2)


class PseudoBoto3:
    def __init__(self, **kwargs):
        self.client = PseudoS3Client(**kwargs)
