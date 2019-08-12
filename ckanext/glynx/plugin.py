import ckan.plugins as p
import ckan.plugins.toolkit as tk

def status_options():
    try:
        tag_list = tk.get_action('tag_list')
        status_options = tag_list(data_dict={'vocabulary_id': 'status'})
        return status_options
    except tk.ObjectNotFound:
        return None

def use_agreement_options():
    try:
        tag_list = tk.get_action('tag_list')
        use_agreement_options = tag_list(data_dict={'vocabulary_id': 'use_agreement'})
        return use_agreement_options
    except tk.ObjectNotFound:
        return None

class GlynxPlugin(p.SingletonPlugin, tk.DefaultDatasetForm):
    p.implements(p.ITemplateHelpers)
    p.implements(p.IDatasetForm)
    p.implements(p.IConfigurer)

    # Populates Status dropdown with vocabulary created above.
    def get_helpers(self):
        return {
            'status': status_options,
            'use_agreement': use_agreement_options
        }

    def create_package_schema(self):
        schema = super(GlynxPlugin, self).create_package_schema()

        schema.update({
            'status': [
                tk.get_converter('convert_to_tags')('status')
            ],
            'archived_at': [
                tk.get_validator('isodate'),
                tk.get_converter('convert_to_extras')
            ],
            'start_date': [
                tk.get_validator('isodate'),
                tk.get_converter('convert_to_extras')
            ],
            'end_date': [
                tk.get_validator('isodate'),
                tk.get_converter('convert_to_extras')
            ],
            'use_agreement': [
                tk.get_converter('convert_to_tags')('use_agreement')
            ],
            'request_contact_info': [
                tk.get_validator('boolean_validator'),
                tk.get_converter('convert_to_extras')
            ],
            'require_contact_info': [
                tk.get_validator('boolean_validator'),
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
            'archived_at': [
                tk.get_validator('isodate'),
                tk.get_converter('convert_to_extras')
            ],
            'start_date': [
                tk.get_validator('isodate'),
                tk.get_converter('convert_to_extras')
            ],
            'end_date': [
                tk.get_validator('isodate'),
                tk.get_converter('convert_to_extras')
            ],
            'use_agreement': [
                tk.get_converter('convert_to_tags')('use_agreement')
            ],
            'request_contact_info': [
                tk.get_validator('boolean_validator'),
                tk.get_converter('convert_to_extras')
            ],
            'require_contact_info': [
                tk.get_validator('boolean_validator'),
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
            'archived_at': [
                tk.get_validator('isodate'),
                tk.get_converter('convert_from_extras')
            ],
            'start_date': [
                tk.get_validator('isodate'),
                tk.get_converter('convert_from_extras')
            ],
            'end_date': [
                tk.get_validator('isodate'),
                tk.get_converter('convert_from_extras')
            ],
            'use_agreement': [
                tk.get_converter('convert_from_tags')('use_agreement')
            ],
            'request_contact_info': [
                tk.get_validator('boolean_validator'),
                tk.get_converter('convert_from_extras')
            ],
            'require_contact_info': [
                tk.get_validator('boolean_validator'),
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
