"""
Test the config module
"""
import unittest
import os
from mock import patch
from nose.tools import assert_equal, set_trace



class ConfigTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_s3_cache_defaults(self):
        self.environ = {}
        self.environ_patch = patch('os.environ', self.environ)
        self.environ_patch.start()
        set_trace()
        print os.environ
        from pip_accel.config import s3_cache_bucket, s3_cache_prefix
        print os.environ

        assert_equal(s3_cache_bucket, None)
        assert_equal(s3_cache_prefix, None)


    def test_s3_cache_bucket_override(self):
        self.environ = {'PIP_S3_CACHE_BUCKET': 'foo'}
        self.environ_patch = patch('os.environ', self.environ)
        self.environ_patch.start()
        from pip_accel.config import s3_cache_bucket, s3_cache_prefix

        assert_equal(s3_cache_bucket, 'foo')
        assert_equal(s3_cache_prefix, '')

    @unittest.skip('fix this one')
    @patch.dict(os.environ, {'PIP_S3_CACHE_BUCKET': 'foo', 'PIP_S3_CACHE_PREFIX': 'bar'})
    def test_s3_cache_prefix_override(self):
        from pip_accel.config import s3_cache_bucket, s3_cache_prefix

        assert_equal(s3_cache_bucket, 'foo')
        assert_equal(s3_cache_prefix, 'bar')

