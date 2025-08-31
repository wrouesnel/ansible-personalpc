#!/usr/bin/python
class FilterModule(object):
    def filters(self):
        return {
            'map_arch': self.map_architecture,
        }

    def map_architecture(self, arch):
        """Map architecture to golang styles"""
        if arch == "x86_64":
            return "amd64"
        return arch