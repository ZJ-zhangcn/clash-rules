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

> 根目录下旧的 `rules/*.yaml` / `rules/*.ymal` 暂时保留，避免旧订阅地址失效；新配置建议使用 `rules/clash/` 或 `rules/loon/`。

## Loon Rule-Set 地址

```text
https://raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/loon/Customer-Direct.list
https://raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/loon/Customer-Proxy-All.list
https://raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/loon/Customer-Proxy-HK.list
https://raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/loon/DNS.list
https://raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/loon/VPS.list
```

## 转换

更新 `rules/clash/` 后运行：

```bash
python3 scripts/convert-clash-to-loon.py
```
