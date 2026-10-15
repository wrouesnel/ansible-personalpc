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
        - Only the newest release of each type in release_types is kept for each
          product. The upstream feed carries every historical release of every
          product (~30MB, ~9600 releases) but callers only ever want the current
          one, and the result is stored in an Ansible fact which is then
          re-templated by every task which touches it.
    options:
      release_types:
        description:
          - Release types to keep the newest release of, in preference order.
        type: list
        default: ['release']

    example:
      - "{{ lookup('jetbrains_products') }}"
"""


class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        #names = terms[0]
        release_types = kwargs.get("release_types", ["release"])

        response = requests.get("https://data.services.jetbrains.com/products")
        data = response.json()

        # Format the data into a useful return
        result = {}
        result["by_name"] = { item["name"].lower():_latest_releases(item, release_types) for item in data }

        return [result]


def _latest_releases(product, release_types):
    """Return product with releases reduced to the newest one of each type.

    The feed lists releases newest-first, so the first match for a type is the
    current one.
    """
    newest = {}
    for release in product.get("releases", []):
        release_type = release.get("type")
        if release_type in release_types and release_type not in newest:
            newest[release_type] = release

    trimmed = dict(product)
    trimmed["releases"] = [newest[t] for t in release_types if t in newest]
    return trimmed
