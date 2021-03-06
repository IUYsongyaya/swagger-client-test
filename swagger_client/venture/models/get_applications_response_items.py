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


class GetApplicationsResponseItems(object):
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
        'project_name': 'str',
        'short_name': 'str',
        'fullname': 'str',
        'coin_logo_key': 'str',
        'coin_logo_url': 'str',
        'applied_at': 'datetime',
        'status': 'str',
        'remarks': 'str',
        'audited_at': 'datetime'
    }

    attribute_map = {
        'id': 'id',
        'project_name': 'projectName',
        'short_name': 'shortName',
        'fullname': 'fullname',
        'coin_logo_key': 'coinLogoKey',
        'coin_logo_url': 'coinLogoUrl',
        'applied_at': 'appliedAt',
        'status': 'status',
        'remarks': 'remarks',
        'audited_at': 'auditedAt'
    }

    def __init__(self, id=None, project_name=None, short_name=None, fullname=None, coin_logo_key=None, coin_logo_url=None, applied_at=None, status=None, remarks=None, audited_at=None):  # noqa: E501
        """GetApplicationsResponseItems - a model defined in Swagger"""  # noqa: E501

        self._id = None
        self._project_name = None
        self._short_name = None
        self._fullname = None
        self._coin_logo_key = None
        self._coin_logo_url = None
        self._applied_at = None
        self._status = None
        self._remarks = None
        self._audited_at = None
        self.discriminator = None

        if id is not None:
            self.id = id
        if project_name is not None:
            self.project_name = project_name
        if short_name is not None:
            self.short_name = short_name
        if fullname is not None:
            self.fullname = fullname
        if coin_logo_key is not None:
            self.coin_logo_key = coin_logo_key
        if coin_logo_url is not None:
            self.coin_logo_url = coin_logo_url
        if applied_at is not None:
            self.applied_at = applied_at
        if status is not None:
            self.status = status
        if remarks is not None:
            self.remarks = remarks
        if audited_at is not None:
            self.audited_at = audited_at

    @property
    def id(self):
        """Gets the id of this GetApplicationsResponseItems.  # noqa: E501

        申请ID  # noqa: E501

        :return: The id of this GetApplicationsResponseItems.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this GetApplicationsResponseItems.

        申请ID  # noqa: E501

        :param id: The id of this GetApplicationsResponseItems.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def project_name(self):
        """Gets the project_name of this GetApplicationsResponseItems.  # noqa: E501

        项目名称  # noqa: E501

        :return: The project_name of this GetApplicationsResponseItems.  # noqa: E501
        :rtype: str
        """
        return self._project_name

    @project_name.setter
    def project_name(self, project_name):
        """Sets the project_name of this GetApplicationsResponseItems.

        项目名称  # noqa: E501

        :param project_name: The project_name of this GetApplicationsResponseItems.  # noqa: E501
        :type: str
        """

        self._project_name = project_name

    @property
    def short_name(self):
        """Gets the short_name of this GetApplicationsResponseItems.  # noqa: E501

        项目简称  # noqa: E501

        :return: The short_name of this GetApplicationsResponseItems.  # noqa: E501
        :rtype: str
        """
        return self._short_name

    @short_name.setter
    def short_name(self, short_name):
        """Sets the short_name of this GetApplicationsResponseItems.

        项目简称  # noqa: E501

        :param short_name: The short_name of this GetApplicationsResponseItems.  # noqa: E501
        :type: str
        """

        self._short_name = short_name

    @property
    def fullname(self):
        """Gets the fullname of this GetApplicationsResponseItems.  # noqa: E501

        项目全称  # noqa: E501

        :return: The fullname of this GetApplicationsResponseItems.  # noqa: E501
        :rtype: str
        """
        return self._fullname

    @fullname.setter
    def fullname(self, fullname):
        """Sets the fullname of this GetApplicationsResponseItems.

        项目全称  # noqa: E501

        :param fullname: The fullname of this GetApplicationsResponseItems.  # noqa: E501
        :type: str
        """

        self._fullname = fullname

    @property
    def coin_logo_key(self):
        """Gets the coin_logo_key of this GetApplicationsResponseItems.  # noqa: E501

        币种图标KEY  # noqa: E501

        :return: The coin_logo_key of this GetApplicationsResponseItems.  # noqa: E501
        :rtype: str
        """
        return self._coin_logo_key

    @coin_logo_key.setter
    def coin_logo_key(self, coin_logo_key):
        """Sets the coin_logo_key of this GetApplicationsResponseItems.

        币种图标KEY  # noqa: E501

        :param coin_logo_key: The coin_logo_key of this GetApplicationsResponseItems.  # noqa: E501
        :type: str
        """

        self._coin_logo_key = coin_logo_key

    @property
    def coin_logo_url(self):
        """Gets the coin_logo_url of this GetApplicationsResponseItems.  # noqa: E501

        币种图标URL  # noqa: E501

        :return: The coin_logo_url of this GetApplicationsResponseItems.  # noqa: E501
        :rtype: str
        """
        return self._coin_logo_url

    @coin_logo_url.setter
    def coin_logo_url(self, coin_logo_url):
        """Sets the coin_logo_url of this GetApplicationsResponseItems.

        币种图标URL  # noqa: E501

        :param coin_logo_url: The coin_logo_url of this GetApplicationsResponseItems.  # noqa: E501
        :type: str
        """

        self._coin_logo_url = coin_logo_url

    @property
    def applied_at(self):
        """Gets the applied_at of this GetApplicationsResponseItems.  # noqa: E501

        申请时间  # noqa: E501

        :return: The applied_at of this GetApplicationsResponseItems.  # noqa: E501
        :rtype: datetime
        """
        return self._applied_at

    @applied_at.setter
    def applied_at(self, applied_at):
        """Sets the applied_at of this GetApplicationsResponseItems.

        申请时间  # noqa: E501

        :param applied_at: The applied_at of this GetApplicationsResponseItems.  # noqa: E501
        :type: datetime
        """

        self._applied_at = applied_at

    @property
    def status(self):
        """Gets the status of this GetApplicationsResponseItems.  # noqa: E501

        状态[未完成undone、审核中under_review、审核通过passed、驳回turn_down]  # noqa: E501

        :return: The status of this GetApplicationsResponseItems.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this GetApplicationsResponseItems.

        状态[未完成undone、审核中under_review、审核通过passed、驳回turn_down]  # noqa: E501

        :param status: The status of this GetApplicationsResponseItems.  # noqa: E501
        :type: str
        """
        allowed_values = ["undone", "under_review", "passed", "turn_down"]  # noqa: E501
        if status not in allowed_values:
            raise ValueError(
                "Invalid value for `status` ({0}), must be one of {1}"  # noqa: E501
                .format(status, allowed_values)
            )

        self._status = status

    @property
    def remarks(self):
        """Gets the remarks of this GetApplicationsResponseItems.  # noqa: E501


        :return: The remarks of this GetApplicationsResponseItems.  # noqa: E501
        :rtype: str
        """
        return self._remarks

    @remarks.setter
    def remarks(self, remarks):
        """Sets the remarks of this GetApplicationsResponseItems.


        :param remarks: The remarks of this GetApplicationsResponseItems.  # noqa: E501
        :type: str
        """

        self._remarks = remarks

    @property
    def audited_at(self):
        """Gets the audited_at of this GetApplicationsResponseItems.  # noqa: E501

        审核时间  # noqa: E501

        :return: The audited_at of this GetApplicationsResponseItems.  # noqa: E501
        :rtype: datetime
        """
        return self._audited_at

    @audited_at.setter
    def audited_at(self, audited_at):
        """Sets the audited_at of this GetApplicationsResponseItems.

        审核时间  # noqa: E501

        :param audited_at: The audited_at of this GetApplicationsResponseItems.  # noqa: E501
        :type: datetime
        """

        self._audited_at = audited_at

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
        if issubclass(GetApplicationsResponseItems, dict):
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
        if not isinstance(other, GetApplicationsResponseItems):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
