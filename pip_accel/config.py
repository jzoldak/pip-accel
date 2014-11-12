# Configuration defaults for the pip accelerator.
#
# Author: Peter Odding <peter.odding@paylogic.eu>
# Last Change: June 26, 2014
# URL: https://github.com/paylogic/pip-accel

# Standard library modules.
import os
import os.path
# from nose.tools import set_trace
# Modules included in our package.
from pip_accel.utils import expand_user

class Config(object):
    """
    Initialize a configuration object.

    This will set up the values for:
        download_cache
        pip_accel_cache

        source_index
        binary_index
        index_version_file

        s3_cache_bucket
        s3_cache_prefix
    """
    def __init__(self, **kw):
        # Select the default location of the download cache and other files based on
        # the user running the pip-accel command (root goes to /var/cache/pip-accel,
        # otherwise ~/.pip-accel).
        self.s3_cache_bucket = None
        self.s3_cache_prefix = None

        if os.getuid() == 0:
            self.download_cache = '/root/.pip/download-cache'
            self.pip_accel_cache = '/var/cache/pip-accel'
        else:
            self.download_cache = expand_user('~/.pip/download-cache')
            self.pip_accel_cache = expand_user('~/.pip-accel')

        # Enable overriding the default locations with environment variables.
        if 'PIP_S3_CACHE_BUCKET' in os.environ:
            self.s3_cache_bucket = os.environ['PIP_S3_CACHE_BUCKET']
            self.s3_cache_prefix = os.environ.get('PIP_S3_CACHE_PREFIX', '')
        if 'PIP_DOWNLOAD_CACHE' in os.environ:
            self.download_cache = expand_user(os.environ['PIP_DOWNLOAD_CACHE'])
        if 'PIP_ACCEL_CACHE' in os.environ:
            self.pip_accel_cache = expand_user(os.environ['PIP_ACCEL_CACHE'])

        # Generate the absolute pathnames of the source/binary caches.
        self.source_index = os.path.join(self.pip_accel_cache, 'sources')
        self.binary_index = os.path.join(self.pip_accel_cache, 'binaries')
        self.index_version_file = os.path.join(self.pip_accel_cache, 'version.txt')
