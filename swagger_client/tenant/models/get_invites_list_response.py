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

from swagger_client.tenant.models.get_invites_list_response_items import GetInvitesListResponseItems  # noqa: F401,E501
from swagger_client.tenant.models.pagination import Pagination  # noqa: F401,E501


class GetInvitesListResponse(object):
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
        'meta': 'Pagination',
        'items': 'list[GetInvitesListResponseItems]'
    }

    attribute_map = {
        'meta': 'meta',
        'items': 'items'
    }

    def __init__(self, meta=None, items=None):  # noqa: E501
        """GetInvitesListResponse - a model defined in Swagger"""  # noqa: E501

        self._meta = None
        self._items = None
        self.discriminator = None

        if meta is not None:
            self.meta = meta
        if items is not None:
            self.items = items

    @property
    def meta(self):
        """Gets the meta of this GetInvitesListResponse.  # noqa: E501


        :return: The meta of this GetInvitesListResponse.  # noqa: E501
        :rtype: Pagination
        """
        return self._meta

    @meta.setter
    def meta(self, meta):
        """Sets the meta of this GetInvitesListResponse.


        :param meta: The meta of this GetInvitesListResponse.  # noqa: E501
        :type: Pagination
        """

        self._meta = meta

    @property
    def items(self):
        """Gets the items of this GetInvitesListResponse.  # noqa: E501

        邀请记录  # noqa: E501

        :return: The items of this GetInvitesListResponse.  # noqa: E501
        :rtype: list[GetInvitesListResponseItems]
        """
        return self._items

    @items.setter
    def items(self, items):
        """Sets the items of this GetInvitesListResponse.

        邀请记录  # noqa: E501

        :param items: The items of this GetInvitesListResponse.  # noqa: E501
        :type: list[GetInvitesListResponseItems]
        """

        self._items = items

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
        if issubclass(GetInvitesListResponse, dict):
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
        if not isinstance(other, GetInvitesListResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other