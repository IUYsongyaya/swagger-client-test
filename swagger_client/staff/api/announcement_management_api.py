# coding: utf-8

"""
    crush-staff 平台接口（职员管理平台）

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: 2.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from swagger_client.staff.api_client import ApiClient


class AnnouncementManagementApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def announcements_exchanges_get(self, **kwargs):  # noqa: E501
        """获取所有交易所公告列表  # noqa: E501

        交易所公告列表  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.announcements_exchanges_get(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int page: 页码
        :param str start_at: 开始时间
        :param str end_at: 结束时间
        :param str exchange_id: 交易所ID
        :param str title: 标题
        :return: GetAnnouncementsByAllExchangeResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.announcements_exchanges_get_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.announcements_exchanges_get_with_http_info(**kwargs)  # noqa: E501
            return data

    def announcements_exchanges_get_with_http_info(self, **kwargs):  # noqa: E501
        """获取所有交易所公告列表  # noqa: E501

        交易所公告列表  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.announcements_exchanges_get_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int page: 页码
        :param str start_at: 开始时间
        :param str end_at: 结束时间
        :param str exchange_id: 交易所ID
        :param str title: 标题
        :return: GetAnnouncementsByAllExchangeResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['page', 'start_at', 'end_at', 'exchange_id', 'title']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method announcements_exchanges_get" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'page' in params:
            query_params.append(('page', params['page']))  # noqa: E501
        if 'start_at' in params:
            query_params.append(('startAt', params['start_at']))  # noqa: E501
        if 'end_at' in params:
            query_params.append(('endAt', params['end_at']))  # noqa: E501
        if 'exchange_id' in params:
            query_params.append(('exchangeId', params['exchange_id']))  # noqa: E501
        if 'title' in params:
            query_params.append(('title', params['title']))  # noqa: E501

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
            '/announcements/exchanges', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='GetAnnouncementsByAllExchangeResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def announcements_exchanges_list_exchange_id_get(self, exchange_id, **kwargs):  # noqa: E501
        """获取某一个交易所公告列表  # noqa: E501

        交易所公告列表  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.announcements_exchanges_list_exchange_id_get(exchange_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str exchange_id: 交易所ID (required)
        :param int page: 页码
        :return: GetAnnouncementsByExchangeIdResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.announcements_exchanges_list_exchange_id_get_with_http_info(exchange_id, **kwargs)  # noqa: E501
        else:
            (data) = self.announcements_exchanges_list_exchange_id_get_with_http_info(exchange_id, **kwargs)  # noqa: E501
            return data

    def announcements_exchanges_list_exchange_id_get_with_http_info(self, exchange_id, **kwargs):  # noqa: E501
        """获取某一个交易所公告列表  # noqa: E501

        交易所公告列表  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.announcements_exchanges_list_exchange_id_get_with_http_info(exchange_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str exchange_id: 交易所ID (required)
        :param int page: 页码
        :return: GetAnnouncementsByExchangeIdResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['exchange_id', 'page']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method announcements_exchanges_list_exchange_id_get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'exchange_id' is set
        if ('exchange_id' not in params or
                params['exchange_id'] is None):
            raise ValueError("Missing the required parameter `exchange_id` when calling `announcements_exchanges_list_exchange_id_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'exchange_id' in params:
            path_params['exchangeId'] = params['exchange_id']  # noqa: E501

        query_params = []
        if 'page' in params:
            query_params.append(('page', params['page']))  # noqa: E501

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
            '/announcements/exchanges/list/{exchangeId}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='GetAnnouncementsByExchangeIdResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def announcements_id_get(self, id, **kwargs):  # noqa: E501
        """公告详情  # noqa: E501

        公告详情  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.announcements_id_get(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id: 公告ID (required)
        :return: GetAnnouncementsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.announcements_id_get_with_http_info(id, **kwargs)  # noqa: E501
        else:
            (data) = self.announcements_id_get_with_http_info(id, **kwargs)  # noqa: E501
            return data

    def announcements_id_get_with_http_info(self, id, **kwargs):  # noqa: E501
        """公告详情  # noqa: E501

        公告详情  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.announcements_id_get_with_http_info(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id: 公告ID (required)
        :return: GetAnnouncementsResponse
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
                    " to method announcements_id_get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `announcements_id_get`")  # noqa: E501

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
        auth_settings = ['api_key']  # noqa: E501

        return self.api_client.call_api(
            '/announcements/{id}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='GetAnnouncementsResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def announcements_id_status_put(self, id, status, **kwargs):  # noqa: E501
        """修改公告的状态  # noqa: E501

        修改公告的状态  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.announcements_id_status_put(id, status, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id: 公告ID (required)
        :param bool status: 状态 (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.announcements_id_status_put_with_http_info(id, status, **kwargs)  # noqa: E501
        else:
            (data) = self.announcements_id_status_put_with_http_info(id, status, **kwargs)  # noqa: E501
            return data

    def announcements_id_status_put_with_http_info(self, id, status, **kwargs):  # noqa: E501
        """修改公告的状态  # noqa: E501

        修改公告的状态  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.announcements_id_status_put_with_http_info(id, status, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id: 公告ID (required)
        :param bool status: 状态 (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['id', 'status']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method announcements_id_status_put" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `announcements_id_status_put`")  # noqa: E501
        # verify the required parameter 'status' is set
        if ('status' not in params or
                params['status'] is None):
            raise ValueError("Missing the required parameter `status` when calling `announcements_id_status_put`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']  # noqa: E501

        query_params = []
        if 'status' in params:
            query_params.append(('status', params['status']))  # noqa: E501

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
            '/announcements/{id}/status', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def announcements_projects_list_project_id_get(self, project_id, **kwargs):  # noqa: E501
        """获取某一个项目公告列表  # noqa: E501

        项目公告列表  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.announcements_projects_list_project_id_get(project_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str project_id: 项目ID (required)
        :param int page: 页码
        :param str start_at: 开始时间
        :param str end_at: 结束时间
        :return: GetAnnouncementsByProjectIdResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.announcements_projects_list_project_id_get_with_http_info(project_id, **kwargs)  # noqa: E501
        else:
            (data) = self.announcements_projects_list_project_id_get_with_http_info(project_id, **kwargs)  # noqa: E501
            return data

    def announcements_projects_list_project_id_get_with_http_info(self, project_id, **kwargs):  # noqa: E501
        """获取某一个项目公告列表  # noqa: E501

        项目公告列表  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.announcements_projects_list_project_id_get_with_http_info(project_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str project_id: 项目ID (required)
        :param int page: 页码
        :param str start_at: 开始时间
        :param str end_at: 结束时间
        :return: GetAnnouncementsByProjectIdResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['project_id', 'page', 'start_at', 'end_at']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method announcements_projects_list_project_id_get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'project_id' is set
        if ('project_id' not in params or
                params['project_id'] is None):
            raise ValueError("Missing the required parameter `project_id` when calling `announcements_projects_list_project_id_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'project_id' in params:
            path_params['projectId'] = params['project_id']  # noqa: E501

        query_params = []
        if 'page' in params:
            query_params.append(('page', params['page']))  # noqa: E501
        if 'start_at' in params:
            query_params.append(('startAt', params['start_at']))  # noqa: E501
        if 'end_at' in params:
            query_params.append(('endAt', params['end_at']))  # noqa: E501

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
            '/announcements/projects/list/{projectId}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='GetAnnouncementsByProjectIdResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def news_id_status_put(self, id, status, **kwargs):  # noqa: E501
        """修改项目资讯的状态  # noqa: E501

        修改项目资讯的状态  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.news_id_status_put(id, status, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id: 资讯ID (required)
        :param bool status: 状态 (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.news_id_status_put_with_http_info(id, status, **kwargs)  # noqa: E501
        else:
            (data) = self.news_id_status_put_with_http_info(id, status, **kwargs)  # noqa: E501
            return data

    def news_id_status_put_with_http_info(self, id, status, **kwargs):  # noqa: E501
        """修改项目资讯的状态  # noqa: E501

        修改项目资讯的状态  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.news_id_status_put_with_http_info(id, status, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id: 资讯ID (required)
        :param bool status: 状态 (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['id', 'status']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method news_id_status_put" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `news_id_status_put`")  # noqa: E501
        # verify the required parameter 'status' is set
        if ('status' not in params or
                params['status'] is None):
            raise ValueError("Missing the required parameter `status` when calling `news_id_status_put`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']  # noqa: E501

        query_params = []
        if 'status' in params:
            query_params.append(('status', params['status']))  # noqa: E501

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
            '/news/{id}/status', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def news_project_id_get(self, project_id, **kwargs):  # noqa: E501
        """获取项目资讯列表  # noqa: E501

        获取项目资讯列表  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.news_project_id_get(project_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str project_id: 项目ID (required)
        :param int page: 页码
        :param str start_at: 开始时间
        :param str end_at: 结束时间
        :return: GetProjectNewsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.news_project_id_get_with_http_info(project_id, **kwargs)  # noqa: E501
        else:
            (data) = self.news_project_id_get_with_http_info(project_id, **kwargs)  # noqa: E501
            return data

    def news_project_id_get_with_http_info(self, project_id, **kwargs):  # noqa: E501
        """获取项目资讯列表  # noqa: E501

        获取项目资讯列表  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.news_project_id_get_with_http_info(project_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str project_id: 项目ID (required)
        :param int page: 页码
        :param str start_at: 开始时间
        :param str end_at: 结束时间
        :return: GetProjectNewsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['project_id', 'page', 'start_at', 'end_at']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method news_project_id_get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'project_id' is set
        if ('project_id' not in params or
                params['project_id'] is None):
            raise ValueError("Missing the required parameter `project_id` when calling `news_project_id_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'project_id' in params:
            path_params['projectId'] = params['project_id']  # noqa: E501

        query_params = []
        if 'page' in params:
            query_params.append(('page', params['page']))  # noqa: E501
        if 'start_at' in params:
            query_params.append(('startAt', params['start_at']))  # noqa: E501
        if 'end_at' in params:
            query_params.append(('endAt', params['end_at']))  # noqa: E501

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
            '/news/{projectId}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='GetProjectNewsResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def reports_id_status_put(self, id, status, **kwargs):  # noqa: E501
        """修改项目报告的状态  # noqa: E501

        修改项目报告的状态  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.reports_id_status_put(id, status, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id: 报告ID (required)
        :param bool status: 状态 (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.reports_id_status_put_with_http_info(id, status, **kwargs)  # noqa: E501
        else:
            (data) = self.reports_id_status_put_with_http_info(id, status, **kwargs)  # noqa: E501
            return data

    def reports_id_status_put_with_http_info(self, id, status, **kwargs):  # noqa: E501
        """修改项目报告的状态  # noqa: E501

        修改项目报告的状态  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.reports_id_status_put_with_http_info(id, status, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id: 报告ID (required)
        :param bool status: 状态 (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['id', 'status']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method reports_id_status_put" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `reports_id_status_put`")  # noqa: E501
        # verify the required parameter 'status' is set
        if ('status' not in params or
                params['status'] is None):
            raise ValueError("Missing the required parameter `status` when calling `reports_id_status_put`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']  # noqa: E501

        query_params = []
        if 'status' in params:
            query_params.append(('status', params['status']))  # noqa: E501

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
            '/reports/{id}/status', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def reports_project_id_get(self, project_id, **kwargs):  # noqa: E501
        """获取项目报告列表  # noqa: E501

        获取项目报告列表  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.reports_project_id_get(project_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str project_id: 项目ID (required)
        :param int page: 页码
        :param str type: 报告类型(日报、周报、月报、年报、其他)
        :param str start_at: 开始时间
        :param str end_at: 结束时间
        :return: GetProjectReportsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.reports_project_id_get_with_http_info(project_id, **kwargs)  # noqa: E501
        else:
            (data) = self.reports_project_id_get_with_http_info(project_id, **kwargs)  # noqa: E501
            return data

    def reports_project_id_get_with_http_info(self, project_id, **kwargs):  # noqa: E501
        """获取项目报告列表  # noqa: E501

        获取项目报告列表  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.reports_project_id_get_with_http_info(project_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str project_id: 项目ID (required)
        :param int page: 页码
        :param str type: 报告类型(日报、周报、月报、年报、其他)
        :param str start_at: 开始时间
        :param str end_at: 结束时间
        :return: GetProjectReportsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['project_id', 'page', 'type', 'start_at', 'end_at']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method reports_project_id_get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'project_id' is set
        if ('project_id' not in params or
                params['project_id'] is None):
            raise ValueError("Missing the required parameter `project_id` when calling `reports_project_id_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'project_id' in params:
            path_params['projectId'] = params['project_id']  # noqa: E501

        query_params = []
        if 'page' in params:
            query_params.append(('page', params['page']))  # noqa: E501
        if 'type' in params:
            query_params.append(('type', params['type']))  # noqa: E501
        if 'start_at' in params:
            query_params.append(('startAt', params['start_at']))  # noqa: E501
        if 'end_at' in params:
            query_params.append(('endAt', params['end_at']))  # noqa: E501

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
            '/reports/{projectId}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='GetProjectReportsResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)