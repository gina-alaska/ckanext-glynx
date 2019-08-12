import ckan.plugins as p
import ckan.plugins.toolkit as tk
import os
import json

iso_topics_file = os.path.dirname(__file__) + '/iso_topic_categories.json'
with open(iso_topics_file) as iso_topics_handle:
    iso_topic_items = json.load(iso_topics_handle)['iso_topic_categories']

def iso_topic_categories():
    return iso_topic_items

statuses_file = os.path.dirname(__file__) + '/statuses.json'
with open(statuses_file) as statuses_handle:
    status_items = json.load(statuses_handle)['statuses']

def statuses():
    return status_items

class GlynxPlugin(p.SingletonPlugin, tk.DefaultDatasetForm):
    p.implements(p.ITemplateHelpers)
    p.implements(p.IDatasetForm)
    p.implements(p.IConfigurer)

    def get_helpers(self):
        return {
            'statuses': statuses,
            'iso_topic_categories': iso_topic_categories
        }

    def create_package_schema(self):
        schema = super(GlynxPlugin, self).create_package_schema()

        schema.update({
            'status': [
                tk.get_converter('convert_to_tags')('status')
            ],
            'iso_topic_category': [
                tk.get_converter('convert_to_tags')('iso_topic_category')
            ],
            'archived_at': [
                tk.get_validator('isodate'),
                tk.get_converter('convert_to_extras')
            ]
        })

        return schema

    def update_package_schema(self):
        schema = super(GlynxPlugin, self).update_package_schema()

        schema.update({
            'status': [
                tk.get_converter('convert_to_tags')('status')
            ],
            'iso_topic_category': [
                tk.get_converter('convert_to_tags')('iso_topic_category')
            ],
            'archived_at': [
                tk.get_validator('isodate'),
                tk.get_converter('convert_to_extras')
            ]
        })

        return schema

    def show_package_schema(self):
        schema = super(GlynxPlugin, self).show_package_schema()
        schema['tags']['__extras'].append(tk.get_converter('free_tags_only'))

        schema.update({
            'status': [
                tk.get_converter('convert_from_tags')('status')
            ],
            'iso_topic_category': [
                tk.get_converter('convert_from_tags')('iso_topic_category')
            ],
            'archived_at': [
                tk.get_validator('isodate'),
                tk.get_converter('convert_from_extras')
            ]
        })

        return schema

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
