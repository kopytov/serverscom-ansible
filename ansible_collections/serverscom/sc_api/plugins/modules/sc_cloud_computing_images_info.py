#!/usr/bin/python
# -*- coding: utf-8 -*-
# (c) 2020, Servers.com
# GNU General Public License v3.0
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import (absolute_import, division, print_function)


__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = """
---
module: sc_cloud_computing_images_info
version_added: "2.10"
author: "George Shuklin (@amarao)"
short_description: List of available images and snapshots
description: >
    Return list of all available images and snapshots in region.

options:
    endpoint:
      type: str
      default: https://api.servers.com/v1
      description:
        - Endpoint to use to connect to API.
        - Do not change until specifically asked to do otherwise.

    token:
      type: str
      required: true
      description:
        - Token to use.
        - You can create token for you account in https://portal.servers.com
          in Profile -> Public API section.

    region_id:
      type: int
      required: true
      description:
        - Id of cloud computing region.
        - Use I(sc_cloud_computing_regions_info) module to retrive list of
          available regions.
"""

RETURN = """
cloud_images:
  type: complex
  description:
    - List of available images
  contains:
    id:
      type: str
      description:
        - Id of the image.
    name:
      type: str
      description:
        - Human-readable name of the image.
    image_size:
      type: int
      description:
        - Image size in bytes (compressed)

    min_size:
      type: int
      description:
        - Minimal size of the disk (flavor) to use image.

    allowed_flavors:
      type: list
      elements: str
      description:
        - List of flavors allowed to run this image.
        - Empy list means compatibility with any flavor.
        - Mostly used for license-specific images.
  returned: on success

api_url:
    description: URL for the failed request
    returned: on failure
    type: str

status_code:
    description: Status code for the request
    returned: always
    type: int
"""

EXAMPLES = """
    - name: List all images in region
      sc_cloud_computing_images_info:
        token: '{{ sc_token }}'
        region_id: 0
      register: images

    - debug: var=images.cloud_images
"""


from ansible.module_utils.basic import AnsibleModule
import json
from ansible_collections.serverscom.sc_api.plugins.module_utils.api import (
    DEFAULT_API_ENDPOINT,
    ModuleError,
    ScCloudComputingImagesInfo
)

__metaclass__ = type


def main():
    module = AnsibleModule(
        argument_spec={
            'token': {'type': 'str', 'no_log': True, 'required': True},
            'endpoint': {'default': DEFAULT_API_ENDPOINT},
            'region_id': {'type': 'int', 'required': True}
        },
        supports_check_mode=True
    )

    images = ScCloudComputingImagesInfo(
        endpoint=module.params['endpoint'],
        token=module.params['token'],
        region_id=module.params['region_id']
    )
    try:
        module.exit_json(**images.run())
    except ModuleError as e:
        module.exit_json(**e.fail())


if __name__ == '__main__':
    main()
