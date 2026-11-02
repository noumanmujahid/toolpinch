// Cloudflare Pages Function: GET /api/dns-txt?domain=example.com -> { domain, records: [] }
const json = (body, status = 200) => new Response(JSON.stringify(body), {
  status, headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store' },
});

export async function onRequestGet({ request }) {
  try {
    const domain = String(new URL(request.url).searchParams.get('domain') || '').toLowerCase().replace(/\.$/, '');
    if (!/^(?=.{1,253}$)(?!-)(?:[a-z0-9-]{1,63}\.)+[a-z]{2,63}$/.test(domain)) throw Error('Enter a valid public domain.');
    const r = await fetch('https://cloudflare-dns.com/dns-query?type=TXT&name=' + encodeURIComponent(domain), {
      headers: { accept: 'application/dns-json' }, signal: AbortSignal.timeout(8000),
    });
    const data = await r.json();
    const records = (data.Answer || []).filter(a => a.type === 16)
      .map(a => [...String(a.data).matchAll(/"((?:[^"\\]|\\.)*)"/g)].map(m => m[1].replace(/\\(.)/g, '$1')).join('') || String(a.data));
    if (!records.length) throw Error('No TXT records were found.');
    return json({ domain, records });
  } catch (error) {
    return json({ error: error.message || 'Unable to look up TXT records.' }, 400);
  }
}
