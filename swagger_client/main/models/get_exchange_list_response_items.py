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


class GetExchangeListResponseItems(object):
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
        'id': 'str',
        'logo_url': 'str',
        'name': 'str',
        'cny_amount': 'str',
        'usd_amount': 'str',
        'trading_pair_count': 'int',
        'summary': 'str',
        'tags': 'str',
        'nationality': 'str',
        'concern_number': 'str',
        'favorites_status': 'bool'
    }

    attribute_map = {
        'id': 'id',
        'logo_url': 'logoUrl',
        'name': 'name',
        'cny_amount': 'cnyAmount',
        'usd_amount': 'usdAmount',
        'trading_pair_count': 'tradingPairCount',
        'summary': 'summary',
        'tags': 'tags',
        'nationality': 'nationality',
        'concern_number': 'concernNumber',
        'favorites_status': 'favoritesStatus'
    }

    def __init__(self, id=None, logo_url=None, name=None, cny_amount=None, usd_amount=None, trading_pair_count=None, summary=None, tags=None, nationality=None, concern_number=None, favorites_status=None):  # noqa: E501
        """GetExchangeListResponseItems - a model defined in Swagger"""  # noqa: E501

        self._id = None
        self._logo_url = None
        self._name = None
        self._cny_amount = None
        self._usd_amount = None
        self._trading_pair_count = None
        self._summary = None
        self._tags = None
        self._nationality = None
        self._concern_number = None
        self._favorites_status = None
        self.discriminator = None

        if id is not None:
            self.id = id
        if logo_url is not None:
            self.logo_url = logo_url
        if name is not None:
            self.name = name
        if cny_amount is not None:
            self.cny_amount = cny_amount
        if usd_amount is not None:
            self.usd_amount = usd_amount
        if trading_pair_count is not None:
            self.trading_pair_count = trading_pair_count
        if summary is not None:
            self.summary = summary
        if tags is not None:
            self.tags = tags
        if nationality is not None:
            self.nationality = nationality
        if concern_number is not None:
            self.concern_number = concern_number
        if favorites_status is not None:
            self.favorites_status = favorites_status

    @property
    def id(self):
        """Gets the id of this GetExchangeListResponseItems.  # noqa: E501

        交易所编号  # noqa: E501

        :return: The id of this GetExchangeListResponseItems.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this GetExchangeListResponseItems.

        交易所编号  # noqa: E501

        :param id: The id of this GetExchangeListResponseItems.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def logo_url(self):
        """Gets the logo_url of this GetExchangeListResponseItems.  # noqa: E501

        交易所logo路径  # noqa: E501

        :return: The logo_url of this GetExchangeListResponseItems.  # noqa: E501
        :rtype: str
        """
        return self._logo_url

    @logo_url.setter
    def logo_url(self, logo_url):
        """Sets the logo_url of this GetExchangeListResponseItems.

        交易所logo路径  # noqa: E501

        :param logo_url: The logo_url of this GetExchangeListResponseItems.  # noqa: E501
        :type: str
        """

        self._logo_url = logo_url

    @property
    def name(self):
        """Gets the name of this GetExchangeListResponseItems.  # noqa: E501

        交易所名称  # noqa: E501

        :return: The name of this GetExchangeListResponseItems.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this GetExchangeListResponseItems.

        交易所名称  # noqa: E501

        :param name: The name of this GetExchangeListResponseItems.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def cny_amount(self):
        """Gets the cny_amount of this GetExchangeListResponseItems.  # noqa: E501

        成交量(cny)  # noqa: E501

        :return: The cny_amount of this GetExchangeListResponseItems.  # noqa: E501
        :rtype: str
        """
        return self._cny_amount

    @cny_amount.setter
    def cny_amount(self, cny_amount):
        """Sets the cny_amount of this GetExchangeListResponseItems.

        成交量(cny)  # noqa: E501

        :param cny_amount: The cny_amount of this GetExchangeListResponseItems.  # noqa: E501
        :type: str
        """

        self._cny_amount = cny_amount

    @property
    def usd_amount(self):
        """Gets the usd_amount of this GetExchangeListResponseItems.  # noqa: E501

        成交量(usd)  # noqa: E501

        :return: The usd_amount of this GetExchangeListResponseItems.  # noqa: E501
        :rtype: str
        """
        return self._usd_amount

    @usd_amount.setter
    def usd_amount(self, usd_amount):
        """Sets the usd_amount of this GetExchangeListResponseItems.

        成交量(usd)  # noqa: E501

        :param usd_amount: The usd_amount of this GetExchangeListResponseItems.  # noqa: E501
        :type: str
        """

        self._usd_amount = usd_amount

    @property
    def trading_pair_count(self):
        """Gets the trading_pair_count of this GetExchangeListResponseItems.  # noqa: E501

        交易对数量  # noqa: E501

        :return: The trading_pair_count of this GetExchangeListResponseItems.  # noqa: E501
        :rtype: int
        """
        return self._trading_pair_count

    @trading_pair_count.setter
    def trading_pair_count(self, trading_pair_count):
        """Sets the trading_pair_count of this GetExchangeListResponseItems.

        交易对数量  # noqa: E501

        :param trading_pair_count: The trading_pair_count of this GetExchangeListResponseItems.  # noqa: E501
        :type: int
        """

        self._trading_pair_count = trading_pair_count

    @property
    def summary(self):
        """Gets the summary of this GetExchangeListResponseItems.  # noqa: E501

        简介  # noqa: E501

        :return: The summary of this GetExchangeListResponseItems.  # noqa: E501
        :rtype: str
        """
        return self._summary

    @summary.setter
    def summary(self, summary):
        """Sets the summary of this GetExchangeListResponseItems.

        简介  # noqa: E501

        :param summary: The summary of this GetExchangeListResponseItems.  # noqa: E501
        :type: str
        """

        self._summary = summary

    @property
    def tags(self):
        """Gets the tags of this GetExchangeListResponseItems.  # noqa: E501

        标签  # noqa: E501

        :return: The tags of this GetExchangeListResponseItems.  # noqa: E501
        :rtype: str
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """Sets the tags of this GetExchangeListResponseItems.

        标签  # noqa: E501

        :param tags: The tags of this GetExchangeListResponseItems.  # noqa: E501
        :type: str
        """

        self._tags = tags

    @property
    def nationality(self):
        """Gets the nationality of this GetExchangeListResponseItems.  # noqa: E501

        交易所国家  # noqa: E501

        :return: The nationality of this GetExchangeListResponseItems.  # noqa: E501
        :rtype: str
        """
        return self._nationality

    @nationality.setter
    def nationality(self, nationality):
        """Sets the nationality of this GetExchangeListResponseItems.

        交易所国家  # noqa: E501

        :param nationality: The nationality of this GetExchangeListResponseItems.  # noqa: E501
        :type: str
        """

        self._nationality = nationality

    @property
    def concern_number(self):
        """Gets the concern_number of this GetExchangeListResponseItems.  # noqa: E501

        关注度  # noqa: E501

        :return: The concern_number of this GetExchangeListResponseItems.  # noqa: E501
        :rtype: str
        """
        return self._concern_number

    @concern_number.setter
    def concern_number(self, concern_number):
        """Sets the concern_number of this GetExchangeListResponseItems.

        关注度  # noqa: E501

        :param concern_number: The concern_number of this GetExchangeListResponseItems.  # noqa: E501
        :type: str
        """

        self._concern_number = concern_number

    @property
    def favorites_status(self):
        """Gets the favorites_status of this GetExchangeListResponseItems.  # noqa: E501

        收藏状态  # noqa: E501

        :return: The favorites_status of this GetExchangeListResponseItems.  # noqa: E501
        :rtype: bool
        """
        return self._favorites_status

    @favorites_status.setter
    def favorites_status(self, favorites_status):
        """Sets the favorites_status of this GetExchangeListResponseItems.

        收藏状态  # noqa: E501

        :param favorites_status: The favorites_status of this GetExchangeListResponseItems.  # noqa: E501
        :type: bool
        """

        self._favorites_status = favorites_status

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
        if issubclass(GetExchangeListResponseItems, dict):
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
        if not isinstance(other, GetExchangeListResponseItems):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
