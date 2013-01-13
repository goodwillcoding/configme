# -*- coding: utf-8 -*-

"""
Test Template Renderer-
"""

from unittest import TestCase


# --------------------------------------------------------------------------- #
class DummyConfig(object):
    pass


# --------------------------------------------------------------------------- #
# class Test_BaseTemplateRender(TestCase):

#     # ....................................................................... #
#     def _makeOne(self, *args, **kwargs):
#         from ..template_renderer import BaseTemplateRenderer
#         return BaseTemplateRenderer(*args, **kwargs)

#     # ....................................................................... #
#     def test_init_and_check_required_initted_properties(self):

#         test_config = DummyConfig()
#         test_role_output_folder_path = 'test_role_output_folder_path'
#         test_path = 'test_path'
#         test_settings = {'test_settings_key': 'test_settings_value'}

#         template_renderer = self._makeOne(
#             config=test_config,
#             role_output_folder_path=test_role_output_folder_path,
#             path=test_path,
#             settings=test_settings)

#         self.assertIs(template_renderer.config, test_config)
#         self.assertEqual(template_renderer.role_output_folder_path,
#                          test_role_output_folder_path)
#         self.assertEqual(template_renderer.path, test_path)
#         self.assertEqual(template_renderer.path, test_path)
