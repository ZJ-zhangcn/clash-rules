# Clash / Loon / Stash Rules

个人分流规则仓库，同时维护 Clash/Mihomo、Loon 和 Stash 格式。

## 快速入口

- [Clash/Mihomo 主配置](https://raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules.yaml)
- [Clash 规则](#clashmihomo-规则)
- [Loon 规则](#loon-规则)
- [Stash 覆写](#stash-覆写)

## 目录结构

```text
rules.yaml                              # Clash/Mihomo 主配置
rules/
├── clash/                              # Clash classical payload 规则
├── loon/                               # Loon Rule-Set，使用 .lsr
└── stash/
    ├── *.stoverride                    # Stash 公共覆写，保持平铺以稳定 Raw URL
    └── sources/loon-plugins.json       # Loon 源插件清单
scripts/
├── convert-clash-to-loon.py             # Clash YAML → Loon LSR
└── convert-loon-to-stash.py             # Loon LPX → Stash Override
.github/workflows/
└── update-stash-overrides.yml           # 每日自动追踪上游插件
sub-store-dialer.js                      # Sub-Store 辅助脚本
```

`rules/stash/*.stoverride` 保持在固定路径，是为了不破坏已经分享或收藏的 Raw/快捷安装链接。

## Clash/Mihomo 规则

规则文件位于 `rules/clash/`，格式示例：

```yaml
payload:
  - DOMAIN-SUFFIX,example.com
  - IP-CIDR,1.1.1.1/32
```

| 文件 | Raw |
| --- | --- |
| `Customer-Direct.yaml` | [Raw](https://raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/clash/Customer-Direct.yaml) |
| `Customer-Proxy-All.yaml` | [Raw](https://raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/clash/Customer-Proxy-All.yaml) |
| `Customer-Proxy-DE.yaml` | [Raw](https://raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/clash/Customer-Proxy-DE.yaml) |
| `Customer-Proxy-HK.yaml` | [Raw](https://raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/clash/Customer-Proxy-HK.yaml) |
| `Customer-Proxy-JP.yaml` | [Raw](https://raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/clash/Customer-Proxy-JP.yaml) |
| `Customer-Proxy-US.yaml` | [Raw](https://raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/clash/Customer-Proxy-US.yaml) |
| `Customer-Proxy-USGT.yaml` | [Raw](https://raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/clash/Customer-Proxy-USGT.yaml) |
| `DNS.yaml` | [Raw](https://raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/clash/DNS.yaml) |

## Loon 规则

规则文件位于 `rules/loon/`，使用 `.lsr` 后缀：

```text
DOMAIN-SUFFIX,example.com
IP-CIDR,1.1.1.1/32
```

| 文件 | Raw |
| --- | --- |
| `Customer-Direct.lsr` | [Raw](https://raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/loon/Customer-Direct.lsr) |
| `Customer-Proxy-All.lsr` | [Raw](https://raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/loon/Customer-Proxy-All.lsr) |
| `Customer-Proxy-DE.lsr` | [Raw](https://raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/loon/Customer-Proxy-DE.lsr) |
| `Customer-Proxy-HK.lsr` | [Raw](https://raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/loon/Customer-Proxy-HK.lsr) |
| `Customer-Proxy-JP.lsr` | [Raw](https://raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/loon/Customer-Proxy-JP.lsr) |
| `Customer-Proxy-US.lsr` | [Raw](https://raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/loon/Customer-Proxy-US.lsr) |
| `Customer-Proxy-USGT.lsr` | [Raw](https://raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/loon/Customer-Proxy-USGT.lsr) |
| `DNS.lsr` | [Raw](https://raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/loon/DNS.lsr) |

## Stash 覆写

在 iPhone 上用 Safari/GitHub 打开后，点击“添加到 Stash”即可进入覆写安装流程；也可以点击 Raw 后，在 Stash 中选择从 URL 安装。

<!-- BEGIN STASH OVERRIDES -->
| 覆写 | 快捷添加 | Raw |
| --- | --- | --- |
| 番茄小说去广告 (`DragonRead_remove_ads.stoverride`) | [添加到 Stash](https://link.stash.ws/install-override/raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/stash/DragonRead_remove_ads.stoverride) | [Raw](https://raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/stash/DragonRead_remove_ads.stoverride) |
| 招商银行开屏广告 (`cmb-startup-ad.stoverride`) | [添加到 Stash](https://link.stash.ws/install-override/raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/stash/cmb-startup-ad.stoverride) | [Raw](https://raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/stash/cmb-startup-ad.stoverride) |
| 沃尔玛去广告 (`Walmart_remove_ads.stoverride`) | [添加到 Stash](https://link.stash.ws/install-override/raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/stash/Walmart_remove_ads.stoverride) | [Raw](https://raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/stash/Walmart_remove_ads.stoverride) |
| 盒马开屏广告 (`freshippo-splash.stoverride`) | [添加到 Stash](https://link.stash.ws/install-override/raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/stash/freshippo-splash.stoverride) | [Raw](https://raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/stash/freshippo-splash.stoverride) |
| 得物去广告 (`Dewu_remove_ads.stoverride`) | [添加到 Stash](https://link.stash.ws/install-override/raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/stash/Dewu_remove_ads.stoverride) | [Raw](https://raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/stash/Dewu_remove_ads.stoverride) |
| 闲鱼去广告 (`FleaMarket_remove_ads.stoverride`) | [添加到 Stash](https://link.stash.ws/install-override/raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/stash/FleaMarket_remove_ads.stoverride) | [Raw](https://raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/stash/FleaMarket_remove_ads.stoverride) |
| 微信公众号去广告 (`Weixin_Official_Accounts_remove_ads.stoverride`) | [添加到 Stash](https://link.stash.ws/install-override/raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/stash/Weixin_Official_Accounts_remove_ads.stoverride) | [Raw](https://raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/stash/Weixin_Official_Accounts_remove_ads.stoverride) |
| 拼多多去广告 (`PinDuoDuo_remove_ads.stoverride`) | [添加到 Stash](https://link.stash.ws/install-override/raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/stash/PinDuoDuo_remove_ads.stoverride) | [Raw](https://raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/stash/PinDuoDuo_remove_ads.stoverride) |
| 高德地图去广告 (`Amap_remove_ads.stoverride`) | [添加到 Stash](https://link.stash.ws/install-override/raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/stash/Amap_remove_ads.stoverride) | [Raw](https://raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/stash/Amap_remove_ads.stoverride) |
| 菜鸟去广告 (`Cainiao_remove_ads.stoverride`) | [添加到 Stash](https://link.stash.ws/install-override/raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/stash/Cainiao_remove_ads.stoverride) | [Raw](https://raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/stash/Cainiao_remove_ads.stoverride) |
| Google 中国跳转 (`Google.stoverride`) | [添加到 Stash](https://link.stash.ws/install-override/raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/stash/Google.stoverride) | [Raw](https://raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/stash/Google.stoverride) |
| 淘宝去广告 (`Taobao_remove_ads.stoverride`) | [添加到 Stash](https://link.stash.ws/install-override/raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/stash/Taobao_remove_ads.stoverride) | [Raw](https://raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/stash/Taobao_remove_ads.stoverride) |
| YouTube 去广告 (`YouTube_remove_ads.stoverride`) | [添加到 Stash](https://link.stash.ws/install-override/raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/stash/YouTube_remove_ads.stoverride) | [Raw](https://raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/stash/YouTube_remove_ads.stoverride) |
| 哔哩哔哩去广告 (`Bilibili_remove_ads.stoverride`) | [添加到 Stash](https://link.stash.ws/install-override/raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/stash/Bilibili_remove_ads.stoverride) | [Raw](https://raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/stash/Bilibili_remove_ads.stoverride) |
| 夸克浏览器去广告 (`QuarkBrowser_remove_ads.stoverride`) | [添加到 Stash](https://link.stash.ws/install-override/raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/stash/QuarkBrowser_remove_ads.stoverride) | [Raw](https://raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/stash/QuarkBrowser_remove_ads.stoverride) |
| 起点读书去广告 (`QiDian_remove_ads.stoverride`) | [添加到 Stash](https://link.stash.ws/install-override/raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/stash/QiDian_remove_ads.stoverride) | [Raw](https://raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/stash/QiDian_remove_ads.stoverride) |
| 网易云音乐去广告 (`NeteaseCloudMusic_remove_ads.stoverride`) | [添加到 Stash](https://link.stash.ws/install-override/raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/stash/NeteaseCloudMusic_remove_ads.stoverride) | [Raw](https://raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/stash/NeteaseCloudMusic_remove_ads.stoverride) |
| 下厨房去广告 (`XiaChuFang_remove_ads.stoverride`) | [添加到 Stash](https://link.stash.ws/install-override/raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/stash/XiaChuFang_remove_ads.stoverride) | [Raw](https://raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/stash/XiaChuFang_remove_ads.stoverride) |
| 京东去广告 (`JD_remove_ads.stoverride`) | [添加到 Stash](https://link.stash.ws/install-override/raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/stash/JD_remove_ads.stoverride) | [Raw](https://raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/stash/JD_remove_ads.stoverride) |
| 什么值得买去广告 (`smzdm_remove_ads.stoverride`) | [添加到 Stash](https://link.stash.ws/install-override/raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/stash/smzdm_remove_ads.stoverride) | [Raw](https://raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/stash/smzdm_remove_ads.stoverride) |
| QQ音乐去广告 (`QQKSong_remove_ads.stoverride`) | [添加到 Stash](https://link.stash.ws/install-override/raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/stash/QQKSong_remove_ads.stoverride) | [Raw](https://raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/stash/QQKSong_remove_ads.stoverride) |
| Twitter 去广告 (`Twitter.stoverride`) | [添加到 Stash](https://link.stash.ws/install-override/raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/stash/Twitter.stoverride) | [Raw](https://raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/stash/Twitter.stoverride) |
| 中国电信去广告 (`ChinaTelecom.stoverride`) | [添加到 Stash](https://link.stash.ws/install-override/raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/stash/ChinaTelecom.stoverride) | [Raw](https://raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/stash/ChinaTelecom.stoverride) |
| Hello (`Hello.stoverride`) | [添加到 Stash](https://link.stash.ws/install-override/raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/stash/Hello.stoverride) | [Raw](https://raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/stash/Hello.stoverride) |
| 微博去广告 (`Weibo_remove_ads.stoverride`) | [添加到 Stash](https://link.stash.ws/install-override/raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/stash/Weibo_remove_ads.stoverride) | [Raw](https://raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/stash/Weibo_remove_ads.stoverride) |
| 美团外卖去广告 (`Meituan-MeituanWaimai.stoverride`) | [添加到 Stash](https://link.stash.ws/install-override/raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/stash/Meituan-MeituanWaimai.stoverride) | [Raw](https://raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/stash/Meituan-MeituanWaimai.stoverride) |
| 微信小程序去广告 (`WexinMiniPrograms_Remove_ads.stoverride`) | [添加到 Stash](https://link.stash.ws/install-override/raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/stash/WexinMiniPrograms_Remove_ads.stoverride) | [Raw](https://raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/stash/WexinMiniPrograms_Remove_ads.stoverride) |
| 微信外部链接解锁 (`Weixin_external_links_unlock.stoverride`) | [添加到 Stash](https://link.stash.ws/install-override/raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/stash/Weixin_external_links_unlock.stoverride) | [Raw](https://raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/stash/Weixin_external_links_unlock.stoverride) |
| 京东历史价格 (`JD_Price.stoverride`) | [添加到 Stash](https://link.stash.ws/install-override/raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/stash/JD_Price.stoverride) | [Raw](https://raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/stash/JD_Price.stoverride) |
| QQ链接跳转 (`QQ_Redirect.stoverride`) | [添加到 Stash](https://link.stash.ws/install-override/raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/stash/QQ_Redirect.stoverride) | [Raw](https://raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/stash/QQ_Redirect.stoverride) |
| Apple天气增强 (`AppleWeatherEnhancer.stoverride`) | [添加到 Stash](https://link.stash.ws/install-override/raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/stash/AppleWeatherEnhancer.stoverride) | [Raw](https://raw.githubusercontent.com/ZJ-zhangcn/clash-rules/main/rules/stash/AppleWeatherEnhancer.stoverride) |
<!-- END STASH OVERRIDES -->

## 更新与维护

### 手动转换

```bash
# Clash YAML → Loon LSR
python3 scripts/convert-clash-to-loon.py

# 拉取清单中的 Loon LPX → Stash Override，并刷新本 README 的快捷链接
python3 scripts/convert-loon-to-stash.py
```

Loon 源插件清单位于 `rules/stash/sources/loon-plugins.json`。其中 `kelee.one` 源不可访问时，转换器会自动使用已验证的镜像地址；其他源按清单原地址抓取。

### 自动追踪

`.github/workflows/update-stash-overrides.yml` 每日运行，也可在 GitHub Actions 中手动触发：

1. 拉取清单中的上游 LPX；
2. 重新生成 Stash 覆写；
3. 更新本 README 的快捷安装表；
4. 有变化时自动提交到 `main`。

### 规则约定

- Clash 使用 `.yaml`，Loon 使用 `.lsr`，Stash 使用 `.stoverride`。
- Stash 公共覆写保持在 `rules/stash/` 根目录，避免已有 URL 失效。
- 生成的 Stash 覆写只使用 Stash 支持的字段；Loon 专属字段不会原样写入。
