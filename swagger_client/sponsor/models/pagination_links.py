# coding: utf-8

"""
    crush-sponsor 平台接口（保荐方平台）

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: 2.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class PaginationLinks(object):
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
        'rel': 'str',
        'link': 'str'
    }

    attribute_map = {
        'rel': 'rel',
        'link': 'link'
    }

    def __init__(self, rel=None, link=None):  # noqa: E501
        """PaginationLinks - a model defined in Swagger"""  # noqa: E501

        self._rel = None
        self._link = None
        self.discriminator = None

        if rel is not None:
            self.rel = rel
        if link is not None:
            self.link = link

    @property
    def rel(self):
        """Gets the rel of this PaginationLinks.  # noqa: E501

        相对于  # noqa: E501

        :return: The rel of this PaginationLinks.  # noqa: E501
        :rtype: str
        """
        return self._rel

    @rel.setter
    def rel(self, rel):
        """Sets the rel of this PaginationLinks.

        相对于  # noqa: E501

        :param rel: The rel of this PaginationLinks.  # noqa: E501
        :type: str
        """
        allowed_values = ["self", "first", "previous", "next", "last"]  # noqa: E501
        if rel not in allowed_values:
            raise ValueError(
                "Invalid value for `rel` ({0}), must be one of {1}"  # noqa: E501
                .format(rel, allowed_values)
            )

        self._rel = rel

    @property
    def link(self):
        """Gets the link of this PaginationLinks.  # noqa: E501

        链接  # noqa: E501

        :return: The link of this PaginationLinks.  # noqa: E501
        :rtype: str
        """
        return self._link

    @link.setter
    def link(self, link):
        """Sets the link of this PaginationLinks.

        链接  # noqa: E501

        :param link: The link of this PaginationLinks.  # noqa: E501
        :type: str
        """

        self._link = link

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
        if issubclass(PaginationLinks, dict):
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
        if not isinstance(other, PaginationLinks):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other