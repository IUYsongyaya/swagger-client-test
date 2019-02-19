# @Author  : xy.zhang
# @Email   : zhangxuyi@wanshare.com
# @Time    : 18-11-14

START_PAGE = 1
ORDER_DESCENDING = "descending"
ORDER_ASCENDING = "ascending"


class Pager:
    def __init__(self, pager, **kwargs):
        try:
            self._page = kwargs['page']
        except KeyError:
            self._page = 1
            self._order = ORDER_ASCENDING
        else:
            del kwargs["page"]
            self._order = kwargs.get("order", ORDER_ASCENDING)

        self._pager = pager
        self._kwargs = kwargs
        rsp = pager(page=self._page, **self._kwargs)
        assert hasattr(rsp, "meta")
        self.meta = rsp.meta
        self._total_page = self.meta.total_page
        self._total_count = self.meta.total_count
        self._items_per_page = self.meta.items_per_page
        try:
            self._end_page = kwargs["end_page"]
        except KeyError:
            if self._order == ORDER_ASCENDING:
                self._end_page = self._total_page
            else:
                self._end_page = START_PAGE

        if self._order == ORDER_ASCENDING and self._page > self._end_page:
            # raise Exception(
            #     "start page is larger than end page in ascending order is not allow  start_page:%u end_page:%u" % (
            #     self._page, self._end_page))
            print("start page is larger than end page in ascending order is not allow  start_page:%u end_page:%u" % (
                self._page, self._end_page))
                
        elif self._order == ORDER_DESCENDING and self._page < self._end_page:
            raise Exception(
                "start page is small than end page in descending order is not allow")

    def __iter__(self):
        return self

    def __next__(self):
        if self._order == ORDER_ASCENDING and self._page > self._end_page:
            raise StopIteration
        elif self._order == ORDER_DESCENDING and self._page < self._end_page:
            raise StopIteration

        page_content = self._pager(page=self._page, **self._kwargs)
        if self._order == ORDER_ASCENDING:
            self._page += 1
        else:
            self._page -= 1
        return page_content


def make_pager(api, **kwargs):
    def pager():
        ret = list()
        pages = Pager(api, **kwargs)
        for page in pages:
            array_attr_name = "items"
            if not hasattr(page, 'items'):
                array_attr_name = "data"
            if getattr(page, array_attr_name):
                ret.extend(getattr(page, array_attr_name))
        return ret
    return pager


def make_query(api, filter=None, **kwargs):
    
    def query():
        if not filter:
            return make_pager(api, **kwargs)()
        else:
            ret = list()
            pages = Pager(api, **kwargs)
            for page in pages:
                array_attr_name = "items"
                if not hasattr(page, 'items'):
                    array_attr_name = "data"
                if getattr(page, array_attr_name):
                    for item in getattr(page, array_attr_name):
                        if isinstance(item, dict):
                            for key, val in filter.items():
                                if item[key] != val:
                                    break
                            else:
                                ret.append(item)
                        else:
                            for key, val in filter.items():
                                try:
                                    if getattr(item, key) != val:
                                        break
                                except AttributeError as e:
                                    break
                            else:
                                ret.append(item)
            return ret
    return query


def list_items(api, **kwargs):
    return make_pager(api, **kwargs)()


def query_items(api, filter=None, **kwargs):
    return make_query(api, filter=filter, **kwargs)()


def query_unique_item(api, filter=None, **kwargs):
    ret = make_query(api, filter=filter, **kwargs)()
    if ret:
        if len(ret) == 1:
            return ret[0]
        else:
            raise Exception("Not unique item, unique query failed!")
