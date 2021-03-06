# coding: utf-8

"""
    crush-otc 平台接口（法币交易）

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: 2.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from swagger_client.otc.api_client import ApiClient


class FileUploadApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def file_key_get(self, key, **kwargs):  # noqa: E501
        """由key来获取对应资源的URL  # noqa: E501

        由key来获取对应资源的URL  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.file_key_get(key, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str key: 文件key (required)
        :return: GetUrlResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.file_key_get_with_http_info(key, **kwargs)  # noqa: E501
        else:
            (data) = self.file_key_get_with_http_info(key, **kwargs)  # noqa: E501
            return data

    def file_key_get_with_http_info(self, key, **kwargs):  # noqa: E501
        """由key来获取对应资源的URL  # noqa: E501

        由key来获取对应资源的URL  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.file_key_get_with_http_info(key, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str key: 文件key (required)
        :return: GetUrlResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['key']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method file_key_get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'key' is set
        if ('key' not in params or
                params['key'] is None):
            raise ValueError("Missing the required parameter `key` when calling `file_key_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'key' in params:
            path_params['key'] = params['key']  # noqa: E501

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
            '/file/{key}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='GetUrlResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def file_key_zoom_zoom_get(self, key, zoom, **kwargs):  # noqa: E501
        """由key来获取对应图片  # noqa: E501

        由key来获取对应图片，并缩放  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.file_key_zoom_zoom_get(key, zoom, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str key: 文件key (required)
        :param str zoom: 缩放大小，合理的取值为：0，1，2，3，分别表示原图，小图，中图，大图，图的尺寸通过配置。 (required)
        :return: GetUrlResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.file_key_zoom_zoom_get_with_http_info(key, zoom, **kwargs)  # noqa: E501
        else:
            (data) = self.file_key_zoom_zoom_get_with_http_info(key, zoom, **kwargs)  # noqa: E501
            return data

    def file_key_zoom_zoom_get_with_http_info(self, key, zoom, **kwargs):  # noqa: E501
        """由key来获取对应图片  # noqa: E501

        由key来获取对应图片，并缩放  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.file_key_zoom_zoom_get_with_http_info(key, zoom, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str key: 文件key (required)
        :param str zoom: 缩放大小，合理的取值为：0，1，2，3，分别表示原图，小图，中图，大图，图的尺寸通过配置。 (required)
        :return: GetUrlResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['key', 'zoom']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method file_key_zoom_zoom_get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'key' is set
        if ('key' not in params or
                params['key'] is None):
            raise ValueError("Missing the required parameter `key` when calling `file_key_zoom_zoom_get`")  # noqa: E501
        # verify the required parameter 'zoom' is set
        if ('zoom' not in params or
                params['zoom'] is None):
            raise ValueError("Missing the required parameter `zoom` when calling `file_key_zoom_zoom_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'key' in params:
            path_params['key'] = params['key']  # noqa: E501
        if 'zoom' in params:
            path_params['zoom'] = params['zoom']  # noqa: E501

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
            '/file/{key}/zoom/{zoom}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='GetUrlResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def upload(self, **kwargs):  # noqa: E501
        """文件上传、图片上传  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.upload(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param file file:
        :return: PostFileResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.upload_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.upload_with_http_info(**kwargs)  # noqa: E501
            return data

    def upload_with_http_info(self, **kwargs):  # noqa: E501
        """文件上传、图片上传  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.upload_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param file file:
        :return: PostFileResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['file']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method upload" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'file' in params:
            local_var_files['file'] = params['file']  # noqa: E501

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['multipart/form-data'])  # noqa: E501

        # Authentication setting
        auth_settings = ['api_key']  # noqa: E501

        return self.api_client.call_api(
            '/file/upload', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='PostFileResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
