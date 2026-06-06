function main(config) {
  var DIALER = "美国-三网精品-vless-reality";
  var KEYWORDS = ["自建家宽", "TR-NAT", "土耳其", "Turkey", "turkey"];

  if (!config || !Array.isArray(config.proxies)) {
    return config;
  }

  for (var i = 0; i < config.proxies.length; i++) {
    var proxy = config.proxies[i];

    if (!proxy || !proxy.name) {
      continue;
    }

    var name = String(proxy.name);

    if (name === DIALER) {
      continue;
    }

    var matched = false;
    for (var j = 0; j < KEYWORDS.length; j++) {
      if (name.indexOf(KEYWORDS[j]) !== -1) {
        matched = true;
        break;
      }
    }

    if (!matched) {
      continue;
    }

    proxy["dialer-proxy"] = DIALER;
  }

  return config;
}
