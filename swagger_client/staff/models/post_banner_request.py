# coding: utf-8

"""
    crush-staff 平台接口（职员管理平台）

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: 2.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class PostBannerRequest(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'title': 'str',
        'banner': 'str',
        'url': 'str',
        'platform': 'str',
        'position': 'str',
        'language': 'str',
        'order': 'int',
        'status': 'bool'
    }

    attribute_map = {
        'title': 'title',
        'banner': 'banner',
        'url': 'url',
        'platform': 'platform',
        'position': 'position',
        'language': 'language',
        'order': 'order',
        'status': 'status'
    }

    def __init__(self, title=None, banner=None, url=None, platform=None, position=None, language=None, order=None, status=None):  # noqa: E501
        """PostBannerRequest - a model defined in Swagger"""  # noqa: E501

        self._title = None
        self._banner = None
        self._url = None
        self._platform = None
        self._position = None
        self._language = None
        self._order = None
        self._status = None
        self.discriminator = None

        if title is not None:
            self.title = title
        if banner is not None:
            self.banner = banner
        if url is not None:
            self.url = url
        if platform is not None:
            self.platform = platform
        if position is not None:
            self.position = position
        if language is not None:
            self.language = language
        if order is not None:
            self.order = order
        if status is not None:
            self.status = status

    @property
    def title(self):
        """Gets the title of this PostBannerRequest.  # noqa: E501

        标题  # noqa: E501

        :return: The title of this PostBannerRequest.  # noqa: E501
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title):
        """Sets the title of this PostBannerRequest.

        标题  # noqa: E501

        :param title: The title of this PostBannerRequest.  # noqa: E501
        :type: str
        """
        if title is not None and len(title) > 16:
            raise ValueError("Invalid value for `title`, length must be less than or equal to `16`")  # noqa: E501
        if title is not None and len(title) < 2:
            raise ValueError("Invalid value for `title`, length must be greater than or equal to `2`")  # noqa: E501

        self._title = title

    @property
    def banner(self):
        """Gets the banner of this PostBannerRequest.  # noqa: E501

        轮播图  # noqa: E501

        :return: The banner of this PostBannerRequest.  # noqa: E501
        :rtype: str
        """
        return self._banner

    @banner.setter
    def banner(self, banner):
        """Sets the banner of this PostBannerRequest.

        轮播图  # noqa: E501

        :param banner: The banner of this PostBannerRequest.  # noqa: E501
        :type: str
        """

        self._banner = banner

    @property
    def url(self):
        """Gets the url of this PostBannerRequest.  # noqa: E501

        跳转链接  # noqa: E501

        :return: The url of this PostBannerRequest.  # noqa: E501
        :rtype: str
        """
        return self._url

    @url.setter
    def url(self, url):
        """Sets the url of this PostBannerRequest.

        跳转链接  # noqa: E501

        :param url: The url of this PostBannerRequest.  # noqa: E501
        :type: str
        """

        self._url = url

    @property
    def platform(self):
        """Gets the platform of this PostBannerRequest.  # noqa: E501

        平台 pc网页端 mobile移动端  # noqa: E501

        :return: The platform of this PostBannerRequest.  # noqa: E501
        :rtype: str
        """
        return self._platform

    @platform.setter
    def platform(self, platform):
        """Sets the platform of this PostBannerRequest.

        平台 pc网页端 mobile移动端  # noqa: E501

        :param platform: The platform of this PostBannerRequest.  # noqa: E501
        :type: str
        """
        allowed_values = ["pc", "mobile"]  # noqa: E501
        if platform not in allowed_values:
            raise ValueError(
                "Invalid value for `platform` ({0}), must be one of {1}"  # noqa: E501
                .format(platform, allowed_values)
            )

        self._platform = platform

    @property
    def position(self):
        """Gets the position of this PostBannerRequest.  # noqa: E501

        轮播位置 homepage首页轮播，exchange_homepage交易所首页轮播  # noqa: E501

        :return: The position of this PostBannerRequest.  # noqa: E501
        :rtype: str
        """
        return self._position

    @position.setter
    def position(self, position):
        """Sets the position of this PostBannerRequest.

        轮播位置 homepage首页轮播，exchange_homepage交易所首页轮播  # noqa: E501

        :param position: The position of this PostBannerRequest.  # noqa: E501
        :type: str
        """
        allowed_values = ["homepage", "exchange_homepage"]  # noqa: E501
        if position not in allowed_values:
            raise ValueError(
                "Invalid value for `position` ({0}), must be one of {1}"  # noqa: E501
                .format(position, allowed_values)
            )

        self._position = position

    @property
    def language(self):
        """Gets the language of this PostBannerRequest.  # noqa: E501

        语种：中文zh_cn 英文en_us 马来文ms_my 韩文ko_kr 柬埔寨文km_kh  # noqa: E501

        :return: The language of this PostBannerRequest.  # noqa: E501
        :rtype: str
        """
        return self._language

    @language.setter
    def language(self, language):
        """Sets the language of this PostBannerRequest.

        语种：中文zh_cn 英文en_us 马来文ms_my 韩文ko_kr 柬埔寨文km_kh  # noqa: E501

        :param language: The language of this PostBannerRequest.  # noqa: E501
        :type: str
        """
        allowed_values = ["zh_cn", "en_us", "ms_my", "ko_kr", "km_kh"]  # noqa: E501
        if language not in allowed_values:
            raise ValueError(
                "Invalid value for `language` ({0}), must be one of {1}"  # noqa: E501
                .format(language, allowed_values)
            )

        self._language = language

    @property
    def order(self):
        """Gets the order of this PostBannerRequest.  # noqa: E501

        排序  # noqa: E501

        :return: The order of this PostBannerRequest.  # noqa: E501
        :rtype: int
        """
        return self._order

    @order.setter
    def order(self, order):
        """Sets the order of this PostBannerRequest.

        排序  # noqa: E501

        :param order: The order of this PostBannerRequest.  # noqa: E501
        :type: int
        """

        self._order = order

    @property
    def status(self):
        """Gets the status of this PostBannerRequest.  # noqa: E501

        状态  # noqa: E501

        :return: The status of this PostBannerRequest.  # noqa: E501
        :rtype: bool
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this PostBannerRequest.

        状态  # noqa: E501

        :param status: The status of this PostBannerRequest.  # noqa: E501
        :type: bool
        """

        self._status = status

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(PostBannerRequest, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, PostBannerRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other