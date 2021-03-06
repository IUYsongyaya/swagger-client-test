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

from swagger_client.tenant.models.face_id_result_response_verify_result_result_faceid_thresholds import FaceIdResultResponseVerifyResultResultFaceidThresholds  # noqa: F401,E501


class FaceIdResultResponseVerifyResultResultFaceid(object):
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
        'confidence': 'float',
        'thresholds': 'FaceIdResultResponseVerifyResultResultFaceidThresholds'
    }

    attribute_map = {
        'confidence': 'confidence',
        'thresholds': 'thresholds'
    }

    def __init__(self, confidence=None, thresholds=None):  # noqa: E501
        """FaceIdResultResponseVerifyResultResultFaceid - a model defined in Swagger"""  # noqa: E501

        self._confidence = None
        self._thresholds = None
        self.discriminator = None

        if confidence is not None:
            self.confidence = confidence
        if thresholds is not None:
            self.thresholds = thresholds

    @property
    def confidence(self):
        """Gets the confidence of this FaceIdResultResponseVerifyResultResultFaceid.  # noqa: E501


        :return: The confidence of this FaceIdResultResponseVerifyResultResultFaceid.  # noqa: E501
        :rtype: float
        """
        return self._confidence

    @confidence.setter
    def confidence(self, confidence):
        """Sets the confidence of this FaceIdResultResponseVerifyResultResultFaceid.


        :param confidence: The confidence of this FaceIdResultResponseVerifyResultResultFaceid.  # noqa: E501
        :type: float
        """

        self._confidence = confidence

    @property
    def thresholds(self):
        """Gets the thresholds of this FaceIdResultResponseVerifyResultResultFaceid.  # noqa: E501


        :return: The thresholds of this FaceIdResultResponseVerifyResultResultFaceid.  # noqa: E501
        :rtype: FaceIdResultResponseVerifyResultResultFaceidThresholds
        """
        return self._thresholds

    @thresholds.setter
    def thresholds(self, thresholds):
        """Sets the thresholds of this FaceIdResultResponseVerifyResultResultFaceid.


        :param thresholds: The thresholds of this FaceIdResultResponseVerifyResultResultFaceid.  # noqa: E501
        :type: FaceIdResultResponseVerifyResultResultFaceidThresholds
        """

        self._thresholds = thresholds

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
        if issubclass(FaceIdResultResponseVerifyResultResultFaceid, dict):
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
        if not isinstance(other, FaceIdResultResponseVerifyResultResultFaceid):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
