# -*- coding: utf-8 -*-
from com.aliyun.api.gateway.sdk import client
from com.aliyun.api.gateway.sdk.http import request
from com.aliyun.api.gateway.sdk.common import constant

host = "https://otc.bjsdfx.com"
url = "/api/options/quotes/30min.csv"

cli = client.DefaultClient(app_key="app_key", app_secret="app_secret")

headers = {
	# 测试环境需要加入以下头，正式环境请移除
	'X-Ca-Stage': 'TEST',
	# debug, 建议生产关闭
	'X-Ca-Request-Mode': 'debug',
}

def print_response(code, headers, response):
	for h in headers:
		print '%s: %s' % h

	if code == 200 :
		print response
	else:
		print 'StatusCode: %d' % code
	print '\n\n'

# Check last modified only
req = request.Request(host=host, protocol=constant.HTTPS, url=url+"?headOnly=true", headers=headers, method="GET", time_out=30000)
print_response(*cli.execute(req))

# GET
req = request.Request(host=host, protocol=constant.HTTPS, url=url, headers=headers, method="GET", time_out=30000)

print_response(*cli.execute(req))
