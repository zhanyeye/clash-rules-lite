<p align="center">
  <img width="100px" src="https://user-images.githubusercontent.com/35565811/214613019-6fd702b7-445e-4663-8471-f47005241724.png" align="center" alt="GitHub Readme Stats" />
  <h2 align="center">Clash Rules Lite</h2>
 
  <p align="center">🍒 自定义代理规则，精简匹配规则。</p>
 
  <p align="center">
    <a href="https://github.com/zhanyeye/clash-rules-lite/blob/master/.github/workflows/release.yml">
    <img src="https://github.com/zhanyeye/clash-rules-lite/actions/workflows/release.yml/badge.svg" />
    </a>
  </p>
 
  <p align="center">
    <a href="https://github.com/zhanyeye/clash-rules-lite/blob/main/proxy-rules.txt">代理规则列表</a> |
    <a href="https://github.com/zhanyeye/clash-rules-lite/blob/main/microsoft-rules.txt">微软服务规则列表</a> |
    <a href="https://github.com/zhanyeye/clash-rules-lite/blob/main/blacklist-rules.txt">黑名单规则列表</a>
  </p>

</p>

<p>
  <pre align="center">
  https://cdn.jsdelivr.net/gh/zhanyeye/clash-rules-lite@release/proxy-rules.txt    
  https://cdn.jsdelivr.net/gh/zhanyeye/clash-rules-lite@release/microsoft-rules.txt
  https://cdn.jsdelivr.net/gh/zhanyeye/clash-rules-lite@release/blacklist-rules.txt</pre>
</p>


### 工具介绍
+ Clash 默认的GFW代理规则内容太多，使用过程中明显感觉到有延迟
+ 本工具的想法是代理规则一边用一边添加，毕竟我们访问的网站应该很有限
+ 该工具的目的是删除不必要的代理规则，方便用户自定义代理的内容
+ 代理规则放在github仓库中方便多设备同步，只需编辑[rules.txt](https://github.com/zhanyeye/clash-rules-lite/blob/main/rules.txt)即可
+ 当用户更新规则后，使用Github Actions自动将规则缓存到免费CDN上 
+ 用户在 github 上更新规则后，在 clash 的 providers 上点击刷新即可拉取更新


### 如何自定义
1. fork 本仓库：[Fork zhanyeye/clash-rules-lite](https://github.com/zhanyeye/clash-rules-lite/fork) 
2. 触发 GitHub Action 中的 `Generate Rules for Clash` 工作流
3. 编辑 `xx-rules.txt` 以自定义规则
4. 在对应的 Clash 上刷新配置文件

<div align="center">
  <center>
    <img style="border-radius: 0.3125em;
    box-shadow: 0 2px 4px 0 rgba(34,36,38,.12),0 2px 10px 0 rgba(34,36,38,.08);" 
    src="https://user-images.githubusercontent.com/35565811/184524456-e956ef59-4577-44e9-9b99-4a8684b77e40.png">
    <br>
    <div style="color:orange; border-bottom: 1px solid #d9d9d9;
    display: inline-block;
    color: #999;
    padding: 2px;">启动流水线示意图</div>
  </center>
</div>


Tips:
> a. 可通过访问进行验证 `https://cdn.jsdelivr.net/gh/{你的GITHUB用户名}/clash-rules-lite@release/`   
> c. **该仓中以 rules.txt 结尾的文件，都会缓存到 jsdelivr CDN中，可以自定义！**    


### 在 Clash Desktop 中生效

1. 鼠标右击订阅的配置文件选中“复制”，将复制的文件命名为`local`（因为更新订阅链接时会覆盖你的修改）

<div align="center">
  <center>
    <img width="800" style="border-radius: 0.3125em;
    box-shadow: 0 2px 4px 0 rgba(34,36,38,.12),0 2px 10px 0 rgba(34,36,38,.08);" 
    src="https://user-images.githubusercontent.com/35565811/184479698-dbc0f06b-7313-4448-a694-cad3d9d5dbe3.png">
    <br>
    <div style="color:orange; border-bottom: 1px solid #d9d9d9;
    display: inline-block;
    color: #999;
    padding: 2px;">拷贝一份配置订阅文件</div>
  </center>
</div>



2. 在你复制的 `local` 配置中，修改配置如下，注意 `proxies`, `proxy-groups` 和 `{YOUR-GITHUB-USERNAME}` 修改为你的配置（加粗的部分）


<pre><code> 
mixed-port: 7890
allow-lan: true
bind-address: '*'
mode: rule
log-level: silent
external-controller: '127.0.0.1:9090'
proxies:
    <b>- { name: '1-香港', type: *, server: **, port: *, cipher: **, password: **, udp: true }</b>
    <b>- { name: '2-香港', type: *, server: **, port: *, cipher: **, password: **, udp: true }</b>
    <b>- ...</b>
proxy-groups:
    <b>- { name: '🔰 节点选择', type: select, proxies: ['1-香港', '2-香港'] }</b>
    <b>- { name: '🎯 全球直连', type: select, proxies: ['DIRECT'] }</b>
    <b>- { name: '🛑 全球拦截', type: select, proxies: ['REJECT'] }</b>
    <b>- { name: 'Ⓜ️ 微软服务', type: select, proxies: ['🎯 全球直连', ] }</b>
    <b>- { name: '🐟 漏网之鱼', type: select, proxies: ['🔰 节点选择'] }</b>
    <b>- ...</b>
rules:
  - RULE-SET,Proxy,🔰 节点选择
  - RULE-SET,Microsoft,Ⓜ️ 微软服务
  - RULE-SET,Backlist,🛑 全球拦截
  - GEOIP,CN,🎯 全球直连
  - MATCH,🐟 漏网之鱼
rule-providers:
  Proxy:
    type: http
    behavior: classical
    url: "https://cdn.jsdelivr.net/gh/zhanyeye/clash-rules-lite@release/proxy-rules.txt"
    path: ./providers/rule-proxy.yaml
    interval: 86400
  Microsoft:
    type: http
    behavior: classical
    url: "https://cdn.jsdelivr.net/gh/zhanyeye/clash-rules-lite@release/microsoft-rules.txt"
    path: ./providers/rule-microsoft.yaml
    interval: 86400
  Backlist:
    type: http
    behavior: classical
    url: "https://cdn.jsdelivr.net/gh/zhanyeye/clash-rules-lite@release/blacklist-rules.txt"
    path: ./providers/rule-backlist.yaml
    interval: 86400 

</code></pre>


3. 运行修改后的 `local` 配置，再切换成 `Rule` 模式

<div align="center">
  <center>
    <img width="800" style="border-radius: 0.3125em;
    box-shadow: 0 2px 4px 0 rgba(34,36,38,.12),0 2px 10px 0 rgba(34,36,38,.08);" 
    src="https://user-images.githubusercontent.com/35565811/184479791-6e2c12ca-d28f-4009-839a-e9a06bdcff00.png">
    <br>
    <div style="color:orange; border-bottom: 1px solid #d9d9d9;
    display: inline-block;
    color: #999;
    padding: 2px;">运行修改后的本地配置</div>
  </center>
</div>

### 在OpenWrt的OpenClash中生效
> OpenWrt 是一个软路由系统，如果你没有用到，请忽略”

需要更新配置文件的`rules`和 `rule-providers`, 注意：
+ 用户名需要替换成用户自己的!!!
+ rules 中所属的group需要替换成自己的 `proxy-groups`!!!
```
rules:
  - RULE-SET,Proxy,🔰 节点选择
  - RULE-SET,Microsoft,Ⓜ️ 微软服务
  - RULE-SET,Backlist,🛑 全球拦截
  - GEOIP,CN,🎯 全球直连
  - MATCH,🐟 漏网之鱼
rule-providers:
  Proxy:
    type: http
    behavior: classical
    url: "https://cdn.jsdelivr.net/gh/zhanyeye/clash-rules-lite@release/proxy-rules.txt"
    path: ./providers/rule-proxy.yaml
    interval: 86400
  Microsoft:
    type: http
    behavior: classical
    url: "https://cdn.jsdelivr.net/gh/zhanyeye/clash-rules-lite@release/microsoft-rules.txt"
    path: ./providers/rule-microsoft.yaml
    interval: 86400
  Backlist:
    type: http
    behavior: classical
    url: "https://cdn.jsdelivr.net/gh/zhanyeye/clash-rules-lite@release/blacklist-rules.txt"
    path: ./providers/rule-backlist.yaml
    interval: 86400 
```





### 自定义代理规则
+ 修改代码仓中以 rule.txt 结尾的文件即可, 也可以自己新增以rule.txt结尾的配置，都会生效
+ 修改后需要在clash中刷新，并重启clash才能生效

> clash desktop 中刷新操作
<div align="center">
  <center>
    <img width="800" style="border-radius: 0.3125em;
    box-shadow: 0 2px 4px 0 rgba(34,36,38,.12),0 2px 10px 0 rgba(34,36,38,.08);" 
    src="https://user-images.githubusercontent.com/35565811/184480450-c24dd895-2b8a-4cfb-8f9e-77843c3df5af.png">
    <br>
    <div style="color:orange; border-bottom: 1px solid #d9d9d9;
    display: inline-block;
    color: #999;
    padding: 2px;">Clash 客户端上刷新 providers, 并重启clash</div>
  </center>
</div>

> OpenClash 中刷新操作

配置文件管理 -> 规则集文件列表 -> 删除所有文件 -> 返回概览 -> 应用配置
<div align="center">
  <center>
    <img width="800" style="border-radius: 0.3125em;
    box-shadow: 0 2px 4px 0 rgba(34,36,38,.12),0 2px 10px 0 rgba(34,36,38,.08);" 
    src="https://user-images.githubusercontent.com/35565811/214744014-f348b5af-477f-465c-842d-e40d36d4a92b.png">
    <br>
    <div style="color:orange; border-bottom: 1px solid #d9d9d9;
    display: inline-block;
    color: #999;
    padding: 2px;">OpenClash上删除规则集文件, 并重新应用配置</div>
  </center>
</div>


+ jsdelivr CDN 缓存没有更新怎么办？

> 这是因为 jsdelivr CDN 缓存的原因，一般来说是 24小时刷新缓存，但是这样太慢了！   
> 不过 jsdelivr CDN 也提供手动刷新缓存的方法：
```
# 假设你的文件 URL 是这样：
https://cdn.jsdelivr.net/xxx/xxx...

# 那么把域名中的 cdn 改为 purge 即可：
https://purge.jsdelivr.net/xxx/xxx...
```
然后访问这个文件新 URL 就会提示你刷新成功！

