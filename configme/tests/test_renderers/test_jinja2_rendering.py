# -*- coding: utf-8 -*-

"""
Test Jinja2 Template Renderer
"""

from unittest import TestCase

from jinja2 import TemplateError

from ...exceptions import TemplateRenderError


# --------------------------------------------------------------------------- #
class DummyConfig(object):

    templates_path = None

    # ....................................................................... #
    def __init__(self, templates_path, *args, **kwargs):
        self.templates_path = templates_path


# --------------------------------------------------------------------------- #
class DummyFileSystemLoader(object):

    searchpath = None

    # ....................................................................... #
    def __init__(self, searchpath):
        self.searchpath = searchpath


# --------------------------------------------------------------------------- #
class Test_Jinja2TemplateRenderer(TestCase):

    # ....................................................................... #
    def _makeOne(self, *args, **kwargs):
        from ...renderers.jinja2_rendering import Jinja2TemplateRenderer
        return Jinja2TemplateRenderer(*args, **kwargs)

    # ....................................................................... #
    def test_initted_properties(self):

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        class DummyEnvironment(object):

            loader = None

            def __init__(self, loader):
                self.loader = loader

        test_templates_path = 'test_templates_path'
        test_config = DummyConfig(templates_path=test_templates_path)
        test_role_output_path = 'test_role_output_path'
        test_path = 'test_path'
        test_settings = {'test_settings_key': 'test_settings_value'}

        jinja2_template_renderer = self._makeOne(
            config=test_config,
            role_output_folder_path=test_role_output_path,
            path=test_path,
            settings=test_settings,
            _jinja2_filesystem_loader_factory=DummyFileSystemLoader,
            _jinja2_environment_factory=DummyEnvironment)

        self.assertIs(jinja2_template_renderer.config, test_config)
        self.assertEqual(jinja2_template_renderer.path, test_path)
        self.assertDictEqual(jinja2_template_renderer.settings, test_settings)

        # test for jinja2 environment
        self.assertIsInstance(
            jinja2_template_renderer.jinja2_env,
            DummyEnvironment)

        # loader in the jinja2 environment
        self.assertIsInstance(
            jinja2_template_renderer.jinja2_env.loader,
            DummyFileSystemLoader)

        # test for searchpath
        self.assertEqual(
            jinja2_template_renderer.jinja2_env.loader.searchpath,
            test_templates_path)

    # ....................................................................... #
    def test_get_rendered_config(self):

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        class DummyJinja2Template(object):

            def render(self, **settings):
                temp = ['%s: %s' % (str(k), str(v)) for
                    k, v in settings.items()]
                temp.sort()
                return ','.join(temp)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        class DummyEnvironment(object):

            loader = None

            def __init__(self, loader):
                self.loader = loader

            def get_template(self, path):
                return DummyJinja2Template()

        test_templates_path = 'test_templates_path'
        test_config = DummyConfig(templates_path=test_templates_path)
        test_role_output_path = 'test_role_output_path'
        test_path = 'test_path'
        test_settings = {
            'test_settings_key1': 'test_settings_value1',
            'test_settings_key2': 'test_settings_value2',
            }

        desired_rendered_response = \
            'test_settings_key1: test_settings_value1,' \
            'test_settings_key2: test_settings_value2'

        jinja2_template_renderer = self._makeOne(
            config=test_config,
            role_output_folder_path=test_role_output_path,
            path=test_path,
            settings=test_settings,
            _jinja2_filesystem_loader_factory=DummyFileSystemLoader,
            _jinja2_environment_factory=DummyEnvironment)

        self.assertEqual(
            jinja2_template_renderer.get_rendered_config(),
            desired_rendered_response)

    # ....................................................................... #
    def test_get_rendered_config_for_exceptions(self):

        config = DummyConfig(templates_path='some_templates_path')
        test_path = 'test_path'
        test_error_message = 'test_error_message'

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        class DummyEnvironment(object):

            loader = None

            def __init__(self, loader):
                self.loader = loader

            def get_template(self, path):
                raise TemplateError(test_error_message)

        desired_error_message = 'Failed to render config template: %s\n\n%s' \
                % (test_path, test_error_message)

        jinja2_template_renderer = self._makeOne(
            config=config,
            role_output_folder_path='some_role_output_path',
            path=test_path,
            settings={},
            _jinja2_filesystem_loader_factory=DummyFileSystemLoader,
            _jinja2_environment_factory=DummyEnvironment)

        self.assertRaisesRegexp(
            TemplateRenderError,
            desired_error_message,
            jinja2_template_renderer.get_rendered_config
            )
