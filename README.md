## PAC 自定义规则
根据个人需求定制的 `PAC`, 用于方便开发和学习   

+ 👀 为什么要自己定制`pac`呢 ？   
+ ✨ 因为`GWFList` 添加的内容太多了，导致匹配速度很慢；例如我在 `PAC` 模式下访问 GitHub 并不顺畅。    
+ 🤣 所以打算只保留我需要的匹配规则。

+ 📖 我会不断精简和添加 `PAC` 文件规则的~

clash profile 补充脚本
```
rule-providers:
  pac:
    type: http
    behavior: domain
    url: "https://gitee.com/zhanzeye/PAC/raw/master/clash.txt"
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
