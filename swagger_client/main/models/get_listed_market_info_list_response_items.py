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


class GetListedMarketInfoListResponseItems(object):
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
        'logo': 'str',
        'name': 'str',
        'market_id': 'str',
        'trading_pair': 'str',
        'trading_area_id': 'str',
        'seller_coin_id': 'str',
        'buyer_coin_id': 'str'
    }

    attribute_map = {
        'id': 'id',
        'logo': 'logo',
        'name': 'name',
        'market_id': 'marketId',
        'trading_pair': 'tradingPair',
        'trading_area_id': 'tradingAreaId',
        'seller_coin_id': 'sellerCoinId',
        'buyer_coin_id': 'buyerCoinId'
    }

    def __init__(self, id=None, logo=None, name=None, market_id=None, trading_pair=None, trading_area_id=None, seller_coin_id=None, buyer_coin_id=None):  # noqa: E501
        """GetListedMarketInfoListResponseItems - a model defined in Swagger"""  # noqa: E501

        self._id = None
        self._logo = None
        self._name = None
        self._market_id = None
        self._trading_pair = None
        self._trading_area_id = None
        self._seller_coin_id = None
        self._buyer_coin_id = None
        self.discriminator = None

        if id is not None:
            self.id = id
        if logo is not None:
            self.logo = logo
        if name is not None:
            self.name = name
        if market_id is not None:
            self.market_id = market_id
        if trading_pair is not None:
            self.trading_pair = trading_pair
        if trading_area_id is not None:
            self.trading_area_id = trading_area_id
        if seller_coin_id is not None:
            self.seller_coin_id = seller_coin_id
        if buyer_coin_id is not None:
            self.buyer_coin_id = buyer_coin_id

    @property
    def id(self):
        """Gets the id of this GetListedMarketInfoListResponseItems.  # noqa: E501

        交易所id  # noqa: E501

        :return: The id of this GetListedMarketInfoListResponseItems.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this GetListedMarketInfoListResponseItems.

        交易所id  # noqa: E501

        :param id: The id of this GetListedMarketInfoListResponseItems.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def logo(self):
        """Gets the logo of this GetListedMarketInfoListResponseItems.  # noqa: E501

        交易所图标  # noqa: E501

        :return: The logo of this GetListedMarketInfoListResponseItems.  # noqa: E501
        :rtype: str
        """
        return self._logo

    @logo.setter
    def logo(self, logo):
        """Sets the logo of this GetListedMarketInfoListResponseItems.

        交易所图标  # noqa: E501

        :param logo: The logo of this GetListedMarketInfoListResponseItems.  # noqa: E501
        :type: str
        """

        self._logo = logo

    @property
    def name(self):
        """Gets the name of this GetListedMarketInfoListResponseItems.  # noqa: E501

        交易所名称  # noqa: E501

        :return: The name of this GetListedMarketInfoListResponseItems.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this GetListedMarketInfoListResponseItems.

        交易所名称  # noqa: E501

        :param name: The name of this GetListedMarketInfoListResponseItems.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def market_id(self):
        """Gets the market_id of this GetListedMarketInfoListResponseItems.  # noqa: E501

        市场id  # noqa: E501

        :return: The market_id of this GetListedMarketInfoListResponseItems.  # noqa: E501
        :rtype: str
        """
        return self._market_id

    @market_id.setter
    def market_id(self, market_id):
        """Sets the market_id of this GetListedMarketInfoListResponseItems.

        市场id  # noqa: E501

        :param market_id: The market_id of this GetListedMarketInfoListResponseItems.  # noqa: E501
        :type: str
        """

        self._market_id = market_id

    @property
    def trading_pair(self):
        """Gets the trading_pair of this GetListedMarketInfoListResponseItems.  # noqa: E501

        交易对  # noqa: E501

        :return: The trading_pair of this GetListedMarketInfoListResponseItems.  # noqa: E501
        :rtype: str
        """
        return self._trading_pair

    @trading_pair.setter
    def trading_pair(self, trading_pair):
        """Sets the trading_pair of this GetListedMarketInfoListResponseItems.

        交易对  # noqa: E501

        :param trading_pair: The trading_pair of this GetListedMarketInfoListResponseItems.  # noqa: E501
        :type: str
        """

        self._trading_pair = trading_pair

    @property
    def trading_area_id(self):
        """Gets the trading_area_id of this GetListedMarketInfoListResponseItems.  # noqa: E501

        交易分区id  # noqa: E501

        :return: The trading_area_id of this GetListedMarketInfoListResponseItems.  # noqa: E501
        :rtype: str
        """
        return self._trading_area_id

    @trading_area_id.setter
    def trading_area_id(self, trading_area_id):
        """Sets the trading_area_id of this GetListedMarketInfoListResponseItems.

        交易分区id  # noqa: E501

        :param trading_area_id: The trading_area_id of this GetListedMarketInfoListResponseItems.  # noqa: E501
        :type: str
        """

        self._trading_area_id = trading_area_id

    @property
    def seller_coin_id(self):
        """Gets the seller_coin_id of this GetListedMarketInfoListResponseItems.  # noqa: E501

        卖方币种ID  # noqa: E501

        :return: The seller_coin_id of this GetListedMarketInfoListResponseItems.  # noqa: E501
        :rtype: str
        """
        return self._seller_coin_id

    @seller_coin_id.setter
    def seller_coin_id(self, seller_coin_id):
        """Sets the seller_coin_id of this GetListedMarketInfoListResponseItems.

        卖方币种ID  # noqa: E501

        :param seller_coin_id: The seller_coin_id of this GetListedMarketInfoListResponseItems.  # noqa: E501
        :type: str
        """

        self._seller_coin_id = seller_coin_id

    @property
    def buyer_coin_id(self):
        """Gets the buyer_coin_id of this GetListedMarketInfoListResponseItems.  # noqa: E501

        买方币种ID  # noqa: E501

        :return: The buyer_coin_id of this GetListedMarketInfoListResponseItems.  # noqa: E501
        :rtype: str
        """
        return self._buyer_coin_id

    @buyer_coin_id.setter
    def buyer_coin_id(self, buyer_coin_id):
        """Sets the buyer_coin_id of this GetListedMarketInfoListResponseItems.

        买方币种ID  # noqa: E501

        :param buyer_coin_id: The buyer_coin_id of this GetListedMarketInfoListResponseItems.  # noqa: E501
        :type: str
        """

        self._buyer_coin_id = buyer_coin_id

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
        if issubclass(GetListedMarketInfoListResponseItems, dict):
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
        if not isinstance(other, GetListedMarketInfoListResponseItems):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
