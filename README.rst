ckanext-glynx
=============

Extend CKAN with custom fields, vocabularies, and tags migrated from GLynx.

Setup
-----

Install the CKAN extension:

.. code-block:: console

    # Activate your CKAN virtualenv if needed before these steps.
    cd /usr/lib/ckan/default/src
    git clone https://github.alaska.edu/crstephenson/ckanext-glynx.git
    cd ckanext-glynx
    python setup.py develop

Then load the extension by adding ``glynx`` to the ckan.plugins line in ``/etc/ckan/default/development.ini``:

.. code-block::

    ckan.plugins = stats text_view image_view recline_view glynx
