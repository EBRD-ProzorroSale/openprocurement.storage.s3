from boto.s3.connection import S3Connection, OrdinaryCallingFormat
from openprocurement.storage.s3.storage import S3Storage


def includeme(config):
    settings = config.registry.settings
    s3_settings = {
        'is_secure': True
    }
    if 's3.access_key' in settings and 's3.secret_key' in settings and 's3.bucket' in settings:
        # S3 connection
        for k, v in settings.items():
            if k[:3] != 's3.':
                continue
            key = k[3:]
            if key == 'secret_key':
                s3_settings['aws_secret_access_key'] = v
            elif key == 'access_key':
                s3_settings['aws_access_key_id'] = v
            elif key == 'port':
                s3_settings[key] = int(v)
            elif key == 'bucket':
                pass
            else:
                s3_settings[key] = v

        if 's3.is_secure' in settings and not settings['s3.is_secure']:
            s3_settings['is_secure'] = False
        s3_settings['calling_format'] = OrdinaryCallingFormat()
        connection = S3Connection(**s3_settings)
        bucket_name = settings['s3.bucket']

        buckets_name = [b.name for b in connection.get_all_buckets()]
        if bucket_name not in buckets_name:
            connection.create_bucket(bucket_name)

        config.registry.storage = S3Storage(connection, bucket_name)
    else:
        raise
