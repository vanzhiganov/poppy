# Copyright (c) 2014 Rackspace, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json

from poppy.model.helpers import domain
from poppy.model.helpers import origin
from poppy.model.helpers import provider_details
from poppy.model import service
from poppy.storage import base


class ServicesController(base.ServicesController):

    @property
    def session(self):
        return self._driver.database

    def list(self, project_id, marker=None, limit=None):
        services = [{'name': 'mockdb1_service_name',
                     'domains': [{'domain': 'www.mywebsite.com'}],
                     'origins': [{'origin': 'mywebsite.com',
                                  'port': 80,
                                  'ssl': False}],
                     'flavorRef': 'standard',
                     'caching': [{'name': 'default',
                                  'ttl': 3600},
                                 {'name': 'home',
                                  'ttl': 17200,
                                  'rules': [{'name': 'index',
                                             'request_url': '/index.htm'}]},
                                 {'name': 'images',
                                  'ttl': 12800,
                                  'rules': [{'name': 'images',
                                             'request_url': '*.png'}]}],
                     'restrictions': [{'name': 'website only',
                                       'rules': [{'name': 'mywebsite.com',
                                                  'http_host':
                                                  'www.mywebsite.com'}]}],
                     'provider_details':
                     {
                         'MaxCDN':
                             '{\"id\": 11942,'
                             ' \"access_urls\": '
                             '[\"mypullzone.netdata.com\"]}',
                         'Mock':
                             '{\"id\": 73242,'
                             ' \"access_urls\": [\"mycdn.mock.com\"]}',
                         'CloudFront':
                             '{\"id\": \"5ABC892\",'
                             ' \"access_urls\": '
                             '[\"cf123.cloudcf.com\"]}',
                         'Fastly':
                             '{\"id\": 3488,'
                             ' \"access_urls\": '
                             '[\"mockcf123.fastly.prod.com\"]}'
                     }}
                    ]

        services_result = []
        for r in services:
            name = r.get('name', 'unnamed')
            origins = r.get('origins', [])
            domains = r.get('domains', [])
            flavorRef = r.get('flavorRef')
            provider_detail_dicts = r.get('provider_details')
            origins = [origin.Origin(d) for d in origins]
            domains = [domain.Domain(d) for d in domains]
            provider_details_dict = {}
            for provider_name in provider_detail_dicts:
                provider_detail_dict = json.loads(
                    provider_detail_dicts[provider_name])
                provider_service_id = provider_detail_dict.get('id', None)
                access_urls = provider_detail_dict.get('access_urls', [])
                status = provider_detail_dict.get('status', u'unknown')
                provider_detail_obj = provider_details.ProviderDetail(
                    provider_service_id=provider_service_id,
                    access_urls=access_urls,
                    status=status)
                provider_details_dict[provider_name] = provider_detail_obj
            service_result = service.Service(name, domains, origins, flavorRef)
            service_result.provider_details = provider_details_dict
            services_result.append(service_result)

        return services_result

    def get(self, project_id, service_name):
        # get the requested service from storage
        if service_name == "non_exist_service_name":
            raise ValueError("service: % does not exist")
        service_dict = {'name': service_name,
                        'domains': [{'domain': 'www.mywebsite.com'}],
                        'origins': [{'origin': 'mywebsite.com',
                                     'port': 80,
                                     'ssl': False}],
                        'flavorRef': 'standard',
                        'caching': [{'name': 'default',
                                     'ttl': 3600},
                                    {'name': 'home',
                                     'ttl': 17200,
                                     'rules': [{'name': 'index',
                                                'request_url': '/index.htm'}]},
                                    {'name': 'images',
                                     'ttl': 12800,
                                     'rules': [{'name': 'images',
                                                'request_url': '*.png'}]}],
                        'restrictions': [{'name': 'website only',
                                          'rules': [{'name': 'mywebsite.com',
                                                     'http_host':
                                                     'www.mywebsite.com'}]}],
                        'provider_details':
                        {
                            'MaxCDN':
                                '{\"id\": 11942,'
                                ' \"access_urls\": '
                                '[\"mypullzone.netdata.com\"]}',
                            'Mock':
                                '{\"id\": 73242,'
                                ' \"access_urls\": '
                                '[\"mycdn.mock.com\"]}',
                            'CloudFront':
                                '{\"id\": \"5ABC892\",'
                                ' \"access_urls\": '
                                '[\"cf123.cloudcf.com\"]}',
                            'Fastly':
                                '{\"id\": 3488,'
                                ' \"access_urls\": '
                                '[\"mockcf123.fastly.prod.com\"'
                                ']}'
                        }}

        name = service_dict.get('name', 'unnamed')
        origins = service_dict.get('origins', [])
        domains = service_dict.get('domains', [])
        origins = [origin.Origin(d) for d in origins]
        domains = [domain.Domain(d) for d in domains]
        flavorRef = service_dict.get('flavorRef')
        provider_detail_dicts = service_dict.get('provider_details')
        services_result = service.Service(name, domains, origins, flavorRef)
        provider_details_dict = {}
        for provider_name in provider_detail_dicts:
            provider_detail_dict = json.loads(
                provider_detail_dicts[provider_name])
            provider_service_id = provider_detail_dict.get('id', None)
            access_urls = provider_detail_dict.get('access_urls', [])
            status = provider_detail_dict.get('status', u'unknown')
            provider_detail_obj = provider_details.ProviderDetail(
                provider_service_id=provider_service_id,
                access_urls=access_urls,
                status=status)
            provider_details_dict[provider_name] = provider_detail_obj
        services_result.provider_details = provider_details_dict
        return services_result

    def create(self, project_id, service_obj):
        if service_obj.name == "mockdb1_service_name":
            raise ValueError("Service %s already exists..." % service_obj.name)
        return ""

    def update(self, project_id, service_name, service_json):
        # update configuration in storage
        return ''

    def delete(self, project_id, service_name):

        # delete from providers
        return ''

    def get_provider_details(self, project_id, service_name):
        return {
            "MaxCDN": provider_details.ProviderDetail(
                provider_service_id=11942,
                name='my_service_name',
                access_urls=['my_service_name'
                             '.mycompanyalias.netdna-cdn.com']),
            "Fastly": provider_details.ProviderDetail(
                provider_service_id=3488,
                name="my_service_name",
                access_urls=['my_service_name'
                             '.global.prod.fastly.net']),
            "CloudFront": provider_details.ProviderDetail(
                provider_service_id=5892,
                access_urls=['my_service_name'
                             '.gibberish.amzcf.com']),
            "Mock": provider_details.ProviderDetail(
                provider_service_id="73242",
                access_urls=['my_service_name.mock.com'])}

    def update_provider_details(self, project_id, service_name,
                                provider_details):
        pass