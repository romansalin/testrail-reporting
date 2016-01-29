# TestRail API binding (API v2, available since TestRail 3.0)
#
# Learn more:
# http://docs.gurock.com/testrail-api2/start
# http://docs.gurock.com/testrail-api2/accessing

import logging
import time

import requests

log = logging.getLogger(__name__)


class TestRailClient(object):
    def __init__(self, base_url, user, password):
        if not base_url.endswith('/'):
            base_url += '/'
        self.__url = base_url + 'index.php?/api/v2/'
        self.user = user
        self.password = password
        self.default_delay = 10

    def send_get(self, uri):
        """Send Get.

        Issues a GET request (read) against the API and returns the result
        (as Python dict).

        :param uri: The API method to call including parameters (e.g.
            get_case/1)
        """
        return self.__send_request('get', uri, data=None)

    def send_post(self, uri, data):
        """Send POST.

        Issues a POST request (write) against the API and returns the result
        (as Python dict).

        :param uri: The API method to call including parameters (e.g.
            add_case/1)
        :param data: The data to submit as part of the request (as Python
            dict, strings must be UTF-8 encoded)
        """
        return self.__send_request('post', uri, data=data)

    def __send_request(self, method, uri, **kwargs):
        url = self.__url + uri
        kwargs['auth'] = (self.user, self.password)
        kwargs['headers'] = {'Content-type': 'application/json'}
        log.debug('Request: {0} {1}'.format(method, url))
        response = requests.request(method, url, allow_redirects=False,
                                    **kwargs)

        if response.status_code == 429:  # Too Many Requests
            delay = int(response.headers.get('Retry-After')) \
                    or self.default_delay
            log.warning('Too Many Requests. Request will be retried after {0} '
                        'seconds'.format(str(delay)))
            time.sleep(delay)
            self.__send_request(method, uri, **kwargs)

        if response.status_code >= 300:
            raise APIError(
                "Wrong response from TestRail API:\n"
                "status_code: {0.status_code}\n"
                "headers: {0.headers}\n"
                "content: '{0.content}'".format(response))

        result = response.json()
        if result and 'error' in result:
            log.warning(result)
        return result


class APIError(Exception):
    pass
