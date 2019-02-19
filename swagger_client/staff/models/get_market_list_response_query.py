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


class GetMarketListResponseQuery(object):
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
        'market_mark': 'str'
    }

    attribute_map = {
        'market_mark': 'marketMark'
    }

    def __init__(self, market_mark=None):  # noqa: E501
        """GetMarketListResponseQuery - a model defined in Swagger"""  # noqa: E501

        self._market_mark = None
        self.discriminator = None

        if market_mark is not None:
            self.market_mark = market_mark

    @property
    def market_mark(self):
        """Gets the market_mark of this GetMarketListResponseQuery.  # noqa: E501

        市场标识  # noqa: E501

        :return: The market_mark of this GetMarketListResponseQuery.  # noqa: E501
        :rtype: str
        """
        return self._market_mark

    @market_mark.setter
    def market_mark(self, market_mark):
        """Sets the market_mark of this GetMarketListResponseQuery.

        市场标识  # noqa: E501

        :param market_mark: The market_mark of this GetMarketListResponseQuery.  # noqa: E501
        :type: str
        """

        self._market_mark = market_mark

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
        if issubclass(GetMarketListResponseQuery, dict):
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
        if not isinstance(other, GetMarketListResponseQuery):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other