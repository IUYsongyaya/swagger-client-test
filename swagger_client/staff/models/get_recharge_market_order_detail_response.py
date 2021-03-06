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


class GetRechargeMarketOrderDetailResponse(object):
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
        'market': 'str',
        'time': 'str',
        'price': 'str'
    }

    attribute_map = {
        'market': 'market',
        'time': 'time',
        'price': 'price'
    }

    def __init__(self, market=None, time=None, price=None):  # noqa: E501
        """GetRechargeMarketOrderDetailResponse - a model defined in Swagger"""  # noqa: E501

        self._market = None
        self._time = None
        self._price = None
        self.discriminator = None

        if market is not None:
            self.market = market
        if time is not None:
            self.time = time
        if price is not None:
            self.price = price

    @property
    def market(self):
        """Gets the market of this GetRechargeMarketOrderDetailResponse.  # noqa: E501

        市场  # noqa: E501

        :return: The market of this GetRechargeMarketOrderDetailResponse.  # noqa: E501
        :rtype: str
        """
        return self._market

    @market.setter
    def market(self, market):
        """Sets the market of this GetRechargeMarketOrderDetailResponse.

        市场  # noqa: E501

        :param market: The market of this GetRechargeMarketOrderDetailResponse.  # noqa: E501
        :type: str
        """

        self._market = market

    @property
    def time(self):
        """Gets the time of this GetRechargeMarketOrderDetailResponse.  # noqa: E501

        时长  # noqa: E501

        :return: The time of this GetRechargeMarketOrderDetailResponse.  # noqa: E501
        :rtype: str
        """
        return self._time

    @time.setter
    def time(self, time):
        """Sets the time of this GetRechargeMarketOrderDetailResponse.

        时长  # noqa: E501

        :param time: The time of this GetRechargeMarketOrderDetailResponse.  # noqa: E501
        :type: str
        """

        self._time = time

    @property
    def price(self):
        """Gets the price of this GetRechargeMarketOrderDetailResponse.  # noqa: E501

        价格  # noqa: E501

        :return: The price of this GetRechargeMarketOrderDetailResponse.  # noqa: E501
        :rtype: str
        """
        return self._price

    @price.setter
    def price(self, price):
        """Sets the price of this GetRechargeMarketOrderDetailResponse.

        价格  # noqa: E501

        :param price: The price of this GetRechargeMarketOrderDetailResponse.  # noqa: E501
        :type: str
        """

        self._price = price

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
        if issubclass(GetRechargeMarketOrderDetailResponse, dict):
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
        if not isinstance(other, GetRechargeMarketOrderDetailResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
