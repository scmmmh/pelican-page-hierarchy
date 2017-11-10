======================
Pelican Page Hierarchy
======================

Simple Pelican plugin to make the page output directory structure match the
input directory structure.

Configuration
#############

Load the plugin in your ``pelicanconf.py``

.. code:: python

  PLUGINS = ['pelican_page_hierarchy']

and then create the directory structure you need in ``pages``. In order to
automatically link parent to child pages, the child pages **must** be in a
directory that has the exact same name as the parent page's slug. You can
override this by explicitly specifying the parent page's slug in a child page.

.. code:: text

  :parent: slug

Theming
#######

For theming purposes each page has the following additional attributes:

* ``parent`` - The parent page or ``None``
* ``parents`` - The full hierarchy of parent pages or an empty list
* ``children`` - The list of child pages
