# coding: utf-8

"""
    crush-venture 平台接口（项目方平台）

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: 2.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class PutProjectRequestSetting(object):
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
        'open': 'bool',
        'access_method': 'str'
    }

    attribute_map = {
        'open': 'open',
        'access_method': 'accessMethod'
    }

    def __init__(self, open=None, access_method=None):  # noqa: E501
        """PutProjectRequestSetting - a model defined in Swagger"""  # noqa: E501

        self._open = None
        self._access_method = None
        self.discriminator = None

        if open is not None:
            self.open = open
        if access_method is not None:
            self.access_method = access_method

    @property
    def open(self):
        """Gets the open of this PutProjectRequestSetting.  # noqa: E501

        是否公示  # noqa: E501

        :return: The open of this PutProjectRequestSetting.  # noqa: E501
        :rtype: bool
        """
        return self._open

    @open.setter
    def open(self, open):
        """Sets the open of this PutProjectRequestSetting.

        是否公示  # noqa: E501

        :param open: The open of this PutProjectRequestSetting.  # noqa: E501
        :type: bool
        """

        self._open = open

    @property
    def access_method(self):
        """Gets the access_method of this PutProjectRequestSetting.  # noqa: E501

        接入方式（refuse：拒绝接入、verification：需要验证、accept：无需验证）  # noqa: E501

        :return: The access_method of this PutProjectRequestSetting.  # noqa: E501
        :rtype: str
        """
        return self._access_method

    @access_method.setter
    def access_method(self, access_method):
        """Sets the access_method of this PutProjectRequestSetting.

        接入方式（refuse：拒绝接入、verification：需要验证、accept：无需验证）  # noqa: E501

        :param access_method: The access_method of this PutProjectRequestSetting.  # noqa: E501
        :type: str
        """
        allowed_values = ["refuse", "verification", "accept"]  # noqa: E501
        if access_method not in allowed_values:
            raise ValueError(
                "Invalid value for `access_method` ({0}), must be one of {1}"  # noqa: E501
                .format(access_method, allowed_values)
            )

        self._access_method = access_method

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
        if issubclass(PutProjectRequestSetting, dict):
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
        if not isinstance(other, PutProjectRequestSetting):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
