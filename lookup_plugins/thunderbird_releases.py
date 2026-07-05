# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

try:
    from __main__ import display
except ImportError:
    from ansible.utils.display import Display

    display = Display()

import re
import requests
from bs4 import BeautifulSoup

from ansible.plugins.lookup import LookupBase

from github import Github
import itertools

DOCUMENTATION = """
    lookup: thunderbird_releases
    author: Will Rouesnel <wrouesnel@wrouesnel.com>
    version_added: '8.0'
    short_description: lookup and return a dictionary of Thunderbird releases
    description:
        - This lookup queries the Mozilla FTP to discover a projects releases

    example:
      - "{{ lookup('thunderbird_releases') }}"
"""

rx = re.compile(r"^(\d+)\.*")

class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        user = kwargs.get("user")
        repo = kwargs.get("repo")
        num_results = kwargs.get("latest",None)

        r = requests.get("https://ftp.mozilla.org/pub/thunderbird/releases/")
        r.raise_for_status()

        soup = BeautifulSoup(r.content, 'lxml')
        versions = {}
        for elem in soup.find_all("tr"):
            value = elem.find("a")
            if value:
                if rx.match(value.text):
                    versions[value.text.rstrip()] = value.attrs["href"]


        # Format the data into a useful return
        result = {}
        result["by_tag"] = { item["tag_name"].lower():item for item in data if "tag_name" in item }
        result["in_order"] = data
        result["asset_by_tag"] = { item["tag_name"].lower():{asset["name"]:asset for asset in item["assets"] } for item in data if "tag_name" in item }
        return [result]
