import ckan.plugins as p
import ckan.plugins.toolkit as tk

# Vocabulary for custom Status dropdown is created here.
def create_status_options():
    user = tk.get_action('get_site_user')({'ignore_auth': True}, {})
    context = {'user': user['name']}
    try:
        data = {'id': 'status_options'}
        tk.get_action('vocabulary_show')(context, data)
    except tk.ObjectNotFound:
        data = {'name': 'status_options'}
        vocab = tk.get_action('vocabulary_create')(context, data)
        for tag in (u'Complete', u'In Progress', u'To Do'):
            data = {'name': tag, 'vocabulary_id': vocab['id']}
            tk.get_action('tag_create')(context, data)

def status_options():
    create_status_options()
    try:
        tag_list = tk.get_action('tag_list')
        status_options = tag_list(data_dict={'vocabulary_id': 'status_options'})
        return status_options
    except tk.ObjectNotFound:
        return None

class GlynxPlugin(p.SingletonPlugin, tk.DefaultDatasetForm):
    p.implements(p.ITemplateHelpers)
    p.implements(p.IDatasetForm)
    p.implements(p.IConfigurer)

    # Populates Status dropdown with vocabulary created above.
    def get_helpers(self):
        return {'status_options': status_options}

    def create_package_schema(self):
        schema = super(GlynxPlugin, self).create_package_schema()

        # Custom "Status" (dropdown) field.
        schema.update({
            'status': [
                tk.get_converter('convert_to_tags')('status_options')
            ]
        })

        # Custom "Archived at" (date) field.
        schema.update({
            'archived_at': [
                tk.get_validator('isodate'),
                tk.get_converter('convert_to_extras')
            ]
        })

        # Custom "Request Contact Info" (boolean) field.
        schema.update({
            'request_contact_info': [
                tk.get_validator('boolean_validator'),
                tk.get_converter('convert_to_extras')
            ]
        })

        return schema

    def update_package_schema(self):
        schema = super(GlynxPlugin, self).update_package_schema()

        # Custom "Status" (dropdown) field.
        schema.update({
            'status': [
                tk.get_converter('convert_to_tags')('status_options')
            ]
        })

        # Custom "Archived at" (date) field.
        schema.update({
            'archived_at': [
                tk.get_validator('isodate'),
                tk.get_converter('convert_to_extras')
            ]
        })

        # Custom "Request Contact Info" (boolean) field.
        schema.update({
            'request_contact_info': [
                tk.get_validator('boolean_validator'),
                tk.get_converter('convert_to_extras')
            ]
        })

        return schema

    def show_package_schema(self):
        schema = super(GlynxPlugin, self).show_package_schema()
        schema['tags']['__extras'].append(tk.get_converter('free_tags_only'))

        # Custom "Status" (dropdown) field.
        schema.update({
            'status': [
                tk.get_converter('convert_from_tags')('status_options')
            ]
        })

        # Custom "Archived at" (date) field.
        schema.update({
            'archived_at': [
                tk.get_validator('isodate'),
                tk.get_converter('convert_from_extras')
            ]
        })

        # Custom "Request Contact Info" (boolean) field.
        schema.update({
            'request_contact_info': [
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
