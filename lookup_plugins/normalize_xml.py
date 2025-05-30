# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

try:
    from __main__ import display
except ImportError:
    from ansible.utils.display import Display

    display = Display()

from ansible.plugins.lookup import LookupBase

from typing import List
from lxml import etree

DOCUMENTATION = """
    lookup: normalize_xml
    author: Will Rouesnel <wrouesnel@wrouesnel.com>
    version_added: '8.0'
    short_description: format the supplied string to a normalized XML form
    description:
        - This lookup normalizes an XML string

    example:
      - "{{ lookup('normalize_xml') }}"
"""


class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        xml = terms[0]

        xpaths = []
        if "remove" in kwargs:
            if isinstance(kwargs["remove"], List):
                xpaths.extend(kwargs["remove"])
            else:
                xpaths.append(kwargs["remove"])

        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.fromstring(xml)

        for xpath in xpaths:
            for to_remove in tree.xpath(xpath):
                to_remove.getparent().remove(to_remove)

        return [etree.tostring(tree, pretty_print=True)]
