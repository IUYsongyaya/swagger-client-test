# coding: utf-8

"""
    crush-tenant 平台接口(租户平台)

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: 2.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class GetDailyStatisticsResponseToday(object):
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
        'orders': 'int',
        'trade_number': 'int',
        'browse_users': 'int',
        'transaction_users': 'int',
        'activity_users': 'float'
    }

    attribute_map = {
        'orders': 'orders',
        'trade_number': 'tradeNumber',
        'browse_users': 'browseUsers',
        'transaction_users': 'transactionUsers',
        'activity_users': 'activityUsers'
    }

    def __init__(self, orders=None, trade_number=None, browse_users=None, transaction_users=None, activity_users=None):  # noqa: E501
        """GetDailyStatisticsResponseToday - a model defined in Swagger"""  # noqa: E501

        self._orders = None
        self._trade_number = None
        self._browse_users = None
        self._transaction_users = None
        self._activity_users = None
        self.discriminator = None

        if orders is not None:
            self.orders = orders
        if trade_number is not None:
            self.trade_number = trade_number
        if browse_users is not None:
            self.browse_users = browse_users
        if transaction_users is not None:
            self.transaction_users = transaction_users
        if activity_users is not None:
            self.activity_users = activity_users

    @property
    def orders(self):
        """Gets the orders of this GetDailyStatisticsResponseToday.  # noqa: E501

        订单量  # noqa: E501

        :return: The orders of this GetDailyStatisticsResponseToday.  # noqa: E501
        :rtype: int
        """
        return self._orders

    @orders.setter
    def orders(self, orders):
        """Sets the orders of this GetDailyStatisticsResponseToday.

        订单量  # noqa: E501

        :param orders: The orders of this GetDailyStatisticsResponseToday.  # noqa: E501
        :type: int
        """

        self._orders = orders

    @property
    def trade_number(self):
        """Gets the trade_number of this GetDailyStatisticsResponseToday.  # noqa: E501

        成交数量  # noqa: E501

        :return: The trade_number of this GetDailyStatisticsResponseToday.  # noqa: E501
        :rtype: int
        """
        return self._trade_number

    @trade_number.setter
    def trade_number(self, trade_number):
        """Sets the trade_number of this GetDailyStatisticsResponseToday.

        成交数量  # noqa: E501

        :param trade_number: The trade_number of this GetDailyStatisticsResponseToday.  # noqa: E501
        :type: int
        """

        self._trade_number = trade_number

    @property
    def browse_users(self):
        """Gets the browse_users of this GetDailyStatisticsResponseToday.  # noqa: E501

        浏览用户  # noqa: E501

        :return: The browse_users of this GetDailyStatisticsResponseToday.  # noqa: E501
        :rtype: int
        """
        return self._browse_users

    @browse_users.setter
    def browse_users(self, browse_users):
        """Sets the browse_users of this GetDailyStatisticsResponseToday.

        浏览用户  # noqa: E501

        :param browse_users: The browse_users of this GetDailyStatisticsResponseToday.  # noqa: E501
        :type: int
        """

        self._browse_users = browse_users

    @property
    def transaction_users(self):
        """Gets the transaction_users of this GetDailyStatisticsResponseToday.  # noqa: E501

        交易用户  # noqa: E501

        :return: The transaction_users of this GetDailyStatisticsResponseToday.  # noqa: E501
        :rtype: int
        """
        return self._transaction_users

    @transaction_users.setter
    def transaction_users(self, transaction_users):
        """Sets the transaction_users of this GetDailyStatisticsResponseToday.

        交易用户  # noqa: E501

        :param transaction_users: The transaction_users of this GetDailyStatisticsResponseToday.  # noqa: E501
        :type: int
        """

        self._transaction_users = transaction_users

    @property
    def activity_users(self):
        """Gets the activity_users of this GetDailyStatisticsResponseToday.  # noqa: E501

        用户活跃度  # noqa: E501

        :return: The activity_users of this GetDailyStatisticsResponseToday.  # noqa: E501
        :rtype: float
        """
        return self._activity_users

    @activity_users.setter
    def activity_users(self, activity_users):
        """Sets the activity_users of this GetDailyStatisticsResponseToday.

        用户活跃度  # noqa: E501

        :param activity_users: The activity_users of this GetDailyStatisticsResponseToday.  # noqa: E501
        :type: float
        """

        self._activity_users = activity_users

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
        if issubclass(GetDailyStatisticsResponseToday, dict):
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
        if not isinstance(other, GetDailyStatisticsResponseToday):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other