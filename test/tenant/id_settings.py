# @Author  : xy.zhang
# @Email   : zhangxuyi@wanshare.com
# @Time    : 18-12-14
import os
import yaml
from functools import reduce


class Config:
    default_index = ["main_index", "tenant_index", "venture_index", "sponsor_index", "project_index"]
    
    def __init__(self, auto_inc=None, tester=None):
        with open(os.path.dirname(os.path.abspath(__file__)) + "/test_config.yaml", "r") as f:
            yaml_dict = yaml.load(f)
            
        if auto_inc:
            with open(os.path.dirname(os.path.abspath(__file__))+"/test_config.yaml", "w") as f:
                yaml_dict["shared_index"] += 1
                for index in self.default_index:
                    if index in yaml_dict.keys():
                        yaml_dict[index] += 1
                        # setattr(self, index.upper(), yaml_dict[index])
                    # else:
                    #     setattr(self, index.upper(), yaml_dict["shared_index"])
                yaml.dump(yaml_dict, f, default_flow_style=False)
            
        for key, val in yaml_dict.items():
            if key == "tester" and tester:
                setattr(self, key.upper(), tester)
            else:
                setattr(self, key.upper(), val)
        
        for index in self.default_index:
            if index not in yaml_dict.keys():
                setattr(self, index.upper(), yaml_dict["shared_index"])
            
    def __repr__(self):
        body = reduce(lambda x, y: x + y,
                      ["%s:%s  " % (key, val) for key, val in self.__dict__.items() if not callable(val)])
        return "<  CONFIG: " + body + ">"
    

CONFIG = Config()

print(CONFIG)


def name_hash(name):
    max_val = 9999
    hash_sum = 0
    for c in name:
        hash_sum += ord(c)
    assert hash_sum <= max_val, f"Name hash fail for hash({name})={hash_sum} is larger than {max_val}"
    return "%04d" % hash_sum


def num_2_ascii(num):
    num_0 = 48
    char_A = 65
    max_val = 36 * 36 * 36 - 1
    position = list()
    assert num <= max_val, f"num:{num} must less than {max_val}"
    while max_val:
        position.append(num % 36)
        num = num//36
        max_val = max_val//36
    return tuple("%c" % (val + num_0) if val < 10 else "%c" % (val - 10 + char_A) for val in reversed(position))


def platfrom_id(platform):
    return str(dict(
        main=4,
        staff=5,
        tenant=6,
        venture=7,
        sponsor=8,
        otc=9
    )[platform])


if not (isinstance(CONFIG.TESTER, str) and len(CONFIG.TESTER) <= 4):
    raise Exception(f"CONFIG.TESTER:{CONFIG.TESTER} must be a non null str and len <= 4")


if __name__ == '__main__':
    # print(Config(auto_inc=True))
    print(Config(tester="sim"))
