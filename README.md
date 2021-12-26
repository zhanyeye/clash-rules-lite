## Clash 自定义代理规则--为开发者准备
+ 👀 根据个人需求定制的 `rules`, 方便开发和学习。为什么要自己定制 `rules` 呢 ？   
+ ✨ 因为 `GWFList` 添加的内容太多了，可能导致匹配速度慢，所以打算只保留我需要的匹配规则。

+ 🍒 代理规则列表：https://cdn.jsdelivr.net/gh/zhanyeye/clash-rules-for-dev@release/rules.txt

#### 使用方法
1. 拷贝一份订阅脚本到 `local file`.
<div align=center>
    <img width="750" src="https://user-images.githubusercontent.com/35565811/147398760-17324346-2fa3-4390-ad80-3d830ec8c58d.png">
</div>

2. 在 `local file` 脚本中追加 `rule-providers` 和 `script`
    + script 中 main 方法的返回值，需要根据自己情况定义（将"🔰 节点选择" 替换成 "你自己的代理"）

```
rule-providers:
  pac:
    type: http
    behavior: domain
    url: "https://cdn.jsdelivr.net/gh/zhanyeye/clash-rules-for-dev@release/rules.txt"
    path: ./rules/pac.yaml
    interval: 86400
script:
  code: |
    def main(ctx, metadata):
        keywords = ["google", "github"]
        for key in keywords:
            if key in metadata["host"]:
                return "🔰 节点选择"
        if ctx.rule_providers["pac"].match(metadata):
            return "🔰 节点选择"
        else:
            return "DIRECT"
```
3. 运行修改后的 `local file`
<div align=center>
    <img width="750" src="https://user-images.githubusercontent.com/35565811/147398721-88a75d2b-ce4d-4605-80a1-60871907f64d.png">
</div>
