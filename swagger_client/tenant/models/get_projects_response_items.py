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


class GetProjectsResponseItems(object):
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
        'project_id': 'str',
        'short_name': 'str',
        'full_name': 'str',
        'coin_logo_url': 'str',
        'issue_price': 'str',
        'issued_volume': 'str',
        'holders_number': 'str',
        'circulation_volume': 'str',
        'official_website': 'str',
        'block_browser': 'str',
        'access_method': 'str'
    }

    attribute_map = {
        'project_id': 'projectId',
        'short_name': 'shortName',
        'full_name': 'fullName',
        'coin_logo_url': 'coinLogoUrl',
        'issue_price': 'issuePrice',
        'issued_volume': 'issuedVolume',
        'holders_number': 'holdersNumber',
        'circulation_volume': 'circulationVolume',
        'official_website': 'officialWebsite',
        'block_browser': 'blockBrowser',
        'access_method': 'accessMethod'
    }

    def __init__(self, project_id=None, short_name=None, full_name=None, coin_logo_url=None, issue_price=None, issued_volume=None, holders_number=None, circulation_volume=None, official_website=None, block_browser=None, access_method=None):  # noqa: E501
        """GetProjectsResponseItems - a model defined in Swagger"""  # noqa: E501

        self._project_id = None
        self._short_name = None
        self._full_name = None
        self._coin_logo_url = None
        self._issue_price = None
        self._issued_volume = None
        self._holders_number = None
        self._circulation_volume = None
        self._official_website = None
        self._block_browser = None
        self._access_method = None
        self.discriminator = None

        if project_id is not None:
            self.project_id = project_id
        if short_name is not None:
            self.short_name = short_name
        if full_name is not None:
            self.full_name = full_name
        if coin_logo_url is not None:
            self.coin_logo_url = coin_logo_url
        if issue_price is not None:
            self.issue_price = issue_price
        if issued_volume is not None:
            self.issued_volume = issued_volume
        if holders_number is not None:
            self.holders_number = holders_number
        if circulation_volume is not None:
            self.circulation_volume = circulation_volume
        if official_website is not None:
            self.official_website = official_website
        if block_browser is not None:
            self.block_browser = block_browser
        if access_method is not None:
            self.access_method = access_method

    @property
    def project_id(self):
        """Gets the project_id of this GetProjectsResponseItems.  # noqa: E501

        项目ID  # noqa: E501

        :return: The project_id of this GetProjectsResponseItems.  # noqa: E501
        :rtype: str
        """
        return self._project_id

    @project_id.setter
    def project_id(self, project_id):
        """Sets the project_id of this GetProjectsResponseItems.

        项目ID  # noqa: E501

        :param project_id: The project_id of this GetProjectsResponseItems.  # noqa: E501
        :type: str
        """

        self._project_id = project_id

    @property
    def short_name(self):
        """Gets the short_name of this GetProjectsResponseItems.  # noqa: E501

        币简称  # noqa: E501

        :return: The short_name of this GetProjectsResponseItems.  # noqa: E501
        :rtype: str
        """
        return self._short_name

    @short_name.setter
    def short_name(self, short_name):
        """Sets the short_name of this GetProjectsResponseItems.

        币简称  # noqa: E501

        :param short_name: The short_name of this GetProjectsResponseItems.  # noqa: E501
        :type: str
        """

        self._short_name = short_name

    @property
    def full_name(self):
        """Gets the full_name of this GetProjectsResponseItems.  # noqa: E501

        币全称  # noqa: E501

        :return: The full_name of this GetProjectsResponseItems.  # noqa: E501
        :rtype: str
        """
        return self._full_name

    @full_name.setter
    def full_name(self, full_name):
        """Sets the full_name of this GetProjectsResponseItems.

        币全称  # noqa: E501

        :param full_name: The full_name of this GetProjectsResponseItems.  # noqa: E501
        :type: str
        """

        self._full_name = full_name

    @property
    def coin_logo_url(self):
        """Gets the coin_logo_url of this GetProjectsResponseItems.  # noqa: E501

        币种LOGO  # noqa: E501

        :return: The coin_logo_url of this GetProjectsResponseItems.  # noqa: E501
        :rtype: str
        """
        return self._coin_logo_url

    @coin_logo_url.setter
    def coin_logo_url(self, coin_logo_url):
        """Sets the coin_logo_url of this GetProjectsResponseItems.

        币种LOGO  # noqa: E501

        :param coin_logo_url: The coin_logo_url of this GetProjectsResponseItems.  # noqa: E501
        :type: str
        """

        self._coin_logo_url = coin_logo_url

    @property
    def issue_price(self):
        """Gets the issue_price of this GetProjectsResponseItems.  # noqa: E501

        发行价格  # noqa: E501

        :return: The issue_price of this GetProjectsResponseItems.  # noqa: E501
        :rtype: str
        """
        return self._issue_price

    @issue_price.setter
    def issue_price(self, issue_price):
        """Sets the issue_price of this GetProjectsResponseItems.

        发行价格  # noqa: E501

        :param issue_price: The issue_price of this GetProjectsResponseItems.  # noqa: E501
        :type: str
        """

        self._issue_price = issue_price

    @property
    def issued_volume(self):
        """Gets the issued_volume of this GetProjectsResponseItems.  # noqa: E501

        发行量  # noqa: E501

        :return: The issued_volume of this GetProjectsResponseItems.  # noqa: E501
        :rtype: str
        """
        return self._issued_volume

    @issued_volume.setter
    def issued_volume(self, issued_volume):
        """Sets the issued_volume of this GetProjectsResponseItems.

        发行量  # noqa: E501

        :param issued_volume: The issued_volume of this GetProjectsResponseItems.  # noqa: E501
        :type: str
        """

        self._issued_volume = issued_volume

    @property
    def holders_number(self):
        """Gets the holders_number of this GetProjectsResponseItems.  # noqa: E501

        持有用户数  # noqa: E501

        :return: The holders_number of this GetProjectsResponseItems.  # noqa: E501
        :rtype: str
        """
        return self._holders_number

    @holders_number.setter
    def holders_number(self, holders_number):
        """Sets the holders_number of this GetProjectsResponseItems.

        持有用户数  # noqa: E501

        :param holders_number: The holders_number of this GetProjectsResponseItems.  # noqa: E501
        :type: str
        """

        self._holders_number = holders_number

    @property
    def circulation_volume(self):
        """Gets the circulation_volume of this GetProjectsResponseItems.  # noqa: E501

        流通量  # noqa: E501

        :return: The circulation_volume of this GetProjectsResponseItems.  # noqa: E501
        :rtype: str
        """
        return self._circulation_volume

    @circulation_volume.setter
    def circulation_volume(self, circulation_volume):
        """Sets the circulation_volume of this GetProjectsResponseItems.

        流通量  # noqa: E501

        :param circulation_volume: The circulation_volume of this GetProjectsResponseItems.  # noqa: E501
        :type: str
        """

        self._circulation_volume = circulation_volume

    @property
    def official_website(self):
        """Gets the official_website of this GetProjectsResponseItems.  # noqa: E501

        官方网站  # noqa: E501

        :return: The official_website of this GetProjectsResponseItems.  # noqa: E501
        :rtype: str
        """
        return self._official_website

    @official_website.setter
    def official_website(self, official_website):
        """Sets the official_website of this GetProjectsResponseItems.

        官方网站  # noqa: E501

        :param official_website: The official_website of this GetProjectsResponseItems.  # noqa: E501
        :type: str
        """

        self._official_website = official_website

    @property
    def block_browser(self):
        """Gets the block_browser of this GetProjectsResponseItems.  # noqa: E501

        区块浏览器  # noqa: E501

        :return: The block_browser of this GetProjectsResponseItems.  # noqa: E501
        :rtype: str
        """
        return self._block_browser

    @block_browser.setter
    def block_browser(self, block_browser):
        """Sets the block_browser of this GetProjectsResponseItems.

        区块浏览器  # noqa: E501

        :param block_browser: The block_browser of this GetProjectsResponseItems.  # noqa: E501
        :type: str
        """

        self._block_browser = block_browser

    @property
    def access_method(self):
        """Gets the access_method of this GetProjectsResponseItems.  # noqa: E501

        接入方式（refuse：拒绝接入、verification：需要验证、accept：无需验证）  # noqa: E501

        :return: The access_method of this GetProjectsResponseItems.  # noqa: E501
        :rtype: str
        """
        return self._access_method

    @access_method.setter
    def access_method(self, access_method):
        """Sets the access_method of this GetProjectsResponseItems.

        接入方式（refuse：拒绝接入、verification：需要验证、accept：无需验证）  # noqa: E501

        :param access_method: The access_method of this GetProjectsResponseItems.  # noqa: E501
        :type: str
        """
        allowed_values = ["refuse", "verification", "accept"]  # noqa: E501
        if access_method not in allowed_values:
            raise ValueError(
                "Invalid value for `access_method` ({0}), must be one of {1}"  # noqa: E501
                .format(access_method, allowed_values)
            )

        self._access_method = access_method

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
        if issubclass(GetProjectsResponseItems, dict):
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
        if not isinstance(other, GetProjectsResponseItems):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
