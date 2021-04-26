#encoding:utf-8
import uuid
import imghdr
from flask import Flask
from flask import render_template
from flask import jsonify
from flask import request
from qiniu import Auth, put_data, etag, put_file

app = Flask(__name__)

access_key = 'W00QA_0SZjaaUQspa2mlnaH2UGTOZ1PB85cpRP2K'
secret_key = 'W3oxzoh5VcjYuOQKtnmnEN_OdFXogrxbt0Eq_RmP'


def upload_file_qiniu(data):
    q = Auth(access_key, secret_key)
    bucket_name = 'cz-tuchuang'
    suffix_name = imghdr.what(None, data)
    bad_pic_name = uuid.uuid5(uuid.NAMESPACE_DNS, "chaizz")
    pic_name = ''.join(str(bad_pic_name).split('-')) + '.' + suffix_name
    print("pic_name", pic_name)
    token = q.upload_token(bucket_name, pic_name, 3600)
    ret1, ret2 = put_data(token, pic_name, data=data)
    print('ret1:', ret1)
    print('ret2:', ret2)
    # 判断是否上传成功
    if ret2.status_code != 200:
        raise Exception('文件上传失败')

    return ret1.get('key')


@app.route('/', methods=['post', 'GET'])
def upload_carimg():
    if request.method == 'GET':
        return render_template('up_load_pic.html')
    if request.method == 'POST':
        file_storage = request.files.get('file')
        data = file_storage.read()
        try:
            pic_name = upload_file_qiniu(data)
            External_link = "https://tc.chaizz.com/" + pic_name
            return jsonify(ImgUrl=External_link)
        except Exception as e:
            return jsonify(errmsg='上传失败')


if __name__ == '__main__':
    app.run(debug=True)
