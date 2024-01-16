""" A simple mock for Boto3's S3 modules. """

import io
import pathlib


class PseudoBotoPaginator:
    def __init__(self, func):
        self.func = func

    def paginate(self, **kwargs):
        yield from self.func(**kwargs)


class PseudoS3Exceptions:
    try:
        from botocore.exceptions import NoSuchKey
    except ImportError:
        class NoSuchKey(BaseException):
            def __init__(self, key):
                self.key = key

            def __repr__(self):
                return f'PseudoNoSuchKey({self.key!r})'

    try:
        from botocore.exceptions import ClientError
    except ImportError:
        class ClientError(BaseException):
            def __init__(self, error_response, operation_name):
                self.response = error_response  # Not error_reponse!
                self.operation_name = operation_name

            def __repr__(self):
                return f'ClientError({repr(str(self))})'

            def __str__(self):
                error_code = self.response['Error']['Code']
                error_message = self.response['Error']['Message']
                return (
                    f'An error occurred ({error_code}) when calling the {self.operation_name} '
                    f'operation: {error_message}')


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

    def __init__(self, *, origin_client=None, init_buckets=None):
        self.origin_client = origin_client

        self.buckets = {}
        if init_buckets:
            for bucket_name in init_buckets:
                self.buckets[bucket_name] = {}

    # non-standard variable names for Boto3 compatibility
    def download_file(self, Bucket, Key, Filename, *, ExtraArgs=None, Callback=None, Config=None):
        bucket = self.buckets[Bucket]
        if Key not in bucket:
            raise self.exceptions.NoSuchKey(Key)
        content = bucket[Key]
        with open(Filename, 'wb') as f:
            f.write(content)

        if Callback:
            Callback(len(content))

    # non-standard variable names for Boto3 compatibility
    def download_fileobj(self, Bucket, Key, Fileobj, *, ExtraArgs=None, Callback=None, Config=None):
        bucket = self.buckets[Bucket]
        storage = getattr(bucket, 'bucket_storage', bucket)
        if Key not in storage:
            raise self.exceptions.NoSuchKey(Key)
        content = storage[Key]
        Fileobj.write(content)

        if Callback:
            Callback(len(content))

    # non-standard variable names for Boto3 compatibility
    def get_object(self, *, Bucket, Key):
        bucket = self.buckets[Bucket]
        if Key not in bucket:
            raise self.exceptions.NoSuchKey(Key)

        content = bucket[Key]
        return {
            'Body': PseudoBotoIO(content),
            'ContentLength': len(content),
        }

    # noqa non-standard variable names from https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.head_object
    def head_object(self, Bucket, Key):
        try:
            bucket = self.buckets[Bucket]
            content = bucket[Key]
        except KeyError as err:
            raise self.exceptions.ClientError(
                error_response={
                    'Error': {
                        'Code': '404',
                        # Real message is only: 'Not Found'
                        'Message': f'Not Found (PseudoS3Client KeyError: {err})'
                    }
                },
                operation_name='HeadObject',
            )

        # File found: return a halfway plausible result ;)
        return {
            'AcceptRanges': 'bytes',
            'ContentLength': len(content),
            'ContentType': 'application/octet-stream',
            'ETag': '"00000000000000000000000000000000"',
            'LastModified': None,
            'Metadata': {},
            'ResponseMetadata': {}
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

        # boto3 closes file objects, see:
        # https://github.com/boto/s3transfer/issues/80
        Fileobj.close()

    # noqa non-standard variable names from https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.upload_file
    def upload_file(self, Filename, Bucket, Key, *, ExtraArgs=None, Callback=None, Config=None):
        contents = pathlib.Path(Filename).read_bytes()
        buf = io.BytesIO(contents)
        self.upload_fileobj(
            Fileobj=buf, Bucket=Bucket, Key=Key, ExtraArgs=ExtraArgs, Callback=Callback,
            Config=Config)

    # noqa non-standard variable names from https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.delete_object
    def delete_object(self, Bucket, Key):
        del self.buckets[Bucket][Key]

    def generate_presigned_url(self, *args, **kwargs):
        return self.origin_client.generate_presigned_url(*args, **kwargs)

    def list_buckets(self):
        return {
            'Buckets': [{'Name': bucket_name} for bucket_name in self.buckets.keys()],
            # Add some "realistic" fake meta data:
            'Owner': {'DisplayName': '', 'ID': 'b36c0000000000000000000000000000000000000000000000000000abcd0005'},
            'ResponseMetadata': {
                'HTTPHeaders': {'x-amz-request-id': 'PseudoS3Client'},
                'HTTPStatusCode': 200,
                'RequestId': 'PseudoS3Client',
            },
        }

    def head_bucket(self, Bucket, ExpectedBucketOwner=None):
        if ExpectedBucketOwner is not None:
            raise NotImplementedError

        if Bucket not in self.buckets:
            raise self.exceptions.NoSuchKey(Bucket)

        return {  # Some "realistic" fake meta data:
            'ResponseMetadata': {
                'HTTPHeaders': {'x-amz-request-id': 'PseudoS3Client'},
                'HTTPStatusCode': 200,
                'RequestId': 'PseudoS3Client',
            }
        }

    def _list_objects_v2(self, Bucket, Prefix=None):
        bucket = self.buckets.get(Bucket, {})
        keys = bucket.keys()
        if Prefix is not None:
            keys = (k for k in keys if k.startswith(Prefix))
        keys = sorted(keys)
        yield {
            'Contents': [{'Key': k, 'Size': len(bucket[k])} for k in keys],
        }

    def get_paginator(self, operation_name):
        assert operation_name == 'list_objects_v2', f'Unsupported operation name {operation_name}'
        return PseudoBotoPaginator(self._list_objects_v2)

    # Non-standard functions, prefixed by "mock_" (can be used in test code, but not main code)
    # or "debug_" (should never be committed)
    def mock_set_content(self, Bucket, Key, content: bytes):
        assert isinstance(content, bytes)
        self.buckets[Bucket][Key] = content

    def mock_get_content(self, Bucket, Key):
        return self.buckets[Bucket][Key]

    def mock_list_files(self, Bucket):
        return sorted(self.buckets[Bucket].keys())

    def debug_long_repr(self, max_string_length=20):
        res = '<MockS3\n'
        for bucket_name, objects in sorted(self.buckets.items()):
            res += f'{bucket_name}\n'
            for key, content in sorted(objects.items()):
                try:
                    content_str = content.decode('utf-8')
                    if len(content_str) > max_string_length:
                        content_repr = repr(content_str[:max_string_length - 3])[:-1] + '...'
                    else:
                        content_repr = repr(content_str)
                except ValueError:
                    # Binary content
                    content_repr = repr(content[:max_string_length])
                    if len(content_repr) > max_string_length:
                        content_repr = content_repr[:max_string_length - 3][:-1] + '...'

                if content == b'':
                    content_repr = ''

                res += f'  {key:20} => [{len(content_repr)} bytes] {content_repr}\n'
        res += '>\n'
        return res

    def debug_print(self):
        print(self.debug_long_repr())


class PseudoBoto3:
    def __init__(self, **kwargs):
        self.client = PseudoS3Client(**kwargs)
