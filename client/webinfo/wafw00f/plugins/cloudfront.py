#!/usr/bin/env python
'''
Copyright (C) 2020, WAFW00F Developers.
See the LICENSE file for copying permission.
'''

NAME = 'Cloudfront (Amazon)'


def is_waf(self):
    schemes = [
        # This is standard detection schema, checking the server header
        self.matchHeader(('Server', 'Cloudfront')),
        # Found samples returning 'Via: 1.1 58bfg7h6fg76h8fg7jhdf2.cloudfront.net (CloudFront)'
        self.matchHeader(('Via', r'([0-9\.]+?)? \w+?\.cloudfront\.net \(Cloudfront\)')),
        # The request token is sent along with this header, eg:
        # X-Amz-Cf-Id: sX5QSkbAzSwd-xx3RbJmxYHL3iVNNyXa1UIebDNCshQbHxCjVcWDww==
        self.matchHeader(('X-Amz-Cf-Id', '.+?'), attack=True),
        # This is another reliable fingerprint found on headers
        self.matchHeader(('X-Cache', 'Error from Cloudfront'), attack=True),
        # These fingerprints are found on the blockpage itself
        self.matchContent(r'Generated by cloudfront \(CloudFront\)')
    ]
    if any(i for i in schemes):
        return True
    return False