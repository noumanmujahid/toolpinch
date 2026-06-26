const TASKS = {
  'meta-description': {
    label: 'AI Meta Description Generator',
    instruction: 'Write 5 unique meta description options. Each option must be 120 to 160 characters when possible, natural, accurate, and not clickbait. Include character counts.'
  },
  'blog-title': {
    label: 'AI Blog Title Generator',
    instruction: 'Write 12 blog title ideas. Mix how-to, checklist, beginner guide, mistakes, examples, and comparison angles. Keep titles honest and specific.'
  },
  rewrite: {
    label: 'AI Text Rewriter',
    instruction: 'Rewrite the text for clarity and flow while preserving meaning. Do not claim originality, bypass detection, or hide copied work. Return one polished version and three short improvement notes.'
  },
  email: {
    label: 'AI Email Writer',
    instruction: 'Write a concise email draft with a subject line, greeting, body, and closing. Use placeholders for private details instead of inventing them.'
  },
  caption: {
    label: 'AI Social Caption Generator',
    instruction: 'Write 8 social caption options. Keep them natural, useful, and not misleading. Include a few light hashtag ideas only if relevant.'
  },
  'product-description': {
    label: 'AI Product Description Generator',
    instruction: 'Write 4 ecommerce product description drafts plus 6 bullet benefits. Do not invent certifications, discounts, reviews, guarantees, medical claims, financial claims, or details not provided by the user.'
  },
  'youtube-title': {
    label: 'AI YouTube Title Generator',
    instruction: 'Write 12 YouTube title ideas and 3 short video description drafts. Keep titles accurate, not clickbait, and matched to the video topic.'
  },
  paragraph: {
    label: 'AI Paragraph Generator',
    instruction: 'Write 3 short paragraph drafts. Keep them clear, useful, natural, and easy to edit. Do not invent facts or statistics.'
  }
};

const RATE_LIMIT = new Map();
const WINDOW_MS = 60 * 1000;
const MAX_REQUESTS = 8;

function send(res, status, data) {
  res.statusCode = status;
  res.setHeader('Content-Type', 'application/json; charset=utf-8');
  res.setHeader('Cache-Control', 'no-store');
  res.end(JSON.stringify(data));
}

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') return send(res, 405, { error: 'Use POST.' });
  const apiKey = process.env.GEMINI_API_KEY;
  if (!apiKey) return send(res, 500, { error: 'AI service is not configured yet.' });

  const ip = String(req.headers['x-forwarded-for'] || req.socket?.remoteAddress || 'unknown').split(',')[0].trim();
  const now = Date.now();
  const bucket = RATE_LIMIT.get(ip) || { count: 0, reset: now + WINDOW_MS };
  if (now > bucket.reset) {
    bucket.count = 0;
    bucket.reset = now + WINDOW_MS;
  }
  bucket.count += 1;
  RATE_LIMIT.set(ip, bucket);
  if (bucket.count > MAX_REQUESTS) {
    return send(res, 429, { error: 'Too many AI requests. Please wait a minute and try again.' });
  }

  let body = {};
  try {
    body = typeof req.body === 'string' ? JSON.parse(req.body || '{}') : (req.body || {});
  } catch (error) {
    return send(res, 400, { error: 'Invalid request body.' });
  }

  const task = TASKS[String(body.task || '')];
  const input = String(body.input || '').trim();
  const tone = String(body.tone || 'clear').slice(0, 30);

  if (!task) return send(res, 400, { error: 'Unsupported AI tool.' });
  if (input.length < 5) return send(res, 400, { error: 'Please enter a little more detail.' });
  if (input.length > 2500) return send(res, 400, { error: 'Please keep input under 2500 characters.' });

  const model = process.env.GEMINI_MODEL || 'gemini-2.5-flash';
  const prompt = [
    'You are ToolPinch, a practical writing assistant for public web tools.',
    'Follow the task exactly. Keep output concise, original, safe, and useful.',
    'Do not produce academic cheating, plagiarism bypassing, AI detector bypassing, deception, fake reviews, illegal content, medical/legal/financial advice, or unsupported earning claims.',
    'Do not invent facts, statistics, prices, live data, quotes, sources, or private details.',
    'Return plain text only. No markdown tables.',
    '',
    'Tool: ' + task.label,
    'Tone: ' + tone,
    'Instruction: ' + task.instruction,
    'User input: ' + input
  ].join('\n');

  try {
    const url = 'https://generativelanguage.googleapis.com/v1beta/models/' + encodeURIComponent(model) + ':generateContent';
    const gemini = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-goog-api-key': apiKey
      },
      body: JSON.stringify({
        contents: [{ parts: [{ text: prompt }] }],
        generationConfig: {
          temperature: 0.7,
          topP: 0.9,
          maxOutputTokens: 900
        }
      })
    });

    const data = await gemini.json().catch(() => ({}));
    if (!gemini.ok) {
      const message = data?.error?.message || 'AI service error. Please try again later.';
      return send(res, gemini.status, { error: message });
    }

    const text = data?.candidates?.[0]?.content?.parts?.map(part => part.text || '').join('\n').trim();
    if (!text) return send(res, 502, { error: 'AI service returned an empty result.' });
    return send(res, 200, { text });
  } catch (error) {
    return send(res, 500, { error: 'AI request failed. Please try again later.' });
  }
};