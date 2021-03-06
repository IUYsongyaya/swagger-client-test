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


class PostLoginRequest(object):
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
        'password': 'str',
        'challenge': 'str',
        'seccode': 'str',
        'validate': 'str'
    }

    attribute_map = {
        'account': 'account',
        'password': 'password',
        'challenge': 'challenge',
        'seccode': 'seccode',
        'validate': 'validate'
    }

    def __init__(self, account=None, password=None, challenge=None, seccode=None, validate=None):  # noqa: E501
        """PostLoginRequest - a model defined in Swagger"""  # noqa: E501

        self._account = None
        self._password = None
        self._challenge = None
        self._seccode = None
        self._validate = None
        self.discriminator = None

        self.account = account
        self.password = password
        self.challenge = challenge
        self.seccode = seccode
        self.validate = validate

    @property
    def account(self):
        """Gets the account of this PostLoginRequest.  # noqa: E501

        邮箱或者手机号吗  # noqa: E501

        :return: The account of this PostLoginRequest.  # noqa: E501
        :rtype: str
        """
        return self._account

    @account.setter
    def account(self, account):
        """Sets the account of this PostLoginRequest.

        邮箱或者手机号吗  # noqa: E501

        :param account: The account of this PostLoginRequest.  # noqa: E501
        :type: str
        """
        if account is None:
            raise ValueError("Invalid value for `account`, must not be `None`")  # noqa: E501
        if account is not None and len(account) > 64:
            raise ValueError("Invalid value for `account`, length must be less than or equal to `64`")  # noqa: E501
        if account is not None and len(account) < 8:
            raise ValueError("Invalid value for `account`, length must be greater than or equal to `8`")  # noqa: E501

        self._account = account

    @property
    def password(self):
        """Gets the password of this PostLoginRequest.  # noqa: E501

        密码  # noqa: E501

        :return: The password of this PostLoginRequest.  # noqa: E501
        :rtype: str
        """
        return self._password

    @password.setter
    def password(self, password):
        """Sets the password of this PostLoginRequest.

        密码  # noqa: E501

        :param password: The password of this PostLoginRequest.  # noqa: E501
        :type: str
        """
        if password is None:
            raise ValueError("Invalid value for `password`, must not be `None`")  # noqa: E501
        if password is not None and len(password) > 16:
            raise ValueError("Invalid value for `password`, length must be less than or equal to `16`")  # noqa: E501
        if password is not None and len(password) < 8:
            raise ValueError("Invalid value for `password`, length must be greater than or equal to `8`")  # noqa: E501

        self._password = password

    @property
    def challenge(self):
        """Gets the challenge of this PostLoginRequest.  # noqa: E501

        极验参数  # noqa: E501

        :return: The challenge of this PostLoginRequest.  # noqa: E501
        :rtype: str
        """
        return self._challenge

    @challenge.setter
    def challenge(self, challenge):
        """Sets the challenge of this PostLoginRequest.

        极验参数  # noqa: E501

        :param challenge: The challenge of this PostLoginRequest.  # noqa: E501
        :type: str
        """
        if challenge is None:
            raise ValueError("Invalid value for `challenge`, must not be `None`")  # noqa: E501

        self._challenge = challenge

    @property
    def seccode(self):
        """Gets the seccode of this PostLoginRequest.  # noqa: E501

        极验参数  # noqa: E501

        :return: The seccode of this PostLoginRequest.  # noqa: E501
        :rtype: str
        """
        return self._seccode

    @seccode.setter
    def seccode(self, seccode):
        """Sets the seccode of this PostLoginRequest.

        极验参数  # noqa: E501

        :param seccode: The seccode of this PostLoginRequest.  # noqa: E501
        :type: str
        """
        if seccode is None:
            raise ValueError("Invalid value for `seccode`, must not be `None`")  # noqa: E501

        self._seccode = seccode

    @property
    def validate(self):
        """Gets the validate of this PostLoginRequest.  # noqa: E501

        极验参数  # noqa: E501

        :return: The validate of this PostLoginRequest.  # noqa: E501
        :rtype: str
        """
        return self._validate

    @validate.setter
    def validate(self, validate):
        """Sets the validate of this PostLoginRequest.

        极验参数  # noqa: E501

        :param validate: The validate of this PostLoginRequest.  # noqa: E501
        :type: str
        """
        if validate is None:
            raise ValueError("Invalid value for `validate`, must not be `None`")  # noqa: E501

        self._validate = validate

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
        if issubclass(PostLoginRequest, dict):
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
        if not isinstance(other, PostLoginRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
