/**
 * Sub-Store Mihomo 配置覆写脚本：家宽节点经香港自建中转
 *
 * 目标链路：用户设备 -> 香港自建节点 -> 自建家宽 HTTP/SOCKS 节点 -> 目标网站
 *
 * 使用方式：
 * 1. 在 Sub-Store 的 Mihomo 配置覆写脚本中粘贴本文件内容；
 * 2. 确认 DIALER_NAME 与你的香港中转策略组/具体节点名完全一致；
 * 3. 如需保留原始直连家宽节点，把 SUFFIX 改成 "-via-HK"；
 *    如不保留原始直连节点，保持 SUFFIX = ""，脚本会直接修改原节点。
 */
function main(config) {
  // 第一跳：香港自建中转。排障时如策略组不兼容，可改成具体 HY2/VLESS 节点名。
  const DIALER_NAME = "香港自建";

  // 家宽节点名称匹配规则：只处理名字包含“自建家宽”的节点。
  const RESIDENTIAL_KEYWORD = /自建家宽/i;

  // 后缀配置：
  // - ""：直接给原始家宽节点注入 dialer-proxy，不生成新节点；
  // - "-via-HK"：复制一份链式节点，保留原始直连节点。
  const SUFFIX = "";

  if (!config || !Array.isArray(config.proxies)) {
    return config;
  }

  // 记录已有节点名，避免 SUFFIX 非空时重复生成。
  const existingNames = new Set(
    config.proxies
      .filter((proxy) => proxy && typeof proxy.name === "string")
      .map((proxy) => proxy.name),
  );

  const derivedProxies = [];

  for (const proxy of config.proxies) {
    if (!proxy || typeof proxy.name !== "string") continue;
    if (!RESIDENTIAL_KEYWORD.test(proxy.name)) continue;

    if (SUFFIX === "") {
      // 不保留原始直连家宽节点：直接把原节点改成链式节点。
      proxy["dialer-proxy"] = DIALER_NAME;
      // HTTP/SOCKS 家宽通常只适合 TCP CONNECT，不适合 UDP/QUIC。
      proxy["udp"] = false;
      continue;
    }

    // 保留原始节点：复制出 “原名 + SUFFIX” 的链式节点。
    const derivedName = `${proxy.name}${SUFFIX}`;
    if (existingNames.has(derivedName)) continue;

    const clonedProxy = JSON.parse(JSON.stringify(proxy));
    clonedProxy.name = derivedName;
    clonedProxy["dialer-proxy"] = DIALER_NAME;
    clonedProxy["udp"] = false;

    derivedProxies.push(clonedProxy);
    existingNames.add(derivedName);
  }

  if (derivedProxies.length > 0) {
    config.proxies.push(...derivedProxies);
  }

  return config;
}
