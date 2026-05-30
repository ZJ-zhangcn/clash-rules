# Clash / Loon Rules

个人分流规则仓库。

## 目录

- `rules/clash/`：Clash classical payload YAML，格式为：

```yaml
payload:
  - DOMAIN-SUFFIX,example.com
```

- `rules/loon/`：Loon Rule-Set 列表，格式为：

```text
DOMAIN-SUFFIX,example.com
```

> `rules/` 根目录只保留分类目录；Clash 用 `rules/clash/`，Loon 用 `rules/loon/`。

## Loon Rule-Set 地址

优先使用 `.lsr`：

```text
https://raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/loon/Customer-Direct.lsr
https://raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/loon/Customer-Proxy-All.lsr
https://raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/loon/Customer-Proxy-HK.lsr
https://raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/loon/DNS.lsr
https://raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/loon/VPS.lsr
```

兼容保留 `.list`。

## 转换

更新 `rules/clash/` 后运行：

```bash
python3 scripts/convert-clash-to-loon.py
```
