#encoding:utf-8
import uuid
import imghdr
from flask import Flask
from flask import jsonify, make_response, render_template
from flask import request
from qiniu import Auth, put_data

app = Flask(__name__)

access_key = 'W00QA_0SZjaaUQspa2mlnaH2UGTOZ1PB85cpRP2K'
secret_key = 'W3oxzoh5VcjYuOQKtnmnEN_OdFXogrxbt0Eq_RmP'


def upload_file_qiniu(data):
    q = Auth(access_key, secret_key)
    bucket_name = 'cz-tuchuang'
    suffix_name = imghdr.what(None, data)
    bad_pic_name = uuid.uuid1()
    pic_name = ''.join(str(bad_pic_name).split('-')) + '.' + suffix_name
    token = q.upload_token(bucket_name, pic_name, 3600)
    ret1, ret2 = put_data(token, pic_name, data=data)
    # 判断是否上传成功
    if ret2.status_code != 200:
        raise Exception('文件上传失败')
    return ret1.get('key')


@app.route('/', methods=['post', 'GET'])
def upload_carimg():
    if request.method == 'GET':
        return jsonify(code=404)
    if request.method == 'POST':
        file_storage = request.files.get('file')
        data = file_storage.read()
        try:
            file_name = upload_file_qiniu(data)
            External_link = "https://tc.chaizz.com/" + file_name
            res = make_response(jsonify(ImgUrl=External_link))
            res.headers['Access-Control-Allow-Origin'] = '*'
            res.headers['Access-Control-Allow-Method'] = '*'
            res.headers['Access-Control-Allow-Headers'] = '*'
            return res
        except Exception as e:
            return jsonify(errmsg='上传失败')


if __name__ == '__main__':
    app.run()
