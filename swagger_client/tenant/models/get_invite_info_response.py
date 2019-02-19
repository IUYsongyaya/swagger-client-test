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


class GetInviteInfoResponse(object):
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
        'reward_total': 'str',
        'invite_total': 'str',
        'invite_code': 'str'
    }

    attribute_map = {
        'reward_total': 'rewardTotal',
        'invite_total': 'inviteTotal',
        'invite_code': 'inviteCode'
    }

    def __init__(self, reward_total=None, invite_total=None, invite_code=None):  # noqa: E501
        """GetInviteInfoResponse - a model defined in Swagger"""  # noqa: E501

        self._reward_total = None
        self._invite_total = None
        self._invite_code = None
        self.discriminator = None

        if reward_total is not None:
            self.reward_total = reward_total
        if invite_total is not None:
            self.invite_total = invite_total
        if invite_code is not None:
            self.invite_code = invite_code

    @property
    def reward_total(self):
        """Gets the reward_total of this GetInviteInfoResponse.  # noqa: E501

        累计奖励  # noqa: E501

        :return: The reward_total of this GetInviteInfoResponse.  # noqa: E501
        :rtype: str
        """
        return self._reward_total

    @reward_total.setter
    def reward_total(self, reward_total):
        """Sets the reward_total of this GetInviteInfoResponse.

        累计奖励  # noqa: E501

        :param reward_total: The reward_total of this GetInviteInfoResponse.  # noqa: E501
        :type: str
        """

        self._reward_total = reward_total

    @property
    def invite_total(self):
        """Gets the invite_total of this GetInviteInfoResponse.  # noqa: E501

        邀请用户  # noqa: E501

        :return: The invite_total of this GetInviteInfoResponse.  # noqa: E501
        :rtype: str
        """
        return self._invite_total

    @invite_total.setter
    def invite_total(self, invite_total):
        """Sets the invite_total of this GetInviteInfoResponse.

        邀请用户  # noqa: E501

        :param invite_total: The invite_total of this GetInviteInfoResponse.  # noqa: E501
        :type: str
        """

        self._invite_total = invite_total

    @property
    def invite_code(self):
        """Gets the invite_code of this GetInviteInfoResponse.  # noqa: E501

        邀请码  # noqa: E501

        :return: The invite_code of this GetInviteInfoResponse.  # noqa: E501
        :rtype: str
        """
        return self._invite_code

    @invite_code.setter
    def invite_code(self, invite_code):
        """Sets the invite_code of this GetInviteInfoResponse.

        邀请码  # noqa: E501

        :param invite_code: The invite_code of this GetInviteInfoResponse.  # noqa: E501
        :type: str
        """

        self._invite_code = invite_code

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
        if issubclass(GetInviteInfoResponse, dict):
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
        if not isinstance(other, GetInviteInfoResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other