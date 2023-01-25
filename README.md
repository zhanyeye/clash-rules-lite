<p align="center">
 <img width="100px" src="https://github.com/Dreamacro/clash/raw/master/docs/logo.png" align="center" alt="GitHub Readme Stats" />
 <h2 align="center">Clash Rules Lite</h2>
 
 <p align="center">🍒 自定义代理规则，精简匹配规则 (<b>代理匹配速度明显提升</b>)。</p>
 
 <p align="center">
  <a href="https://github.com/zhanyeye/clash-rules-lite/blob/master/.github/workflows/release.yml">
   <img src="https://github.com/zhanyeye/clash-rules-lite/actions/workflows/release.yml/badge.svg" />
  </a>
 </p>
 
 <p>
  <pre align="center">
  https://cdn.jsdelivr.net/gh/zhanyeye/clash-rules-lite@release/proxy-rules.txt    
  https://cdn.jsdelivr.net/gh/zhanyeye/clash-rules-lite@release/microsoft-rules.txt
  https://cdn.jsdelivr.net/gh/zhanyeye/clash-rules-lite@release/blacklist-rules.txt</pre>
 </p>
 <p align="center">
 <a href="https://github.com/zhanyeye/clash-rules-lite/blob/main/proxy-rules.txt">代理规则列表</a> |
 <a href="https://github.com/zhanyeye/clash-rules-lite/blob/main/microsoft-rules.txt">微软服务规则列表</a> |
 <a href="https://github.com/zhanyeye/clash-rules-lite/blob/main/blacklist-rules.txt">黑名单规则列表</a>
 </p>

</p>

> Tips: 有200M以上宽带，且有多设备同时使用代理需求，可以考虑上能刷固件的路由器，或者软路由，刷OpenWrt使用OpenClash插件，使用体验也会不错~ （一般使用买便宜的就够了）


### 工具介绍
+ Clash 默认的GFW代理规则内容太多，使用过程中明显感觉到有延迟
+ 本工具的想法是代理规则一边用一边添加，毕竟我们访问的网站应该很有限
+ 该工具的目的是删除不必要的代理规则，方便用户自定义代理的内容
+ 代理规则放在github仓库中方便多设备同步，只需编辑[rules.txt](https://github.com/zhanyeye/clash-rules-lite/blob/main/rules.txt)即可
+ 当用户更新规则后，使用Github Actions自动将规则缓存到免费CDN上 
+ 用户在 github 上更新规则后，在 clash 的 providers 上点击刷新即可拉取更新


### 如何自定义
1. fork 本仓库：[Fork zhanyeye/clash-rules-lite](https://github.com/zhanyeye/clash-rules-lite/fork) 
2. 启动 GitHub Action，并手动触发 `Generate Rules for Clash` 工作流，若执行成功，则Github端配置已完成
3. 编辑 `xx-rules.txt` 以自定义规则，**该仓中以 rules.txt 结尾的文件，都会缓存到 jsdelivr CDN中，可以自定义！**
4. 在对应的 Clash 上刷新配置文件。

<div>
    <img width="750" src="https://user-images.githubusercontent.com/35565811/184524456-e956ef59-4577-44e9-9b99-4a8684b77e40.png">
</div>



> a. 设置完成后可通过访问 https://cdn.jsdelivr.net/gh/{GITHUB-USERNAME}/clash-rules-lite@release/rules.txt 来验证    
> b. {GITHUB-USERNAME} 需替换成自己的GitHub用户名

### 在软路由的OpenClash中生效




### 在 Clash 中生效

3. 鼠标右击订阅的配置文件选中“复制”，将复制的文件命名为`local`（因为更新订阅链接时会覆盖你的修改）

<div>
    <img width="750" src="https://user-images.githubusercontent.com/35565811/184479698-dbc0f06b-7313-4448-a694-cad3d9d5dbe3.png">
</div>


4. 在你复制的 `local` 配置中，修改配置如下，注意 `proxies`, `proxy-groups` 和 `{YOUR-GITHUB-USERNAME}` 修改为你的配置（加粗的部分）


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
proxy-groups:
    <b>- { name: 'PROXY', type: select, proxies: ['1-香港', '2-香港'] }</b>
rules:
  - DOMAIN-KEYWORD,github,PROXY
  - DOMAIN-KEYWORD,google,PROXY
  - RULE-SET,pac,PROXY
rule-providers:
  pac:
    type: http
    behavior: domain
    url: "https://cdn.jsdelivr.net/gh/<b>{YOUR-GITHUB-USERNAME}</b>/clash-rules-lite@release/rules.txt"
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

</code></pre>


5. 运行修改后的 `local` 配置，再切换成 `Rule` 或 `Script` 模式
<div>
    <img width="750" src="https://user-images.githubusercontent.com/35565811/184479791-6e2c12ca-d28f-4009-839a-e9a06bdcff00.png">
</div>


#### 自定义代理规则
修改仓库中[rules.txt](https://github.com/zhanyeye/clash-rules-lite/blob/main/rules.txt)，修改完后会自动更新并邮件提醒（有可能没有邮件提醒），然后在 Clash 上刷新 providers
<div>
    <img width="750" src="https://user-images.githubusercontent.com/35565811/184480450-c24dd895-2b8a-4cfb-8f9e-77843c3df5af.png">
</div>


