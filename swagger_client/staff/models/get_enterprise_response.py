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


class GetEnterpriseResponse(object):
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
        'company_name': 'str',
        'nationality_code': 'str',
        'area': 'str',
        'address': 'str',
        'logo': 'str',
        'social_code': 'str',
        'tax_number': 'str',
        'organization_code': 'str',
        'business_license': 'str',
        'name': 'str',
        'phone_number': 'str'
    }

    attribute_map = {
        'company_name': 'companyName',
        'nationality_code': 'nationalityCode',
        'area': 'area',
        'address': 'address',
        'logo': 'logo',
        'social_code': 'socialCode',
        'tax_number': 'taxNumber',
        'organization_code': 'organizationCode',
        'business_license': 'businessLicense',
        'name': 'name',
        'phone_number': 'phoneNumber'
    }

    def __init__(self, company_name=None, nationality_code=None, area=None, address=None, logo=None, social_code=None, tax_number=None, organization_code=None, business_license=None, name=None, phone_number=None):  # noqa: E501
        """GetEnterpriseResponse - a model defined in Swagger"""  # noqa: E501

        self._company_name = None
        self._nationality_code = None
        self._area = None
        self._address = None
        self._logo = None
        self._social_code = None
        self._tax_number = None
        self._organization_code = None
        self._business_license = None
        self._name = None
        self._phone_number = None
        self.discriminator = None

        if company_name is not None:
            self.company_name = company_name
        if nationality_code is not None:
            self.nationality_code = nationality_code
        if area is not None:
            self.area = area
        if address is not None:
            self.address = address
        if logo is not None:
            self.logo = logo
        if social_code is not None:
            self.social_code = social_code
        if tax_number is not None:
            self.tax_number = tax_number
        if organization_code is not None:
            self.organization_code = organization_code
        if business_license is not None:
            self.business_license = business_license
        if name is not None:
            self.name = name
        if phone_number is not None:
            self.phone_number = phone_number

    @property
    def company_name(self):
        """Gets the company_name of this GetEnterpriseResponse.  # noqa: E501

        企业名字  # noqa: E501

        :return: The company_name of this GetEnterpriseResponse.  # noqa: E501
        :rtype: str
        """
        return self._company_name

    @company_name.setter
    def company_name(self, company_name):
        """Sets the company_name of this GetEnterpriseResponse.

        企业名字  # noqa: E501

        :param company_name: The company_name of this GetEnterpriseResponse.  # noqa: E501
        :type: str
        """

        self._company_name = company_name

    @property
    def nationality_code(self):
        """Gets the nationality_code of this GetEnterpriseResponse.  # noqa: E501

        公司国籍（证件所在区域）  # noqa: E501

        :return: The nationality_code of this GetEnterpriseResponse.  # noqa: E501
        :rtype: str
        """
        return self._nationality_code

    @nationality_code.setter
    def nationality_code(self, nationality_code):
        """Sets the nationality_code of this GetEnterpriseResponse.

        公司国籍（证件所在区域）  # noqa: E501

        :param nationality_code: The nationality_code of this GetEnterpriseResponse.  # noqa: E501
        :type: str
        """

        self._nationality_code = nationality_code

    @property
    def area(self):
        """Gets the area of this GetEnterpriseResponse.  # noqa: E501

        公司地区  # noqa: E501

        :return: The area of this GetEnterpriseResponse.  # noqa: E501
        :rtype: str
        """
        return self._area

    @area.setter
    def area(self, area):
        """Sets the area of this GetEnterpriseResponse.

        公司地区  # noqa: E501

        :param area: The area of this GetEnterpriseResponse.  # noqa: E501
        :type: str
        """

        self._area = area

    @property
    def address(self):
        """Gets the address of this GetEnterpriseResponse.  # noqa: E501

        公司地址  # noqa: E501

        :return: The address of this GetEnterpriseResponse.  # noqa: E501
        :rtype: str
        """
        return self._address

    @address.setter
    def address(self, address):
        """Sets the address of this GetEnterpriseResponse.

        公司地址  # noqa: E501

        :param address: The address of this GetEnterpriseResponse.  # noqa: E501
        :type: str
        """

        self._address = address

    @property
    def logo(self):
        """Gets the logo of this GetEnterpriseResponse.  # noqa: E501

        logo  # noqa: E501

        :return: The logo of this GetEnterpriseResponse.  # noqa: E501
        :rtype: str
        """
        return self._logo

    @logo.setter
    def logo(self, logo):
        """Sets the logo of this GetEnterpriseResponse.

        logo  # noqa: E501

        :param logo: The logo of this GetEnterpriseResponse.  # noqa: E501
        :type: str
        """

        self._logo = logo

    @property
    def social_code(self):
        """Gets the social_code of this GetEnterpriseResponse.  # noqa: E501

        社会统一编号  # noqa: E501

        :return: The social_code of this GetEnterpriseResponse.  # noqa: E501
        :rtype: str
        """
        return self._social_code

    @social_code.setter
    def social_code(self, social_code):
        """Sets the social_code of this GetEnterpriseResponse.

        社会统一编号  # noqa: E501

        :param social_code: The social_code of this GetEnterpriseResponse.  # noqa: E501
        :type: str
        """

        self._social_code = social_code

    @property
    def tax_number(self):
        """Gets the tax_number of this GetEnterpriseResponse.  # noqa: E501

        税务登记证编号  # noqa: E501

        :return: The tax_number of this GetEnterpriseResponse.  # noqa: E501
        :rtype: str
        """
        return self._tax_number

    @tax_number.setter
    def tax_number(self, tax_number):
        """Sets the tax_number of this GetEnterpriseResponse.

        税务登记证编号  # noqa: E501

        :param tax_number: The tax_number of this GetEnterpriseResponse.  # noqa: E501
        :type: str
        """

        self._tax_number = tax_number

    @property
    def organization_code(self):
        """Gets the organization_code of this GetEnterpriseResponse.  # noqa: E501

        组织机构编号  # noqa: E501

        :return: The organization_code of this GetEnterpriseResponse.  # noqa: E501
        :rtype: str
        """
        return self._organization_code

    @organization_code.setter
    def organization_code(self, organization_code):
        """Sets the organization_code of this GetEnterpriseResponse.

        组织机构编号  # noqa: E501

        :param organization_code: The organization_code of this GetEnterpriseResponse.  # noqa: E501
        :type: str
        """

        self._organization_code = organization_code

    @property
    def business_license(self):
        """Gets the business_license of this GetEnterpriseResponse.  # noqa: E501

        营业执照副本  # noqa: E501

        :return: The business_license of this GetEnterpriseResponse.  # noqa: E501
        :rtype: str
        """
        return self._business_license

    @business_license.setter
    def business_license(self, business_license):
        """Sets the business_license of this GetEnterpriseResponse.

        营业执照副本  # noqa: E501

        :param business_license: The business_license of this GetEnterpriseResponse.  # noqa: E501
        :type: str
        """

        self._business_license = business_license

    @property
    def name(self):
        """Gets the name of this GetEnterpriseResponse.  # noqa: E501

        法人姓名  # noqa: E501

        :return: The name of this GetEnterpriseResponse.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this GetEnterpriseResponse.

        法人姓名  # noqa: E501

        :param name: The name of this GetEnterpriseResponse.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def phone_number(self):
        """Gets the phone_number of this GetEnterpriseResponse.  # noqa: E501

        电话号  # noqa: E501

        :return: The phone_number of this GetEnterpriseResponse.  # noqa: E501
        :rtype: str
        """
        return self._phone_number

    @phone_number.setter
    def phone_number(self, phone_number):
        """Sets the phone_number of this GetEnterpriseResponse.

        电话号  # noqa: E501

        :param phone_number: The phone_number of this GetEnterpriseResponse.  # noqa: E501
        :type: str
        """

        self._phone_number = phone_number

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
        if issubclass(GetEnterpriseResponse, dict):
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
        if not isinstance(other, GetEnterpriseResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other