"""
用于从订阅链接解析配置，生成自定义的配置文件
"""
import base64
import requests
import re
import urllib.request

url = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX_URL'  # 你自己的订阅URL
template = 'mixed-port: 7890\nallow-lan: true\nbind-address: \'*\'\nmode: rule\nlog-level: silent\nexternal-controller: \'127.0.0.1:9090\'\nproxies:\n{proxy_list}proxy-groups:\n    - {{ name: \'PROXY\', type: select, proxies: {name_list} }}\nrules:\n  - DOMAIN-KEYWORD,github,PROXY\n  - DOMAIN-KEYWORD,google,PROXY\n  - RULE-SET,pac,PROXY\nrule-providers:\n  pac:\n    type: http\n    behavior: domain\n    url: "https://cdn.jsdelivr.net/gh/zhanyeye/clash-rules-lite@release/rules.txt"\n    path: ./rules/pac.yaml\n    interval: 86400\nscript:\n  code: |\n    def main(ctx, metadata):\n        keywords = ["google", "github"]\n        for key in keywords:\n            if key in metadata["host"]:\n                return "PROXY"\n        if ctx.rule_providers["pac"].match(metadata):\n            return "PROXY"\n        else:\n            return "DIRECT"\n'
proxy_list = ''
name_list = []

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
