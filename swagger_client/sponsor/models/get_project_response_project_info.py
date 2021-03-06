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


class GetProjectResponseProjectInfo(object):
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
        'project_name': 'str',
        'project_logo': 'str',
        'white_paper': 'str',
        'official_website': 'str',
        'email': 'str',
        'cellphone': 'str',
        'description': 'str'
    }

    attribute_map = {
        'project_name': 'projectName',
        'project_logo': 'projectLogo',
        'white_paper': 'whitePaper',
        'official_website': 'officialWebsite',
        'email': 'email',
        'cellphone': 'cellphone',
        'description': 'description'
    }

    def __init__(self, project_name=None, project_logo=None, white_paper=None, official_website=None, email=None, cellphone=None, description=None):  # noqa: E501
        """GetProjectResponseProjectInfo - a model defined in Swagger"""  # noqa: E501

        self._project_name = None
        self._project_logo = None
        self._white_paper = None
        self._official_website = None
        self._email = None
        self._cellphone = None
        self._description = None
        self.discriminator = None

        if project_name is not None:
            self.project_name = project_name
        if project_logo is not None:
            self.project_logo = project_logo
        if white_paper is not None:
            self.white_paper = white_paper
        if official_website is not None:
            self.official_website = official_website
        if email is not None:
            self.email = email
        if cellphone is not None:
            self.cellphone = cellphone
        if description is not None:
            self.description = description

    @property
    def project_name(self):
        """Gets the project_name of this GetProjectResponseProjectInfo.  # noqa: E501

        项目名  # noqa: E501

        :return: The project_name of this GetProjectResponseProjectInfo.  # noqa: E501
        :rtype: str
        """
        return self._project_name

    @project_name.setter
    def project_name(self, project_name):
        """Sets the project_name of this GetProjectResponseProjectInfo.

        项目名  # noqa: E501

        :param project_name: The project_name of this GetProjectResponseProjectInfo.  # noqa: E501
        :type: str
        """

        self._project_name = project_name

    @property
    def project_logo(self):
        """Gets the project_logo of this GetProjectResponseProjectInfo.  # noqa: E501

        项目logo  # noqa: E501

        :return: The project_logo of this GetProjectResponseProjectInfo.  # noqa: E501
        :rtype: str
        """
        return self._project_logo

    @project_logo.setter
    def project_logo(self, project_logo):
        """Sets the project_logo of this GetProjectResponseProjectInfo.

        项目logo  # noqa: E501

        :param project_logo: The project_logo of this GetProjectResponseProjectInfo.  # noqa: E501
        :type: str
        """

        self._project_logo = project_logo

    @property
    def white_paper(self):
        """Gets the white_paper of this GetProjectResponseProjectInfo.  # noqa: E501

        白皮书PDF  # noqa: E501

        :return: The white_paper of this GetProjectResponseProjectInfo.  # noqa: E501
        :rtype: str
        """
        return self._white_paper

    @white_paper.setter
    def white_paper(self, white_paper):
        """Sets the white_paper of this GetProjectResponseProjectInfo.

        白皮书PDF  # noqa: E501

        :param white_paper: The white_paper of this GetProjectResponseProjectInfo.  # noqa: E501
        :type: str
        """

        self._white_paper = white_paper

    @property
    def official_website(self):
        """Gets the official_website of this GetProjectResponseProjectInfo.  # noqa: E501

        官方网站  # noqa: E501

        :return: The official_website of this GetProjectResponseProjectInfo.  # noqa: E501
        :rtype: str
        """
        return self._official_website

    @official_website.setter
    def official_website(self, official_website):
        """Sets the official_website of this GetProjectResponseProjectInfo.

        官方网站  # noqa: E501

        :param official_website: The official_website of this GetProjectResponseProjectInfo.  # noqa: E501
        :type: str
        """

        self._official_website = official_website

    @property
    def email(self):
        """Gets the email of this GetProjectResponseProjectInfo.  # noqa: E501

        电子邮箱  # noqa: E501

        :return: The email of this GetProjectResponseProjectInfo.  # noqa: E501
        :rtype: str
        """
        return self._email

    @email.setter
    def email(self, email):
        """Sets the email of this GetProjectResponseProjectInfo.

        电子邮箱  # noqa: E501

        :param email: The email of this GetProjectResponseProjectInfo.  # noqa: E501
        :type: str
        """

        self._email = email

    @property
    def cellphone(self):
        """Gets the cellphone of this GetProjectResponseProjectInfo.  # noqa: E501

        手机号  # noqa: E501

        :return: The cellphone of this GetProjectResponseProjectInfo.  # noqa: E501
        :rtype: str
        """
        return self._cellphone

    @cellphone.setter
    def cellphone(self, cellphone):
        """Sets the cellphone of this GetProjectResponseProjectInfo.

        手机号  # noqa: E501

        :param cellphone: The cellphone of this GetProjectResponseProjectInfo.  # noqa: E501
        :type: str
        """

        self._cellphone = cellphone

    @property
    def description(self):
        """Gets the description of this GetProjectResponseProjectInfo.  # noqa: E501

        项目简介  # noqa: E501

        :return: The description of this GetProjectResponseProjectInfo.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this GetProjectResponseProjectInfo.

        项目简介  # noqa: E501

        :param description: The description of this GetProjectResponseProjectInfo.  # noqa: E501
        :type: str
        """

        self._description = description

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
        if issubclass(GetProjectResponseProjectInfo, dict):
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
        if not isinstance(other, GetProjectResponseProjectInfo):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
