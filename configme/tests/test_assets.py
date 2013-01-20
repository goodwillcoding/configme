# -*- coding: utf-8 -*-

"""
Test asset management.
"""

from unittest import TestCase

from ..compat import StringIO

from ..exceptions import AssetCreationError
from ..exceptions import AssetLocationTaken
from ..exceptions import LocationCreationError
from ..exceptions import LocationNotFound
from ..exceptions import LocationRemovalError


# --------------------------------------------------------------------------- #
class DummyEnvironmentError(EnvironmentError):
    # subclass from EnvironmentError since the can not be initted
    errno = None
    strerror = None
    filename = None

    def __init__(self, errno, strerror, filename):
        self.errno = errno
        self.strerror = strerror
        self.filename = filename


# --------------------------------------------------------------------------- #
class Test_AssetManager(TestCase):

    # ....................................................................... #
    def _makeOne(self, *args, **kwargs):
        from ..assets import AssetManager
        return AssetManager(*args, **kwargs)

    # ....................................................................... #
    def test_location(self):

        test_location = 'test_location'

        def dummy_os_path_isdir(path):
            return True

        asset_manager = self._makeOne()

        self.assertEqual(
            asset_manager.location(
                test_location, 'some_subject',
                _os_path_isdir=dummy_os_path_isdir),
            test_location)

    # ....................................................................... #
    def test_location_for_exceptions(self):

        test_location = 'test_location'
        test_subject = 'test_subject'

        def dummy_os_path_isdir(path):
            return False

        desired_error_message = "%s does not exist, is not a folder, or is " \
            "not accessible: %s" \
            % (test_subject.capitalize(), test_location)

        asset_manager = self._makeOne()

        self.assertRaisesRegexp(
            LocationNotFound,
            desired_error_message,
            asset_manager.location,
            test_location,
            test_subject,
            _os_path_isdir=dummy_os_path_isdir)

    # ....................................................................... #
    def test_path_join(self):

        test_path_parts = ('test', 'path', 'parts')

        def dummy_os_path_join(*path_parts):
            return '/'.join(path_parts)

        desired_result = 'test/path/parts'

        asset_manager = self._makeOne()

        self.assertEqual(
            asset_manager.path_join(
                test_path_parts,
                _os_path_join=dummy_os_path_join),
            desired_result)

    # ....................................................................... #
    def test_path_filename(self):

        test_filename = 'test_filename'
        test_path = 'test_path_folder/%s' % test_filename

        def dummy_os_path_basename(path):
            return path.split('/')[-1]

        desired_result = test_filename

        asset_manager = self._makeOne()

        self.assertEqual(
            asset_manager.path_filename(
                test_path,
                _os_path_basename=dummy_os_path_basename),
            desired_result)

    # ....................................................................... #
    def test_path_folder(self):

        test_folder = 'test_folder_part1/test_folder_part2'
        test_path = '%s/some_filename' % test_folder

        def dummy_os_path_dirname(path):
            return '/'.join(path.split('/')[:-1])

        desired_result = test_folder

        asset_manager = self._makeOne()

        self.assertEqual(
            asset_manager.path_folder(
                test_path,
                _os_path_dirname=dummy_os_path_dirname),
            desired_result)

    # ....................................................................... #
    def test_asset_or_location_exists(self):

        test_path = 'test_path'

        def dummy_os_path_isfile(path):
            return False

        asset_manager = self._makeOne()

        self.assertEqual(
            asset_manager.asset_or_location_exists(
                test_path,
                _os_path_isfile=dummy_os_path_isfile),
            test_path)

    # ....................................................................... #
    def test_asset_or_location_exists_for_exceptions(self):

        test_path = 'test_path'

        def dummy_os_path_isfile(path):
            return True

        desired_error_message = "Asset or Location already exist: %s" \
            % test_path

        asset_manager = self._makeOne()

        self.assertRaisesRegexp(
            AssetLocationTaken,
            desired_error_message,
            asset_manager.asset_or_location_exists,
            test_path,
            _os_path_isfile=dummy_os_path_isfile,
            )

    # ....................................................................... #
    def test_remove_folder_if_exists(self):

        test_folder_path = 'test_folder_path'

        def dummy_os_path_isdir(path):
            return True

        def dummy_shutil_rmtree(path):
            pass

        asset_manager = self._makeOne()

        self.assertEqual(
            asset_manager.remove_folder(
                folder_path=test_folder_path,
                _os_path_isdir=dummy_os_path_isdir,
                _shutil_rmtree=dummy_shutil_rmtree),
            test_folder_path)

    # ....................................................................... #
    def test_remove_folder_if_doesnot_exists(self):

        test_folder_path = 'test_folder_path'

        def dummy_os_path_isdir(path):
            return False

        asset_manager = self._makeOne()

        self.assertEqual(
            asset_manager.remove_folder(
                folder_path=test_folder_path,
                _os_path_isdir=dummy_os_path_isdir),
            test_folder_path)

    # ....................................................................... #
    def test_remove_folder_for_exceptions(self):

        test_folder_path = 'test_folder_path'
        test_errno = 10
        test_strerror = 'test_strerror'

        def dummy_os_path_isdir(path):
            return True

        def dummy_shutil_rmtree(path):
            raise DummyEnvironmentError(
                errno=test_errno,
                strerror=test_strerror,
                filename=test_folder_path)

        desired_error_message = "\[Errno %d\] %s: '%s'" \
            % (test_errno, test_strerror, test_folder_path)

        asset_manager = self._makeOne()

        self.assertRaisesRegexp(
            LocationRemovalError,
            desired_error_message,
            asset_manager.remove_folder,
            test_folder_path,
            _os_path_isdir=dummy_os_path_isdir,
            _shutil_rmtree=dummy_shutil_rmtree)

    # ....................................................................... #
    def test_create_folder(self):

        test_folder_path = 'test_folder_path'

        def dummy_os_makedirs(folder_path):
            pass

        asset_manager = self._makeOne()

        self.assertEqual(
            asset_manager.create_folder(
                test_folder_path,
                _os_makedirs=dummy_os_makedirs),
            test_folder_path)

    # ....................................................................... #
    def test_create_folder_for_exceptions(self):

        test_folder_path = 'test_folder_path'
        test_errno = 10
        test_strerror = 'test_strerror'

        def dummy_os_makedirs(folder_path):
            raise DummyEnvironmentError(errno=test_errno,
                                        strerror=test_strerror,
                                        filename=test_folder_path)

        desired_error_message = "\[Errno %d\] %s: '%s'" \
            % (test_errno, test_strerror, test_folder_path)

        asset_manager = self._makeOne()

        self.assertRaisesRegexp(
            LocationCreationError,
            desired_error_message,
            asset_manager.create_folder,
            test_folder_path,
            _os_makedirs=dummy_os_makedirs)

    # ....................................................................... #
    def test_write_to_file(self):

        test_file_path = 'test_file_path'
        test_content = 'test_content'

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        class DummyFileStream(object):

            file_path = None
            closed = False

            _stream = None
            _written_stream = None

            def __init__(self):
                self._stream = StringIO()

            def __call__(self, file_path, mode):
                self.file_path = file_path
                return self

            def write(self, content):
                self._stream.write(content)

            def close(self):
                self._written_stream = self._stream.getvalue()
                self.closed = True
                self._stream.close()

            def getvalue(self):
                return self._written_stream

        dummy_file_stream = DummyFileStream()
        dummy_io_open = dummy_file_stream

        asset_manager = self._makeOne()

        # call FUT
        self.assertEqual(
            asset_manager.write_to_file(
                file_path=test_file_path,
                content=test_content,
                _io_open=dummy_io_open),
            test_file_path)

        # test that the file path of the file that has been written to
        self.assertEqual(dummy_file_stream.file_path, test_file_path)
        # test that the content is written to file
        self.assertEqual(dummy_file_stream.getvalue(), test_content)
        # test the file has been closed
        self.assertTrue(dummy_file_stream.closed)

    # ....................................................................... #
    def test_write_to_file_for_exceptions(self):

        test_file_path = 'test_file_path'
        test_errno = 10
        test_strerror = 'test_strerror'

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        def dummy_io_open(path, content):
            raise DummyEnvironmentError(
                errno=test_errno,
                strerror=test_strerror,
                filename=test_file_path)

        desired_error_message = "\[Errno %d\] %s: '%s'" \
            % (test_errno, test_strerror, test_file_path)

        asset_manager = self._makeOne()

        self.assertRaisesRegexp(
            AssetCreationError,
            desired_error_message,
            asset_manager.write_to_file,
            test_file_path,
            'some_content',
            _io_open=dummy_io_open)
