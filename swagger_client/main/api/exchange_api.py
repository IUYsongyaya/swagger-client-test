# coding: utf-8

"""
    crush-main 平台接口（主平台）

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: 2.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from swagger_client.main.api_client import ApiClient


class ExchangeApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def exchanges_exchange_coin_exchange_id_get(self, exchange_id, **kwargs):  # noqa: E501
        """获取交易所买卖方币种列表-邹凌威  # noqa: E501

        获取交易所买卖方币种列表-邹凌威  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.exchanges_exchange_coin_exchange_id_get(exchange_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str exchange_id: 交易所ID (required)
        :return: ExchangeCoin
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.exchanges_exchange_coin_exchange_id_get_with_http_info(exchange_id, **kwargs)  # noqa: E501
        else:
            (data) = self.exchanges_exchange_coin_exchange_id_get_with_http_info(exchange_id, **kwargs)  # noqa: E501
            return data

    def exchanges_exchange_coin_exchange_id_get_with_http_info(self, exchange_id, **kwargs):  # noqa: E501
        """获取交易所买卖方币种列表-邹凌威  # noqa: E501

        获取交易所买卖方币种列表-邹凌威  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.exchanges_exchange_coin_exchange_id_get_with_http_info(exchange_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str exchange_id: 交易所ID (required)
        :return: ExchangeCoin
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['exchange_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method exchanges_exchange_coin_exchange_id_get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'exchange_id' is set
        if ('exchange_id' not in params or
                params['exchange_id'] is None):
            raise ValueError("Missing the required parameter `exchange_id` when calling `exchanges_exchange_coin_exchange_id_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'exchange_id' in params:
            path_params['exchangeId'] = params['exchange_id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['api_key']  # noqa: E501

        return self.api_client.call_api(
            '/exchanges/exchange-coin/{exchangeId}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ExchangeCoin',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def exchanges_exchanges_get(self, **kwargs):  # noqa: E501
        """交易所排行列表-邹凌威  # noqa: E501

        交易所排行列表-邹凌威  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.exchanges_exchanges_get(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int page: 页码
        :param str sort_key: 排序依据，amount:成交额,concernNumber:关注度
        :param int page_size: 每页条数
        :return: GetExchangeListResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.exchanges_exchanges_get_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.exchanges_exchanges_get_with_http_info(**kwargs)  # noqa: E501
            return data

    def exchanges_exchanges_get_with_http_info(self, **kwargs):  # noqa: E501
        """交易所排行列表-邹凌威  # noqa: E501

        交易所排行列表-邹凌威  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.exchanges_exchanges_get_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int page: 页码
        :param str sort_key: 排序依据，amount:成交额,concernNumber:关注度
        :param int page_size: 每页条数
        :return: GetExchangeListResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['page', 'sort_key', 'page_size']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method exchanges_exchanges_get" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'page' in params:
            query_params.append(('page', params['page']))  # noqa: E501
        if 'sort_key' in params:
            query_params.append(('sortKey', params['sort_key']))  # noqa: E501
        if 'page_size' in params:
            query_params.append(('pageSize', params['page_size']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/exchanges/exchanges', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='GetExchangeListResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def exchanges_suggestion_get(self, name, **kwargs):  # noqa: E501
        """交易所列表模糊查询-邹凌威  # noqa: E501

        交易所列表模糊查询-邹凌威  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.exchanges_suggestion_get(name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str name: 名称 (required)
        :return: GetSuggestionExchangeListResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.exchanges_suggestion_get_with_http_info(name, **kwargs)  # noqa: E501
        else:
            (data) = self.exchanges_suggestion_get_with_http_info(name, **kwargs)  # noqa: E501
            return data

    def exchanges_suggestion_get_with_http_info(self, name, **kwargs):  # noqa: E501
        """交易所列表模糊查询-邹凌威  # noqa: E501

        交易所列表模糊查询-邹凌威  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.exchanges_suggestion_get_with_http_info(name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str name: 名称 (required)
        :return: GetSuggestionExchangeListResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['name']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method exchanges_suggestion_get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'name' is set
        if ('name' not in params or
                params['name'] is None):
            raise ValueError("Missing the required parameter `name` when calling `exchanges_suggestion_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'name' in params:
            query_params.append(('name', params['name']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/exchanges/suggestion', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='GetSuggestionExchangeListResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def exchanges_total_data_get(self, **kwargs):  # noqa: E501
        """获取总数据-邹凌威  # noqa: E501

        获取总数据-邹凌威  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.exchanges_total_data_get(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :return: GetTotalDataResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.exchanges_total_data_get_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.exchanges_total_data_get_with_http_info(**kwargs)  # noqa: E501
            return data

    def exchanges_total_data_get_with_http_info(self, **kwargs):  # noqa: E501
        """获取总数据-邹凌威  # noqa: E501

        获取总数据-邹凌威  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.exchanges_total_data_get_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :return: GetTotalDataResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = []  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method exchanges_total_data_get" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/exchanges/total-data', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='GetTotalDataResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
