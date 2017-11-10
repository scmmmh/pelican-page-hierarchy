'''
###########################################
Pelican plugin to generate a page hierarchy
###########################################
'''
import os

from itertools import chain
from pelican import signals, contents


def get_path(content_object):
    """Returns the ``content_object``\ 's path as a list. Strips the first
    element of the list (which is "pages").
    """
    return content_object.get_relative_source_path().replace(os.path.sep, '/').split('/')[1:]


def update_slugs(content_object):
    """Updates all pages' slugs to include any directory paths."""
    if type(content_object) is contents.Page:
        path = get_path(content_object)
        if len(path) > 1:
            content_object.slug = '%s/%s' % ('/'.join(path[:-1]), content_object.slug)


def fix_relationships(generator):
    """Adds ``parent``, ``parents``, and ``children`` attributes to all
    pages.
    """
    def page_iterator():
        return chain(generator.pages, generator.translations)

    def parent_hierarchy(page):
        if page.parent:
            return parent_hierarchy(page.parent) + [page]
        else:
            return [page]

    for page in page_iterator():
        page.children = []
        if hasattr(page, 'parent'):
            for page2 in page_iterator():
                if page2.slug == page.parent:
                    page.parent = page2
                    break
            if isinstance(page.parent, str):
                page.parent = None
        else:
            page.parent = None
            path = get_path(page)
            if len(path) > 1:
                for page2 in page_iterator():
                    if page2.slug.split('/') == path[:-1]:
                        page.parent = page2
                        break
    for page in page_iterator():
        if page.parent:
            page.parents = parent_hierarchy(page.parent)
            page.parent.children.append(page)
        else:
            page.parents = []


def register():
    """Registers the processing callbacks."""
    signals.content_object_init.connect(update_slugs)
    signals.page_generator_finalized.connect(fix_relationships)
