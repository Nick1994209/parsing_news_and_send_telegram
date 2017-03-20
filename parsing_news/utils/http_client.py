# -*- coding: utf-8 -*-
import logging
import requests

logger = logging.getLogger(__name__)

GOOD_STATUS = 200


class HTTPClient(object):
    """Унифицированный класс для выполнения http запросов"""
    log = logger

    class Method:
        POST = 'post'
        GET = 'get'

    DEFAULT_TIMEOUT = (10, 10)  # seconds
    DEFAULT_HEADERS = {
        'User-Agent': 'Python Client',
    }

    def __init__(self, timeout=None, good_http_codes=None):
        self.timeout = timeout or self.DEFAULT_TIMEOUT
        self.good_http_codes = good_http_codes

    def request(self, method, url, data=None, headers=None, **kwargs):
        """
            @param method: Method.POST или Method.GET
            @return request.Response object или None
        """
        final_headers = self.DEFAULT_HEADERS.copy()
        final_headers.update(headers or {})
        request_parameters = dict(
            data=data,
            headers=final_headers,
            timeout=self.timeout,
        )
        request_parameters.update(kwargs)
        try:
            response = requests.request(
                method,
                url,
                **request_parameters
            )
        except requests.RequestException:
            self.log.exception(
                'HTTP request failed',
                extra=request_parameters,
            )
            return None
        except ValueError as ex:
            self.log.error(
                'Error while reading response',
                extra={'data': {
                    'response.text': response.text if response else None,
                    'url': response.url if response else url,
                    'exception': ex,
                }}
            )
            return None
        if (self.good_http_codes is not None and
                response.status_code not in self.good_http_codes):
            extra = {
                'response_headers': dict(response.headers),
                'response_content': response.content,
            }
            extra.update(request_parameters)
            self.log.critical(
                'Wrong HTTP status code %s', response.status_code,
                extra=extra
            )
        return response

    def get(self, *args, **kwargs):
        kwargs.pop('method', None)
        return self.request(self.Method.GET, *args, **kwargs)

    def post(self, *args, **kwargs):
        kwargs.pop('method', None)
        return self.request(self.Method.POST, *args, **kwargs)


simple_client = HTTPClient(good_http_codes={GOOD_STATUS, })
