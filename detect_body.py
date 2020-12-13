import base64
import json

import cv2
from tencentcloud.bda.v20200324 import bda_client, models
from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile


# 检测一张照片中的人并框出
try:
    cred = credential.Credential("", "")
    httpProfile = HttpProfile()
    httpProfile.endpoint = "bda.tencentcloudapi.com"

    clientProfile = ClientProfile()
    clientProfile.httpProfile = httpProfile
    client = bda_client.BdaClient(cred, "ap-shanghai", clientProfile)

    req = models.DetectBodyRequest()

    image_path = 'D:/detect/img/1.jpg'
    with open(image_path, 'rb') as f:
        image = f.read()
    image_base64 = str(base64.b64encode(image), encoding='utf-8')
    params = {
        "Image": image_base64,
        "MaxBodyNum": 10,
        "AttributesOptions": {
            "Orientation": True
        }
    }
    req.from_json_string(json.dumps(params))

    resp = client.DetectBody(req)
    BodyDetectResults = json.loads(resp.to_json_string())["BodyDetectResults"]
    BodyDetectResults_length = len(BodyDetectResults)
    i = 1
    for item in BodyDetectResults:
        print("第" + str(i) + "个人\n")
        print(item["BodyAttributeInfo"]["Orientation"])
        if item["BodyAttributeInfo"]["Orientation"]["Type"] == "背向":
            print(item["BodyRect"])
            print("\n")
            i = i + 1
            im = cv2.imread(image_path)
            cv2.rectangle(im, (item["BodyRect"]["X"], item["BodyRect"]["Y"]),
                          (item["BodyRect"]["X"] + item["BodyRect"]["Width"], item["BodyRect"]["Height"]),
                          (128, 0, 128), 3)
            save_path = "D:/"
            cv2.imencode('.jpg', im)[1].tofile(save_path)


except TencentCloudSDKException as err:
    print(err)
