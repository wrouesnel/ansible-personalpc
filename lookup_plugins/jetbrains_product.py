# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

try:
    from __main__ import display
except ImportError:
    from ansible.utils.display import Display

    display = Display()

import requests

from ansible.plugins.lookup import LookupBase

DOCUMENTATION = """
    lookup: jetbrains_products
    author: Will Rouesnel <wrouesnel@wrouesnel.com>
    version_added: '8.0'
    short_description: lookup and return a dictionary of Jetbrains products
    description:
        - This lookup queries the Jetbrains website to lookup product information.

    example:
      - "{{ lookup('jetbrains_products') }}"
"""


class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        names = terms[0]

        response = requests.get("https://data.services.jetbrains.com/products")
        data = response.json()

        # Format the data into a useful return
        result = {}
        result["by_name"] = { item["name"].lower():item for item in data }

        return [result]
