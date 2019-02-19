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


class GetProjectsResponseQuery(object):
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
        'sort_key': 'str'
    }

    attribute_map = {
        'sort_key': 'sortKey'
    }

    def __init__(self, sort_key=None):  # noqa: E501
        """GetProjectsResponseQuery - a model defined in Swagger"""  # noqa: E501

        self._sort_key = None
        self.discriminator = None

        if sort_key is not None:
            self.sort_key = sort_key

    @property
    def sort_key(self):
        """Gets the sort_key of this GetProjectsResponseQuery.  # noqa: E501

        排序依据,volume:24小时交易量,marketValue:市值  # noqa: E501

        :return: The sort_key of this GetProjectsResponseQuery.  # noqa: E501
        :rtype: str
        """
        return self._sort_key

    @sort_key.setter
    def sort_key(self, sort_key):
        """Sets the sort_key of this GetProjectsResponseQuery.

        排序依据,volume:24小时交易量,marketValue:市值  # noqa: E501

        :param sort_key: The sort_key of this GetProjectsResponseQuery.  # noqa: E501
        :type: str
        """
        allowed_values = ["volume", "marketValue"]  # noqa: E501
        if sort_key not in allowed_values:
            raise ValueError(
                "Invalid value for `sort_key` ({0}), must be one of {1}"  # noqa: E501
                .format(sort_key, allowed_values)
            )

        self._sort_key = sort_key

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
        if issubclass(GetProjectsResponseQuery, dict):
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
        if not isinstance(other, GetProjectsResponseQuery):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other