# Clash / Loon Rules

个人分流规则仓库，同时维护 Clash 与 Loon 两套规则格式。

## 目录结构

```text
rules.yaml                         # Clash 主配置
rules/clash/                       # Clash classical payload 规则
rules/loon/                        # Loon Rule-Set 规则，使用 .lsr 后缀
scripts/convert-clash-to-loon.py   # Clash -> Loon 转换脚本
```

## Clash 规则

Clash 规则放在 `rules/clash/`，格式示例：

```yaml
payload:
  - DOMAIN-SUFFIX,example.com
  - IP-CIDR,1.1.1.1/32
```

当前 Clash 规则：

- `Customer-Direct.yaml`：6 条，Raw：`https://raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/clash/Customer-Direct.yaml`
- `Customer-Proxy-All.yaml`：2 条，Raw：`https://raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/clash/Customer-Proxy-All.yaml`
- `Customer-Proxy-HK.yaml`：5 条，Raw：`https://raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/clash/Customer-Proxy-HK.yaml`
- `DNS.ymal`：4 条，Raw：`https://raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/clash/DNS.ymal`
- `VPS.ymal`：2 条，Raw：`https://raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/clash/VPS.ymal`

## Loon 规则

Loon 规则放在 `rules/loon/`，只保留 `.lsr` 文件，格式示例：

```text
DOMAIN-SUFFIX,example.com
IP-CIDR,1.1.1.1/32
```

当前 Loon 规则：

- `Customer-Direct.lsr`：6 条，Raw：`https://raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/loon/Customer-Direct.lsr`
- `Customer-Proxy-All.lsr`：2 条，Raw：`https://raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/loon/Customer-Proxy-All.lsr`
- `Customer-Proxy-HK.lsr`：5 条，Raw：`https://raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/loon/Customer-Proxy-HK.lsr`
- `DNS.lsr`：4 条，Raw：`https://raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/loon/DNS.lsr`
- `VPS.lsr`：2 条，Raw：`https://raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/loon/VPS.lsr`

## 更新流程

1. 修改 `rules/clash/` 下的 YAML 文件。
2. 运行转换脚本：

```bash
python3 scripts/convert-clash-to-loon.py
```

3. 检查 `rules/loon/` 下对应 `.lsr` 是否更新。
4. 提交并推送。

## 说明

- `rules/` 根目录不放单独规则文件，只区分 `clash/` 和 `loon/`。
- Loon 使用 `.lsr`，不再生成 `.list`。
- `DNS.ymal`、`VPS.ymal` 当前保留原文件名，避免改名影响已有 Clash 引用。
