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


class PostStaffRequest(object):
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
        'account': 'str',
        'real_name': 'str',
        'phone_number': 'str',
        'email_address': 'str'
    }

    attribute_map = {
        'account': 'account',
        'real_name': 'realName',
        'phone_number': 'phoneNumber',
        'email_address': 'emailAddress'
    }

    def __init__(self, account=None, real_name=None, phone_number=None, email_address=None):  # noqa: E501
        """PostStaffRequest - a model defined in Swagger"""  # noqa: E501

        self._account = None
        self._real_name = None
        self._phone_number = None
        self._email_address = None
        self.discriminator = None

        if account is not None:
            self.account = account
        if real_name is not None:
            self.real_name = real_name
        if phone_number is not None:
            self.phone_number = phone_number
        if email_address is not None:
            self.email_address = email_address

    @property
    def account(self):
        """Gets the account of this PostStaffRequest.  # noqa: E501

        账号  # noqa: E501

        :return: The account of this PostStaffRequest.  # noqa: E501
        :rtype: str
        """
        return self._account

    @account.setter
    def account(self, account):
        """Sets the account of this PostStaffRequest.

        账号  # noqa: E501

        :param account: The account of this PostStaffRequest.  # noqa: E501
        :type: str
        """
        if account is not None and len(account) > 64:
            raise ValueError("Invalid value for `account`, length must be less than or equal to `64`")  # noqa: E501

        self._account = account

    @property
    def real_name(self):
        """Gets the real_name of this PostStaffRequest.  # noqa: E501

        真实姓名  # noqa: E501

        :return: The real_name of this PostStaffRequest.  # noqa: E501
        :rtype: str
        """
        return self._real_name

    @real_name.setter
    def real_name(self, real_name):
        """Sets the real_name of this PostStaffRequest.

        真实姓名  # noqa: E501

        :param real_name: The real_name of this PostStaffRequest.  # noqa: E501
        :type: str
        """
        if real_name is not None and len(real_name) > 50:
            raise ValueError("Invalid value for `real_name`, length must be less than or equal to `50`")  # noqa: E501

        self._real_name = real_name

    @property
    def phone_number(self):
        """Gets the phone_number of this PostStaffRequest.  # noqa: E501

        手机号码  # noqa: E501

        :return: The phone_number of this PostStaffRequest.  # noqa: E501
        :rtype: str
        """
        return self._phone_number

    @phone_number.setter
    def phone_number(self, phone_number):
        """Sets the phone_number of this PostStaffRequest.

        手机号码  # noqa: E501

        :param phone_number: The phone_number of this PostStaffRequest.  # noqa: E501
        :type: str
        """
        if phone_number is not None and len(phone_number) > 16:
            raise ValueError("Invalid value for `phone_number`, length must be less than or equal to `16`")  # noqa: E501

        self._phone_number = phone_number

    @property
    def email_address(self):
        """Gets the email_address of this PostStaffRequest.  # noqa: E501

        邮箱地址  # noqa: E501

        :return: The email_address of this PostStaffRequest.  # noqa: E501
        :rtype: str
        """
        return self._email_address

    @email_address.setter
    def email_address(self, email_address):
        """Sets the email_address of this PostStaffRequest.

        邮箱地址  # noqa: E501

        :param email_address: The email_address of this PostStaffRequest.  # noqa: E501
        :type: str
        """
        if email_address is not None and len(email_address) > 64:
            raise ValueError("Invalid value for `email_address`, length must be less than or equal to `64`")  # noqa: E501

        self._email_address = email_address

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
        if issubclass(PostStaffRequest, dict):
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
        if not isinstance(other, PostStaffRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other