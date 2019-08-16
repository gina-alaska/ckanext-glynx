ckanext-glynx
=============

Extend CKAN with custom fields, vocabularies, and tags migrated from GLynx.

Setup
-----

The ckanext-glynx extension requires the ckanext-spatial extension. Install the ckanext-spatial extension using this documentation:

https://docs.ckan.org/projects/ckanext-spatial/en/latest/install.html#install-postgis-and-system-packages

Then, install the CKAN extension:

.. code-block:: console

    # Activate your CKAN virtualenv if needed before these steps.
    cd /usr/lib/ckan/default/src
    git clone https://github.alaska.edu/crstephenson/ckanext-glynx.git
    cd ckanext-glynx
    python setup.py develop

Load the ckanext-glynx extension and its ckanext-spatial dependencies by adding them to the the ckan.plugins line in ``/etc/ckan/default/development.ini``:

.. code-block::

    ckan.plugins = stats text_view image_view recline_view glynx spatial_metadata spatial_query
