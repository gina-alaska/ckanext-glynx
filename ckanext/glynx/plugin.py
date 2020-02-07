# This code was adapted from the "adding custom fields" guide:
# https://docs.ckan.org/en/2.8/extensions/adding-custom-fields.html

import ckan.plugins as p
import ckan.plugins.toolkit as tk
import os
import json

# Read iso_topic_categories.json, store in variable for later.
# iso_topics_file = os.path.dirname(__file__) + '/iso_topic_categories.json'
# with open(iso_topics_file) as iso_topics_handle:
#     iso_topic_items = json.load(iso_topics_handle)['iso_topic_categories']


# Helper function that gets called in templates as h.iso_topic_categories().
# def iso_topic_categories():
#     return iso_topic_items


# Custom validator to make sure the iso_topic_category key provided through the
# edit form or API is present in the list of keys read from JSON file.
# def iso_topic_category_validator(value, context):
#     if value not in list(iso_topic_items.keys()):
#         raise tk.Invalid('Invalid Iso Topic Category value: {}'.format(value))
#     return value


class GlynxPlugin(p.SingletonPlugin, tk.DefaultDatasetForm):
    p.implements(p.ITemplateHelpers)
    p.implements(p.IDatasetForm)
    p.implements(p.IConfigurer)
    p.implements(p.IPackageController, inherit=True)

    # IPackageController
    # Change the default search sort to ascending
    def before_search(self, data_dict):
        if not data_dict.get('sort'):
            data_dict['sort'] = 'title_string asc'
        return data_dict

    # Change the sort index to be case insensitive
    def before_index(self, pkg_dict):
        title = pkg_dict['title']
        if title:
            pkg_dict['title_string'] = title.lower()
        
        return pkg_dict

    def get_helpers(self):
        return {
        #         'iso_topic_categories': iso_topic_categories
        }

    # Custom field support for package creation.
    #def create_package_schema(self):
    #    schema = super(GlynxPlugin, self).create_package_schema()

    #    schema.update({
    #        # 'iso_topic_category': [
    #        #     iso_topic_category_validator,
    #        #     tk.get_converter('convert_to_extras')
    #        # ],
    #        'archived_at': [
    #            # tk.get_validator('isodate'),
    #            tk.get_converter('convert_to_extras')
    #        ]
    #    })

    #    return schema

    # Custom field support for package updates.
    #def update_package_schema(self):
    #    schema = super(GlynxPlugin, self).update_package_schema()

    #    schema.update({
    #        # 'iso_topic_category': [
    #        #     iso_topic_category_validator,
    #        #     tk.get_converter('convert_to_extras')
    #        # ],
    #        'archived_at': [
    #            # tk.get_validator('isodate'),
    #            tk.get_converter('convert_to_extras')
    #        ]
    #    })

    #    return schema

    # Custom field support for package display.
    #def show_package_schema(self):
    #    schema = super(GlynxPlugin, self).show_package_schema()

    #    schema.update({
    #        # 'iso_topic_category': [
    #        #     iso_topic_category_validator,
    #        #     tk.get_converter('convert_from_extras')
    #        # ],
    #        'archived_at': [
    #            # tk.get_validator('isodate'),
    #            tk.get_converter('convert_from_extras')
    #        ]
    #    })

    #    return schema

    def is_fallback(self):
        # Return True to register this plugin as the default handler for
        # package types not handled by any other IDatasetForm plugin.
        return True

    def package_types(self):
        # This plugin doesn't handle any special package types, it just
        # registers itself as the default (above).
        return []

    def update_config(self, config):
        # Add this plugin's templates dir to CKAN's extra_template_paths, so
        # that CKAN will use this plugin's custom templates.
        tk.add_template_directory(config, 'templates')

