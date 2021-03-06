# coding: utf-8

"""
    crush-sponsor 平台接口（保荐方平台）

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: 2.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class PostVerifyRequest(object):
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
        'user_name': 'str',
        'uri': 'str',
        'code': 'str',
        'type': 'str'
    }

    attribute_map = {
        'user_name': 'userName',
        'uri': 'uri',
        'code': 'code',
        'type': 'type'
    }

    def __init__(self, user_name=None, uri=None, code=None, type=None):  # noqa: E501
        """PostVerifyRequest - a model defined in Swagger"""  # noqa: E501

        self._user_name = None
        self._uri = None
        self._code = None
        self._type = None
        self.discriminator = None

        self.user_name = user_name
        self.uri = uri
        self.code = code
        self.type = type

    @property
    def user_name(self):
        """Gets the user_name of this PostVerifyRequest.  # noqa: E501

        账号  # noqa: E501

        :return: The user_name of this PostVerifyRequest.  # noqa: E501
        :rtype: str
        """
        return self._user_name

    @user_name.setter
    def user_name(self, user_name):
        """Sets the user_name of this PostVerifyRequest.

        账号  # noqa: E501

        :param user_name: The user_name of this PostVerifyRequest.  # noqa: E501
        :type: str
        """
        if user_name is None:
            raise ValueError("Invalid value for `user_name`, must not be `None`")  # noqa: E501

        self._user_name = user_name

    @property
    def uri(self):
        """Gets the uri of this PostVerifyRequest.  # noqa: E501

        账号，邮箱不超过64个字符，手机不超过16  # noqa: E501

        :return: The uri of this PostVerifyRequest.  # noqa: E501
        :rtype: str
        """
        return self._uri

    @uri.setter
    def uri(self, uri):
        """Sets the uri of this PostVerifyRequest.

        账号，邮箱不超过64个字符，手机不超过16  # noqa: E501

        :param uri: The uri of this PostVerifyRequest.  # noqa: E501
        :type: str
        """
        if uri is None:
            raise ValueError("Invalid value for `uri`, must not be `None`")  # noqa: E501
        if uri is not None and len(uri) > 64:
            raise ValueError("Invalid value for `uri`, length must be less than or equal to `64`")  # noqa: E501
        if uri is not None and len(uri) < 16:
            raise ValueError("Invalid value for `uri`, length must be greater than or equal to `16`")  # noqa: E501

        self._uri = uri

    @property
    def code(self):
        """Gets the code of this PostVerifyRequest.  # noqa: E501

        验证码  # noqa: E501

        :return: The code of this PostVerifyRequest.  # noqa: E501
        :rtype: str
        """
        return self._code

    @code.setter
    def code(self, code):
        """Sets the code of this PostVerifyRequest.

        验证码  # noqa: E501

        :param code: The code of this PostVerifyRequest.  # noqa: E501
        :type: str
        """
        if code is None:
            raise ValueError("Invalid value for `code`, must not be `None`")  # noqa: E501
        if code is not None and len(code) > 6:
            raise ValueError("Invalid value for `code`, length must be less than or equal to `6`")  # noqa: E501
        if code is not None and len(code) < 6:
            raise ValueError("Invalid value for `code`, length must be greater than or equal to `6`")  # noqa: E501

        self._code = code

    @property
    def type(self):
        """Gets the type of this PostVerifyRequest.  # noqa: E501

        验证码类型,根据类型调用不同的短信模板  # noqa: E501

        :return: The type of this PostVerifyRequest.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this PostVerifyRequest.

        验证码类型,根据类型调用不同的短信模板  # noqa: E501

        :param type: The type of this PostVerifyRequest.  # noqa: E501
        :type: str
        """
        if type is None:
            raise ValueError("Invalid value for `type`, must not be `None`")  # noqa: E501
        allowed_values = ["login", "forget_pwd", "edit_login_pwd"]  # noqa: E501
        if type not in allowed_values:
            raise ValueError(
                "Invalid value for `type` ({0}), must be one of {1}"  # noqa: E501
                .format(type, allowed_values)
            )

        self._type = type

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
        if issubclass(PostVerifyRequest, dict):
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
        if not isinstance(other, PostVerifyRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
