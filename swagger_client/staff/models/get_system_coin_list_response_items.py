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


class GetSystemCoinListResponseItems(object):
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
        'coin_id': 'str',
        'coin_name': 'str',
        'create_at': 'str',
        'rechargeable': 'bool',
        'withdrawable': 'bool',
        'warning': 'str',
        'initialized': 'bool'
    }

    attribute_map = {
        'id': 'id',
        'coin_id': 'coinId',
        'coin_name': 'coinName',
        'create_at': 'createAt',
        'rechargeable': 'rechargeable',
        'withdrawable': 'withdrawable',
        'warning': 'warning',
        'initialized': 'initialized'
    }

    def __init__(self, id=None, coin_id=None, coin_name=None, create_at=None, rechargeable=None, withdrawable=None, warning=None, initialized=None):  # noqa: E501
        """GetSystemCoinListResponseItems - a model defined in Swagger"""  # noqa: E501

        self._id = None
        self._coin_id = None
        self._coin_name = None
        self._create_at = None
        self._rechargeable = None
        self._withdrawable = None
        self._warning = None
        self._initialized = None
        self.discriminator = None

        if id is not None:
            self.id = id
        if coin_id is not None:
            self.coin_id = coin_id
        if coin_name is not None:
            self.coin_name = coin_name
        if create_at is not None:
            self.create_at = create_at
        if rechargeable is not None:
            self.rechargeable = rechargeable
        if withdrawable is not None:
            self.withdrawable = withdrawable
        if warning is not None:
            self.warning = warning
        if initialized is not None:
            self.initialized = initialized

    @property
    def id(self):
        """Gets the id of this GetSystemCoinListResponseItems.  # noqa: E501

        id  # noqa: E501

        :return: The id of this GetSystemCoinListResponseItems.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this GetSystemCoinListResponseItems.

        id  # noqa: E501

        :param id: The id of this GetSystemCoinListResponseItems.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def coin_id(self):
        """Gets the coin_id of this GetSystemCoinListResponseItems.  # noqa: E501

        币id  # noqa: E501

        :return: The coin_id of this GetSystemCoinListResponseItems.  # noqa: E501
        :rtype: str
        """
        return self._coin_id

    @coin_id.setter
    def coin_id(self, coin_id):
        """Sets the coin_id of this GetSystemCoinListResponseItems.

        币id  # noqa: E501

        :param coin_id: The coin_id of this GetSystemCoinListResponseItems.  # noqa: E501
        :type: str
        """

        self._coin_id = coin_id

    @property
    def coin_name(self):
        """Gets the coin_name of this GetSystemCoinListResponseItems.  # noqa: E501

        币简称  # noqa: E501

        :return: The coin_name of this GetSystemCoinListResponseItems.  # noqa: E501
        :rtype: str
        """
        return self._coin_name

    @coin_name.setter
    def coin_name(self, coin_name):
        """Sets the coin_name of this GetSystemCoinListResponseItems.

        币简称  # noqa: E501

        :param coin_name: The coin_name of this GetSystemCoinListResponseItems.  # noqa: E501
        :type: str
        """

        self._coin_name = coin_name

    @property
    def create_at(self):
        """Gets the create_at of this GetSystemCoinListResponseItems.  # noqa: E501

        创建时间  # noqa: E501

        :return: The create_at of this GetSystemCoinListResponseItems.  # noqa: E501
        :rtype: str
        """
        return self._create_at

    @create_at.setter
    def create_at(self, create_at):
        """Sets the create_at of this GetSystemCoinListResponseItems.

        创建时间  # noqa: E501

        :param create_at: The create_at of this GetSystemCoinListResponseItems.  # noqa: E501
        :type: str
        """

        self._create_at = create_at

    @property
    def rechargeable(self):
        """Gets the rechargeable of this GetSystemCoinListResponseItems.  # noqa: E501

        充币开关  # noqa: E501

        :return: The rechargeable of this GetSystemCoinListResponseItems.  # noqa: E501
        :rtype: bool
        """
        return self._rechargeable

    @rechargeable.setter
    def rechargeable(self, rechargeable):
        """Sets the rechargeable of this GetSystemCoinListResponseItems.

        充币开关  # noqa: E501

        :param rechargeable: The rechargeable of this GetSystemCoinListResponseItems.  # noqa: E501
        :type: bool
        """

        self._rechargeable = rechargeable

    @property
    def withdrawable(self):
        """Gets the withdrawable of this GetSystemCoinListResponseItems.  # noqa: E501

        提币开关  # noqa: E501

        :return: The withdrawable of this GetSystemCoinListResponseItems.  # noqa: E501
        :rtype: bool
        """
        return self._withdrawable

    @withdrawable.setter
    def withdrawable(self, withdrawable):
        """Sets the withdrawable of this GetSystemCoinListResponseItems.

        提币开关  # noqa: E501

        :param withdrawable: The withdrawable of this GetSystemCoinListResponseItems.  # noqa: E501
        :type: bool
        """

        self._withdrawable = withdrawable

    @property
    def warning(self):
        """Gets the warning of this GetSystemCoinListResponseItems.  # noqa: E501

        警示信息  # noqa: E501

        :return: The warning of this GetSystemCoinListResponseItems.  # noqa: E501
        :rtype: str
        """
        return self._warning

    @warning.setter
    def warning(self, warning):
        """Sets the warning of this GetSystemCoinListResponseItems.

        警示信息  # noqa: E501

        :param warning: The warning of this GetSystemCoinListResponseItems.  # noqa: E501
        :type: str
        """

        self._warning = warning

    @property
    def initialized(self):
        """Gets the initialized of this GetSystemCoinListResponseItems.  # noqa: E501

        是否初始化  # noqa: E501

        :return: The initialized of this GetSystemCoinListResponseItems.  # noqa: E501
        :rtype: bool
        """
        return self._initialized

    @initialized.setter
    def initialized(self, initialized):
        """Sets the initialized of this GetSystemCoinListResponseItems.

        是否初始化  # noqa: E501

        :param initialized: The initialized of this GetSystemCoinListResponseItems.  # noqa: E501
        :type: bool
        """

        self._initialized = initialized

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
        if issubclass(GetSystemCoinListResponseItems, dict):
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
        if not isinstance(other, GetSystemCoinListResponseItems):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other