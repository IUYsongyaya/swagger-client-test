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


class ProjectApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def projects_coins_init_get(self, init, **kwargs):  # noqa: E501
        """获取币种列表  # noqa: E501

        获取币种列表  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.projects_coins_init_get(init, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param bool init: 是否初始化 (required)
        :return: GetCoinListsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.projects_coins_init_get_with_http_info(init, **kwargs)  # noqa: E501
        else:
            (data) = self.projects_coins_init_get_with_http_info(init, **kwargs)  # noqa: E501
            return data

    def projects_coins_init_get_with_http_info(self, init, **kwargs):  # noqa: E501
        """获取币种列表  # noqa: E501

        获取币种列表  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.projects_coins_init_get_with_http_info(init, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param bool init: 是否初始化 (required)
        :return: GetCoinListsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['init']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method projects_coins_init_get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'init' is set
        if ('init' not in params or
                params['init'] is None):
            raise ValueError("Missing the required parameter `init` when calling `projects_coins_init_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'init' in params:
            path_params['init'] = params['init']  # noqa: E501

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
            '/projects/coins/{init}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='GetCoinListsResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def projects_get(self, page, sort_key, limit, **kwargs):  # noqa: E501
        """获取项目列表  # noqa: E501

        获取项目列表  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.projects_get(page, sort_key, limit, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int page: 页码 (required)
        :param str sort_key: 排序依据,volume:24小时交易量,marketValue:市值 (required)
        :param int limit: 显示条数 (required)
        :return: GetProjectsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.projects_get_with_http_info(page, sort_key, limit, **kwargs)  # noqa: E501
        else:
            (data) = self.projects_get_with_http_info(page, sort_key, limit, **kwargs)  # noqa: E501
            return data

    def projects_get_with_http_info(self, page, sort_key, limit, **kwargs):  # noqa: E501
        """获取项目列表  # noqa: E501

        获取项目列表  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.projects_get_with_http_info(page, sort_key, limit, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int page: 页码 (required)
        :param str sort_key: 排序依据,volume:24小时交易量,marketValue:市值 (required)
        :param int limit: 显示条数 (required)
        :return: GetProjectsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['page', 'sort_key', 'limit']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method projects_get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'page' is set
        if ('page' not in params or
                params['page'] is None):
            raise ValueError("Missing the required parameter `page` when calling `projects_get`")  # noqa: E501
        # verify the required parameter 'sort_key' is set
        if ('sort_key' not in params or
                params['sort_key'] is None):
            raise ValueError("Missing the required parameter `sort_key` when calling `projects_get`")  # noqa: E501
        # verify the required parameter 'limit' is set
        if ('limit' not in params or
                params['limit'] is None):
            raise ValueError("Missing the required parameter `limit` when calling `projects_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'page' in params:
            query_params.append(('page', params['page']))  # noqa: E501
        if 'sort_key' in params:
            query_params.append(('sortKey', params['sort_key']))  # noqa: E501
        if 'limit' in params:
            query_params.append(('limit', params['limit']))  # noqa: E501

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
            '/projects', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='GetProjectsResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def projects_id_get(self, id, **kwargs):  # noqa: E501
        """获取项目详情  # noqa: E501

        获取项目详情（项目方、交易所、主平台、用户管理后台）  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.projects_id_get(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id: 项目ID (required)
        :return: GetProjectResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.projects_id_get_with_http_info(id, **kwargs)  # noqa: E501
        else:
            (data) = self.projects_id_get_with_http_info(id, **kwargs)  # noqa: E501
            return data

    def projects_id_get_with_http_info(self, id, **kwargs):  # noqa: E501
        """获取项目详情  # noqa: E501

        获取项目详情（项目方、交易所、主平台、用户管理后台）  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.projects_id_get_with_http_info(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id: 项目ID (required)
        :return: GetProjectResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method projects_id_get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `projects_id_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']  # noqa: E501

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
            '/projects/{id}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='GetProjectResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def projects_search_get(self, value, **kwargs):  # noqa: E501
        """搜索项目名称列表  # noqa: E501

        根据输入条件查询项目名称列表  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.projects_search_get(value, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str value: 搜索条件 (required)
        :return: GetProjectsSearchResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.projects_search_get_with_http_info(value, **kwargs)  # noqa: E501
        else:
            (data) = self.projects_search_get_with_http_info(value, **kwargs)  # noqa: E501
            return data

    def projects_search_get_with_http_info(self, value, **kwargs):  # noqa: E501
        """搜索项目名称列表  # noqa: E501

        根据输入条件查询项目名称列表  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.projects_search_get_with_http_info(value, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str value: 搜索条件 (required)
        :return: GetProjectsSearchResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['value']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method projects_search_get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'value' is set
        if ('value' not in params or
                params['value'] is None):
            raise ValueError("Missing the required parameter `value` when calling `projects_search_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'value' in params:
            query_params.append(('value', params['value']))  # noqa: E501

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
            '/projects/search', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='GetProjectsSearchResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)