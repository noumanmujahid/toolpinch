// Cloudflare Pages Function: GET /api/seo-fetch?url=https://example.com
// -> { status, finalUrl, contentType, body } (max 1 MB, public http/https only)
const json = (body, status = 200) => new Response(JSON.stringify(body), {
  status, headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store' },
});

function privateIp(ip) {
  if (/^\d+\.\d+\.\d+\.\d+$/.test(ip)) {
    const p = ip.split('.').map(Number);
    return p[0] === 10 || p[0] === 127 || p[0] === 0 || (p[0] === 169 && p[1] === 254) ||
      (p[0] === 172 && p[1] >= 16 && p[1] <= 31) || (p[0] === 192 && p[1] === 168) || (p[0] === 100 && p[1] >= 64 && p[1] <= 127);
  }
  const v = ip.toLowerCase();
  return v === '::1' || v === '::' || v.startsWith('fc') || v.startsWith('fd') || v.startsWith('fe80:') || v.startsWith('::ffff:');
}

async function resolve(host) {
  const out = [];
  for (const type of ['A', 'AAAA']) {
    const r = await fetch(`https://cloudflare-dns.com/dns-query?type=${type}&name=${encodeURIComponent(host)}`, {
      headers: { accept: 'application/dns-json' }, signal: AbortSignal.timeout(5000),
    });
    const d = await r.json();
    for (const a of d.Answer || []) if (a.type === 1 || a.type === 28) out.push(a.data);
  }
  return out;
}

async function safeUrl(raw) {
  const url = new URL(raw);
  if (!['http:', 'https:'].includes(url.protocol) || url.username || url.password || (url.port && !['80', '443'].includes(url.port)))
    throw Error('Only public HTTP or HTTPS URLs on standard ports are allowed.');
  const host = url.hostname.replace(/^\[|\]$/g, '');
  const ips = /^[\d.]+$/.test(host) || host.includes(':') ? [host] : await resolve(host);
  if (!ips.length || ips.some(privateIp) || host === 'localhost' || host.endsWith('.local'))
    throw Error('Private or local network addresses are blocked.');
  return url;
}

export async function onRequestGet({ request }) {
  try {
    let url = await safeUrl(new URL(request.url).searchParams.get('url') || '');
    let response;
    for (let i = 0; i < 5; i++) {
      response = await fetch(url.href, {
        redirect: 'manual', signal: AbortSignal.timeout(8000),
        headers: { 'user-agent': 'ToolPinch-SEO-Checker/1.0', accept: 'text/html,application/xhtml+xml,text/plain,application/xml' },
      });
      const loc = response.headers.get('location');
      if (response.status >= 300 && response.status < 400 && loc) { url = await safeUrl(new URL(loc, url).href); continue; }
      break;
    }
    const type = response.headers.get('content-type') || '';
    if (!/(text\/html|application\/xhtml\+xml|text\/plain|application\/xml|text\/xml)/i.test(type))
      throw Error('The URL did not return HTML, XML or text.');
    const reader = response.body.getReader();
    const chunks = []; let size = 0;
    while (true) {
      const part = await reader.read();
      if (part.done) break;
      size += part.value.length;
      if (size > 1048576) { reader.cancel(); throw Error('Response is larger than 1 MB.'); }
      chunks.push(part.value);
    }
    const all = new Uint8Array(size); let off = 0;
    for (const c of chunks) { all.set(c, off); off += c.length; }
    const body = new TextDecoder('utf-8').decode(all);
    return json({ status: response.status, finalUrl: url.href, contentType: type, body });
  } catch (error) {
    return json({ error: error.message || 'Unable to fetch URL.' }, 400);
  }
}
