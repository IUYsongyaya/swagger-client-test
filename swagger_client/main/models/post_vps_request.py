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


class PostVPSRequest(object):
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
        'ip': 'str',
        'port': 'int',
        'remark': 'str'
    }

    attribute_map = {
        'ip': 'ip',
        'port': 'port',
        'remark': 'remark'
    }

    def __init__(self, ip=None, port=None, remark=None):  # noqa: E501
        """PostVPSRequest - a model defined in Swagger"""  # noqa: E501

        self._ip = None
        self._port = None
        self._remark = None
        self.discriminator = None

        if ip is not None:
            self.ip = ip
        if port is not None:
            self.port = port
        if remark is not None:
            self.remark = remark

    @property
    def ip(self):
        """Gets the ip of this PostVPSRequest.  # noqa: E501

        vps ip  # noqa: E501

        :return: The ip of this PostVPSRequest.  # noqa: E501
        :rtype: str
        """
        return self._ip

    @ip.setter
    def ip(self, ip):
        """Sets the ip of this PostVPSRequest.

        vps ip  # noqa: E501

        :param ip: The ip of this PostVPSRequest.  # noqa: E501
        :type: str
        """

        self._ip = ip

    @property
    def port(self):
        """Gets the port of this PostVPSRequest.  # noqa: E501

        端口号  # noqa: E501

        :return: The port of this PostVPSRequest.  # noqa: E501
        :rtype: int
        """
        return self._port

    @port.setter
    def port(self, port):
        """Sets the port of this PostVPSRequest.

        端口号  # noqa: E501

        :param port: The port of this PostVPSRequest.  # noqa: E501
        :type: int
        """

        self._port = port

    @property
    def remark(self):
        """Gets the remark of this PostVPSRequest.  # noqa: E501

        备注  # noqa: E501

        :return: The remark of this PostVPSRequest.  # noqa: E501
        :rtype: str
        """
        return self._remark

    @remark.setter
    def remark(self, remark):
        """Sets the remark of this PostVPSRequest.

        备注  # noqa: E501

        :param remark: The remark of this PostVPSRequest.  # noqa: E501
        :type: str
        """

        self._remark = remark

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
        if issubclass(PostVPSRequest, dict):
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
        if not isinstance(other, PostVPSRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
