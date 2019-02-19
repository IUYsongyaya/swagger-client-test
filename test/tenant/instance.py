# @Author  : xy.zhang
# @Email   : zhangxuyi@wanshare.com
# @Time    : 18-12-9

import logging
from test.tenant.id_settings import *
from common.photo import *

logger = logging.getLogger(__name__)


class DictObj:
    
    def __init__(self, attr_dict):
        assert isinstance(attr_dict, dict), "Must use dict for templating"
        for key, val in attr_dict.items():
            setattr(self, key, val)
    
    def to_dict(self):
        return self.__dict__


def get_templated_attrs(cls, idx):
    name = str.lower(cls.__name__)
    dict_copy = cls.attrs_template.copy()
    for key, template in dict_copy.items():
        dict_copy[key] = template(name, idx) if callable(template) else template
    return dict_copy


class InstanceMeta(type):

    def __call__(cls, index, attrs=None):
        # print("args: ", args)
        # print("kwargs: ", kwargs)
        idx = index
        assert "attrs_template" in vars(cls), "Missing attrs template"
        # print("instances count", len(cls._instances))
        if str(idx) not in cls._instances:
            inst = cls.__new__(cls, cls.__name__, cls.__bases__)
            logger.info("%s create new instance %s" % (type(inst).__name__.upper(), str(idx)))
            cls._instances[idx] = inst
            inst.__init__(index, attrs=attrs)
        if hasattr(cls._instances[idx], "inited") and not cls._instances[idx].inited:
            cls._instances[idx].init_instance()

        return cls._instances[idx]


INIT_INDEX = -1


class Instance(metaclass=InstanceMeta):
    
    def __init__(self, index, attrs=None):
        super().__init__()
        self._index = index
        if isinstance(self._index, int):
            for base_cls in reversed(self.__class__.__mro__):
                if "attrs_template" in vars(base_cls):
                    for key, val in get_templated_attrs(base_cls, index).items():
                        setattr(self, key, val)
        else:
            assert isinstance(self._index, str), "Index must be a int or str"
            assert attrs, "If index is a str, attrs must not be None"
            
    @property
    def index(self):
        return self._index


class User(Instance):
    
    def __init__(self, index, attrs=None):
        super().__init__(index, attrs=attrs)

    def login(self):
        print("login with account:%s email:%s password:%s" % (self.account, self.email, self.password))
        pass
    
    def __repr__(self):
        cls_name = f"< {type(self).__name__}"
        attrs_info = ""
        for key, val in self.__dict__.items():
            attrs_info += f" {key}: {val} "
        else:
            attrs_info += " >"
        return cls_name+attrs_info


class Venture(User):
    
    _instances = dict()
    
    attrs_template = dict(
        email=lambda name, index: "%s_%s_%u@gmail.com" % (CONFIG.TESTER.upper(), name, index),
        password=lambda name, index: "%s_%s_pwd" % (CONFIG.TESTER.upper(), name),
        name=lambda name, index: "%s%s%u" % (CONFIG.TESTER.upper(), name, index),
        logo=PHOTO_URL,
        account=lambda name, index: "_%s%s%u" % (CONFIG.TESTER.upper(), name, index),
        phone=lambda name, index: "1%s%s%05d" % (platfrom_id(name), name_hash(CONFIG.TESTER.upper()), index),
        identity=lambda name, index: "23233219%s%s%05d" % (platfrom_id(name), name_hash(CONFIG.TESTER.upper()), index),
        nationality_code=lambda name, index: "CN")
    
    def __init__(self, index, attrs=None):
        super().__init__(index, attrs=attrs)
        for key, val in  attrs.items():
            setattr(self, key, val)
            

def main():

    venture_xy = dict(
        email="user_xy@gmail.com",
        password="xy_bangbang",
        name="xy",
        logo=PHOTO_URL,
        account="_xy",
        phone="18588232661",
        identity="441202199911190544",
    )

    v2 = Venture("xy", attrs=venture_xy)
    print(v2)


if __name__ == '__main__':
    main()
