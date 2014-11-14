#!/usr/bin/env python

# Tests for the pip accelerator.
#
# Author: Peter Odding <peter.odding@paylogic.eu>
# Last Change: November 9, 2014
# URL: https://github.com/paylogic/pip-accel
#
# TODO Test successful installation of iPython, because it used to break! (nested /lib/ directory)

# Standard library modules.
import logging
import os
import pipes
import shutil
import sys
import tempfile
import unittest

# External dependency.
import coloredlogs

# Initialize a logger for this module.
logger = logging.getLogger(__name__)

class PipAccelTestCase(unittest.TestCase):

    def setUp(self):
        """
        Create a temporary working directory and a virtual environment where
        pip-accel can be tested in isolation (starting with an empty download
        cache, source index and binary index and no installed modules) and make
        sure pip and pip-accel use the directory. Also creates the directories
        for the download cache, the source index and the binary index (normally
        this is done from pip_accel.main).
        """
        coloredlogs.install(level=logging.DEBUG)
        # Create a temporary working directory.
        self.working_directory = tempfile.mkdtemp()
        # Create a temporary build directory.
        self.build_directory = os.path.join(self.working_directory, 'build')
        # Create a temporary virtual environment.
        self.virtual_environment = os.path.join(self.working_directory, 'environment')
        python = 'python%i.%i' % (sys.version_info[0], sys.version_info[1])
        assert os.system('virtualenv --python=%s %s' % (pipes.quote(python), pipes.quote(self.virtual_environment))) == 0
        # Make sure pip-accel uses the pip in the temporary virtual environment.
        os.environ['PATH'] = '%s:%s' % (os.path.join(self.virtual_environment, 'bin'), os.environ['PATH'])
        os.environ['VIRTUAL_ENV'] = self.virtual_environment
        # Make pip and pip-accel use the temporary working directory.
        os.environ['PIP_DOWNLOAD_CACHE'] = os.path.join(self.working_directory, 'download-cache')
        os.environ['PIP_ACCEL_CACHE'] = self.working_directory
        # Initialize the required subdirectories.
        self.pip_accel = __import__('pip_accel')
        self.pip_accel.initialize_directories()

    def runTest(self):
        """
        A very basic test of the functions that make up the pip-accel command
        using the `virtualenv` package as a test case.
        """
        # We will test the downloading, conversion to binary distribution and
        # installation of the virtualenv package (we simply need a package we
        # know is available from PyPI).
        arguments = ['install', '--ignore-installed', 'virtualenv==1.8.4']
        # First we do a simple sanity check.
        from pip.exceptions import DistributionNotFound
        try:
            requirements = self.pip_accel.unpack_source_dists(arguments, build_directory=self.build_directory)
            # This line should never be reached.
            self.assertTrue(False)
        except Exception as e:
            self.assertTrue(isinstance(e, DistributionNotFound))
        # Download the source distribution from PyPI.
        self.pip_accel.download_source_dists(arguments, self.build_directory)
        # Implicitly verify that the download was successful.
        requirements = self.pip_accel.unpack_source_dists(arguments, build_directory=self.build_directory)
        # self.assertIsInstance(requirements, list)
        self.assertTrue(isinstance(requirements, list))
        self.assertEqual(len(requirements), 1)
        self.assertEqual(requirements[0][0], 'virtualenv')
        self.assertEqual(requirements[0][1], '1.8.4')
        self.assertTrue(os.path.isdir(requirements[0][2]))
        # Test the build and installation of the binary package. We have to
        # pass "install_prefix" explicitly here because the Python process
        # running this test is not inside the virtual environment created to
        # run the tests...
        self.pip_accel.install_requirements(requirements,
                                            cache=self.pip_accel.caches.CacheManager(),
                                            install_prefix=self.virtual_environment)
        # Check that the virtualenv command was installed.
        self.assertTrue(os.path.isfile(os.path.join(self.virtual_environment, 'bin', 'virtualenv')))
        # Check that the virtualenv command can be executed successfully.
        logger.debug("Checking that `virtualenv' command works ..")
        command = '%s --help' % pipes.quote(os.path.join(self.virtual_environment, 'bin', 'virtualenv'))
        self.assertEqual(os.system(command), 0)

    def tearDown(self):
        """
        Cleanup the temporary working directory that was used during the test.
        """
        shutil.rmtree(self.working_directory)

if __name__ == '__main__':
    unittest.main()
