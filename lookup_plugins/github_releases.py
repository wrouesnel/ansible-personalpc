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

from github import Github
import itertools

DOCUMENTATION = """
    lookup: github_releases
    author: Will Rouesnel <wrouesnel@wrouesnel.com>
    version_added: '8.0'
    short_description: lookup and return a dictionary of Github releases
    description:
        - This lookup queries Github to discover a projects releases

    example:
      - "{{ lookup('github_releases') }}"
"""


class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        user = kwargs.get("user")
        repo = kwargs.get("repo")
        num_results = kwargs.get("latest",None)

        g = Github()

        repo = g.get_user(user).get_repo(repo)

        data = [ release.raw_data for release in itertools.islice(repo.get_releases(),num_results) ]

        # Format the data into a useful return
        result = {}
        result["by_tag"] = { item["tag_name"].lower():item for item in data if "tag_name" in item }
        result["in_order"] = data
        result["asset_by_tag"] = { item["tag_name"].lower():{asset["name"]:asset for asset in item["assets"] } for item in data if "tag_name" in item }
        return [result]
