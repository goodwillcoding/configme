# -*- coding: utf-8 -*-

"""
Test asset management.
"""

from unittest import TestCase


from ..exceptions import LocationNotFound
from ..exceptions import LocationRemovalError
from ..exceptions import LocationCreationError


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
            asset_manager.location(test_location, 'some_subject',
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
            asset_manager.path_join(test_path_parts,
                                    _os_path_join=dummy_os_path_join),
            desired_result)

    # ....................................................................... #
    def test_remove_folder_if_exists(self):

        test_folder_path = 'test_folder_path'

        def dummy_os_path_isdir(path):
            return True

        def dummy_shutil_rmtree(path):
            pass

        asset_manager = self._makeOne()

        self.assertEqual(
            asset_manager.remove_folder(folder_path=test_folder_path,
                                        _os_path_isdir=dummy_os_path_isdir,
                                        _shutil_rmtree=dummy_shutil_rmtree),
            test_folder_path)

    # ....................................................................... #
    def test_remove_folder_if_doesnot_exists(self):

        test_folder_path = 'test_folder_path'

        def dummy_os_path_isdir(path):
            return False

        def dummy_shutil_rmtree(path):  # pragma: no cover
            pass

        asset_manager = self._makeOne()

        self.assertEqual(
            asset_manager.remove_folder(folder_path=test_folder_path,
                                        _os_path_isdir=dummy_os_path_isdir,
                                        _shutil_rmtree=dummy_shutil_rmtree),
            test_folder_path)

    # ....................................................................... #
    def test_remove_folder_for_exceptions(self):

        test_folder_path = 'test_folder_path'
        test_errno = 10
        test_strerror = 'test_strerror'

        def dummy_os_path_isdir(path):
            return True

        def dummy_shutil_rmtree(path):
            raise DummyEnvironmentError(errno=test_errno,
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

        def dummy_os_makedirs(folder_path):  # pragma: no cover
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
