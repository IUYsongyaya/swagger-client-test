# @Author  : xy.zhang
# @Email   : zhangxuyi@wanshare.com
# @Time    : 19-1-8
# from PIL import Image


class UtilUpload:
    def __init__(self):
        pass

    def upload(self, path=None, red=0, green=0, blue=0, width=0, height=0):
        assert path, "Photo path must not be null"
        rsp = self.api_file_upload.upload(file=path)
        # else:
            # path_saved = "test_upload_photo.jpg"
            # Image.new('RGB', (width, height), color=(red, green, blue)).save(path_saved)
            # rsp = self.api_file_upload.upload(file=path_saved)
        return rsp.key, rsp.url

    def get_file(self, key):
        rsp = self.api_file_upload.file_key_get(key=key)
        return rsp.url
    
    def get_zoom_file(self, key, zoom):
        rsp = self.api_file_upload.file_key_zoom_zoom_get(key=key, zoom=zoom)
        return rsp.url
