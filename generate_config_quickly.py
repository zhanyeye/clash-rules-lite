"""
用于从订阅链接解析配置，生成自定义的配置文件
"""

import base64
import requests
import re
import urllib.request


url = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'  # 订阅URL
proxy_list = ''
name_list = []


template = '''mixed-port: 7890
allow-lan: true
bind-address: '*'
mode: rule
log-level: silent
external-controller: '127.0.0.1:9090'
proxies:
{proxy_list}proxy-groups:
    - {{ name: 'PROXY', type: select, proxies: {name_list} }}
rules:
  - DOMAIN-KEYWORD,github,PROXY
  - DOMAIN-KEYWORD,google,PROXY
  - RULE-SET,pac,PROXY
rule-providers:
  pac:
    type: http
    behavior: domain
    url: "https://cdn.jsdelivr.net/gh/zhanyeye/clash-rules-lite@release/rules.txt"
    path: ./rules/pac.yaml
    interval: 86400
script:
  code: |
    def main(ctx, metadata):
        keywords = ["google", "github"]
        for key in keywords:
            if key in metadata["host"]:
                return "PROXY"
        if ctx.rule_providers["pac"].match(metadata):
            return "PROXY"
        else:
            return "DIRECT"
'''



def decode_ss(ss):
    args = re.split('@|#', ss)
    cipher = base64.b64decode(args[0][5:] + '=' ).decode('ascii').split(':')[0]
    password = base64.b64decode(args[0][5:] + '=' ).decode('ascii').split(':')[1]
    server = args[1].split(':')[0]
    port = args[1].split(':')[1]
    name = urllib.request.unquote(args[2])
    name_list.append(name)
    return "    - {{ name: '{name}', type: ss, server: {server}, port: {port}, cipher: {cipher}, password: {password}, udp: true }}\r\n".format(name=name, server=server, port=port, cipher=cipher, password=password)



try:
    base64_str = requests.get(url=url).text
    ss_str_list = base64.b64decode(base64_str).decode('ascii').split('\r\n')

    for ss in ss_str_list:
        if ss != '':
            proxy_list = proxy_list + decode_ss(ss)

    res = template.format(proxy_list = proxy_list, name_list = name_list)
    print(res)
    
    fh = open('config.yml', 'w')
    fh.write(res)
    fh.close()
    
except Exception:
    print("订阅url出现问题，请检测url或更新代码")
