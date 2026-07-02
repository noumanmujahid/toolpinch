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
const SITE_LIMIT = {
  minute: { count: 0, reset: 0 },
  day: { count: 0, key: '' }
};
const WINDOW_MS = 60 * 1000;
const MAX_REQUESTS_PER_IP = 2;
const MAX_SITE_REQUESTS_PER_MINUTE = parseInt(process.env.AI_MAX_REQUESTS_PER_MINUTE || '4', 10);
const MAX_SITE_REQUESTS_PER_DAY = parseInt(process.env.AI_MAX_REQUESTS_PER_DAY || '18', 10);

function currentUtcDay() {
  return new Date().toISOString().slice(0, 10);
}

function checkSiteLimits(now) {
  if (now > SITE_LIMIT.minute.reset) {
    SITE_LIMIT.minute.count = 0;
    SITE_LIMIT.minute.reset = now + WINDOW_MS;
  }

  const dayKey = currentUtcDay();
  if (SITE_LIMIT.day.key !== dayKey) {
    SITE_LIMIT.day.key = dayKey;
    SITE_LIMIT.day.count = 0;
  }

  if (SITE_LIMIT.minute.count >= MAX_SITE_REQUESTS_PER_MINUTE) {
    return 'AI is busy right now. Please wait a minute and try again.';
  }
  if (SITE_LIMIT.day.count >= MAX_SITE_REQUESTS_PER_DAY) {
    return 'Daily free AI limit reached. Please try again tomorrow.';
  }

  SITE_LIMIT.minute.count += 1;
  SITE_LIMIT.day.count += 1;
  return '';
}

function send(res, status, data) {
  res.statusCode = status;
  res.setHeader('Content-Type', 'application/json; charset=utf-8');
  res.setHeader('Cache-Control', 'no-store');
  res.end(JSON.stringify(data));
}

function buildPrompt(task, input, tone) {
  return [
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
}

async function callGroq(prompt) {
  const apiKey = process.env.GROQ_API_KEY;
  if (!apiKey) return { ok: false, status: 0, error: 'Groq is not configured.' };

  const model = process.env.GROQ_MODEL || 'llama-3.1-8b-instant';
  const response = await fetch('https://api.groq.com/openai/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Authorization': 'Bearer ' + apiKey,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      model,
      messages: [
        { role: 'system', content: 'Return plain text only. Follow safety instructions exactly.' },
        { role: 'user', content: prompt }
      ],
      temperature: 0.7,
      top_p: 0.9,
      max_tokens: 900
    })
  });

  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    return {
      ok: false,
      status: response.status,
      error: response.status === 429 ? 'AI limit reached. Please try again later.' : (data?.error?.message || 'Groq service error.')
    };
  }

  const text = data?.choices?.[0]?.message?.content?.trim();
  if (!text) return { ok: false, status: 502, error: 'AI service returned an empty result.' };
  return { ok: true, text, provider: 'groq' };
}

async function callGemini(prompt) {
  const apiKey = process.env.GEMINI_API_KEY;
  if (!apiKey) return { ok: false, status: 0, error: 'Gemini is not configured.' };

  const model = process.env.GEMINI_MODEL || 'gemini-2.5-flash-lite';
  const url = 'https://generativelanguage.googleapis.com/v1beta/models/' + encodeURIComponent(model) + ':generateContent';
  const response = await fetch(url, {
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

  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    const rawMessage = data?.error?.message || '';
    return {
      ok: false,
      status: response.status,
      error: response.status === 429 ? 'AI limit reached. Please try again later.' : rawMessage || 'Gemini service error.'
    };
  }

  const text = data?.candidates?.[0]?.content?.parts?.map(part => part.text || '').join('\n').trim();
  if (!text) return { ok: false, status: 502, error: 'AI service returned an empty result.' };
  return { ok: true, text, provider: 'gemini' };
}

async function generateDraft(prompt) {
  const provider = String(process.env.AI_PROVIDER || 'groq').toLowerCase();
  const first = provider === 'gemini' ? callGemini : callGroq;
  const second = provider === 'gemini' ? callGroq : callGemini;

  const primary = await first(prompt);
  if (primary.ok) return primary;

  const shouldFallback = primary.status === 0 || primary.status === 429 || primary.status >= 500;
  if (shouldFallback) {
    const fallback = await second(prompt);
    if (fallback.ok) return fallback;
  }

  return primary;
}

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') return send(res, 405, { error: 'Use POST.' });
  if (!process.env.GROQ_API_KEY && !process.env.GEMINI_API_KEY) {
    return send(res, 500, { error: 'AI service is not configured yet.' });
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

  const ip = String(req.headers['x-forwarded-for'] || req.socket?.remoteAddress || 'unknown').split(',')[0].trim();
  const now = Date.now();
  const bucket = RATE_LIMIT.get(ip) || { count: 0, reset: now + WINDOW_MS };
  if (now > bucket.reset) {
    bucket.count = 0;
    bucket.reset = now + WINDOW_MS;
  }
  bucket.count += 1;
  RATE_LIMIT.set(ip, bucket);
  if (bucket.count > MAX_REQUESTS_PER_IP) {
    return send(res, 429, { error: 'Please wait a minute before generating another AI draft.' });
  }

  const siteLimitError = checkSiteLimits(now);
  if (siteLimitError) return send(res, 429, { error: siteLimitError });

  const prompt = buildPrompt(task, input, tone);
  try {
    const result = await generateDraft(prompt);
    if (!result.ok) return send(res, result.status || 500, { error: result.error || 'AI request failed. Please try again later.' });
    return send(res, 200, { text: result.text, provider: result.provider });
  } catch (error) {
    return send(res, 500, { error: 'AI request failed. Please try again later.' });
  }
};
