# coding: utf-8

"""
    crush-main 平台接口（主平台）

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: 2.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class GetBannerListResponseItems(object):
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
        'url': 'str'
    }

    attribute_map = {
        'title': 'title',
        'banner': 'banner',
        'url': 'url'
    }

    def __init__(self, title=None, banner=None, url=None):  # noqa: E501
        """GetBannerListResponseItems - a model defined in Swagger"""  # noqa: E501

        self._title = None
        self._banner = None
        self._url = None
        self.discriminator = None

        if title is not None:
            self.title = title
        if banner is not None:
            self.banner = banner
        if url is not None:
            self.url = url

    @property
    def title(self):
        """Gets the title of this GetBannerListResponseItems.  # noqa: E501

        标题  # noqa: E501

        :return: The title of this GetBannerListResponseItems.  # noqa: E501
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title):
        """Sets the title of this GetBannerListResponseItems.

        标题  # noqa: E501

        :param title: The title of this GetBannerListResponseItems.  # noqa: E501
        :type: str
        """

        self._title = title

    @property
    def banner(self):
        """Gets the banner of this GetBannerListResponseItems.  # noqa: E501

        轮播图  # noqa: E501

        :return: The banner of this GetBannerListResponseItems.  # noqa: E501
        :rtype: str
        """
        return self._banner

    @banner.setter
    def banner(self, banner):
        """Sets the banner of this GetBannerListResponseItems.

        轮播图  # noqa: E501

        :param banner: The banner of this GetBannerListResponseItems.  # noqa: E501
        :type: str
        """

        self._banner = banner

    @property
    def url(self):
        """Gets the url of this GetBannerListResponseItems.  # noqa: E501

        跳转链接  # noqa: E501

        :return: The url of this GetBannerListResponseItems.  # noqa: E501
        :rtype: str
        """
        return self._url

    @url.setter
    def url(self, url):
        """Sets the url of this GetBannerListResponseItems.

        跳转链接  # noqa: E501

        :param url: The url of this GetBannerListResponseItems.  # noqa: E501
        :type: str
        """

        self._url = url

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
        if issubclass(GetBannerListResponseItems, dict):
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
        if not isinstance(other, GetBannerListResponseItems):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other