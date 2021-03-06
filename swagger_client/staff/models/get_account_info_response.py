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

from swagger_client.staff.models.get_account_info_response_basic_info import GetAccountInfoResponseBasicInfo  # noqa: F401,E501


class GetAccountInfoResponse(object):
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
        'basic_info': 'GetAccountInfoResponseBasicInfo'
    }

    attribute_map = {
        'basic_info': 'basicInfo'
    }

    def __init__(self, basic_info=None):  # noqa: E501
        """GetAccountInfoResponse - a model defined in Swagger"""  # noqa: E501

        self._basic_info = None
        self.discriminator = None

        if basic_info is not None:
            self.basic_info = basic_info

    @property
    def basic_info(self):
        """Gets the basic_info of this GetAccountInfoResponse.  # noqa: E501


        :return: The basic_info of this GetAccountInfoResponse.  # noqa: E501
        :rtype: GetAccountInfoResponseBasicInfo
        """
        return self._basic_info

    @basic_info.setter
    def basic_info(self, basic_info):
        """Sets the basic_info of this GetAccountInfoResponse.


        :param basic_info: The basic_info of this GetAccountInfoResponse.  # noqa: E501
        :type: GetAccountInfoResponseBasicInfo
        """

        self._basic_info = basic_info

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
        if issubclass(GetAccountInfoResponse, dict):
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
        if not isinstance(other, GetAccountInfoResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
