# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request, render_template
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.auth import credentials
import requests
import json
from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest, DescribeInstanceStatusRequest

app = Flask(__name__)

metaUrl = 'http://100.100.100.200/latest/meta-data/ram/security-credentials/zheng'
region = 'cn-beijing'

# 获取临时身份凭证
def getStsToken():
	tokenResponse = requests.get(metaUrl)
	return tokenResponse.json()

# 主页为超链接
@app.route('/', methods=['HEAD', 'GET'])
def main_page():
  return render_template('main.html')

@app.route('/photo_of_zhuge', methods=['HEAD', 'GET'])
def photo_of_zhuge():
  return render_template('index.html')

# 在app.route装饰器中声明响应的URL和请求方法
@app.route('/ecs/getServerInfo', methods=['GET'])
def getServerInfo():
    tokenResult = getStsToken()
    accessKeyId = tokenResult['AccessKeyId']
    accessSecret = tokenResult['AccessKeySecret']
    securityToken = tokenResult['SecurityToken']
    credential = credentials.StsTokenCredential(accessKeyId, accessSecret, securityToken)
    client = AcsClient(credential=credential, region_id=region)

    # GET方式获取请求参数
    instanceId = request.args.get("instanceId")
    if instanceId is None:    
        return "Invalid Parameter"
    # 查询实例信息
    describeInstancesRequest = DescribeInstancesRequest.DescribeInstancesRequest()
    describeInstancesRequest.set_InstanceIds([instanceId])
    describeInstancesResponse = client.do_action_with_exception(describeInstancesRequest)
    # 返回数据为bytes类型，需要将bytes类型转换为str然后反序列化为json对象
    describeInstancesResponse = json.loads(str(describeInstancesResponse, 'utf-8'))
    print(describeInstancesResponse)
    if len(describeInstancesResponse['Instances']['Instance']) == 0:
        return jsonify({})

    instanceInfo = describeInstancesResponse['Instances']['Instance'][0]

    # 查询实例状态
    describeInstanceStatusRequest = DescribeInstanceStatusRequest.DescribeInstanceStatusRequest()
    describeInstanceStatusRequest.set_InstanceIds([instanceId])
    describeInstanceStatusResponse = client.do_action_with_exception(describeInstanceStatusRequest)
    describeInstanceStatusResponse = json.loads(str(describeInstanceStatusResponse, 'utf-8'))
    instanceStatus = describeInstanceStatusResponse['InstanceStatuses']['InstanceStatus'][0]['Status']

    # 封装结果
    result = {
        # cpu数
        'Cpu': instanceInfo['Cpu'],
        # 内存大小
        'Memory': instanceInfo['Memory'],
        # 操作系统名称
        'OSName': instanceInfo['OSName'],
        # 实例规格
        'InstanceType': instanceInfo['InstanceType'],
        # 实例公网IP地址
        'IpAddress': instanceInfo['PublicIpAddress']['IpAddress'][0],
        # 公网出带宽最大值
        'InternetMaxBandwidthOut': instanceInfo['InternetMaxBandwidthOut'],
        # 实例状态
        'instanceStatus': instanceStatus
    }
    return jsonify(result)


if __name__ == "__main__":
    app.run()
