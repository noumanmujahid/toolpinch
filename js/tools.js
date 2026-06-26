function bmiCalc(){const w=parseFloat(document.getElementById('weight').value);const h=parseFloat(document.getElementById('height').value)/100;const r=document.getElementById('result');if(!w||!h||w<=0||h<=0){r.innerHTML='Please enter a valid weight and height.';return}const bmi=w/(h*h);let s=bmi<18.5?'Underweight':bmi<25?'Healthy weight':bmi<30?'Overweight':'Obesity range';r.innerHTML=`Your BMI is ${bmi.toFixed(1)} <small>${s}. BMI is a screening number, not a medical diagnosis.</small>`}
function wordCount(){const raw=document.getElementById('textInput').value;const t=raw.trim();const words=t?t.split(/\s+/).length:0;const chars=raw.length;const charsNoSpaces=raw.replace(/\s/g,'').length;const sentences=(t.match(/[^.!?]+[.!?]+/g)||[]).length;document.getElementById('result').innerHTML=`${words} words <small>${chars} characters · ${charsNoSpaces} without spaces · ${sentences} sentences</small>`}
function ageCalc(){const d=new Date(document.getElementById('dob').value);const r=document.getElementById('result');if(isNaN(d)){r.innerHTML='Please select your date of birth.';return}const now=new Date();if(d>now){r.innerHTML='Date of birth cannot be in the future.';return}let age=now.getFullYear()-d.getFullYear();const m=now.getMonth()-d.getMonth();if(m<0||(m===0&&now.getDate()<d.getDate()))age--;const nextBirthday=new Date(now.getFullYear(),d.getMonth(),d.getDate());if(nextBirthday<now)nextBirthday.setFullYear(now.getFullYear()+1);const days=Math.ceil((nextBirthday-now)/86400000);r.innerHTML=`You are ${age} years old <small>${days} day${days===1?'':'s'} until your next birthday.</small>`}
function percentCalc(){const p=parseFloat(document.getElementById('percent').value);const n=parseFloat(document.getElementById('number').value);const r=document.getElementById('result');if(isNaN(p)||isNaN(n)){r.innerHTML='Please enter both values.';return}r.innerHTML=`${p}% of ${n} = ${(p/100*n).toFixed(2)} <small>Formula: (${p} / 100) x ${n}</small>`}
function discountCalc(){const price=parseFloat(document.getElementById('price').value);const disc=parseFloat(document.getElementById('discount').value);const r=document.getElementById('result');if(isNaN(price)||isNaN(disc)||price<0||disc<0){r.innerHTML='Please enter a valid price and discount.';return}const save=price*disc/100;const final=price-save;r.innerHTML=`Final price: ${final.toFixed(2)} <small>You save ${save.toFixed(2)} at ${disc}% off.</small>`}
function passwordGen(){const input=document.getElementById('length');const len=Math.min(128,Math.max(6,parseInt(input.value)||12));input.value=len;const chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=[]{};:,.?';const values=new Uint32Array(len);crypto.getRandomValues(values);let pass='';for(let i=0;i<len;i++)pass+=chars[values[i]%chars.length];document.getElementById('passOut').value=pass;document.getElementById('result').innerHTML=`Password generated successfully. <small>${len} characters with letters, numbers and symbols.</small>`}
function caseConvert(type){const el=document.getElementById('textInput');let t=el.value;if(type==='upper')t=t.toUpperCase();if(type==='lower')t=t.toLowerCase();if(type==='title')t=t.toLowerCase().replace(/\b\w/g,c=>c.toUpperCase());if(type==='sentence')t=t.toLowerCase().replace(/(^\s*\w|[.!?]\s*\w)/g,c=>c.toUpperCase());el.value=t;document.getElementById('result')&&(document.getElementById('result').innerHTML='Text converted successfully.')}
function keywordDensity(){const keyword=(document.getElementById('keyword').value||'').trim().toLowerCase();const text=(document.getElementById('textInput').value||'').trim().toLowerCase();const r=document.getElementById('result');if(!keyword||!text){r.innerHTML='Please enter a keyword and content.';return}const words=text.split(/\s+/).filter(Boolean).length;const escaped=keyword.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');const count=(text.match(new RegExp(`\\b${escaped}\\b`,'g'))||[]).length;const density=words?count/words*100:0;r.innerHTML=`${count} match${count===1?'':'es'} <small>${density.toFixed(2)}% density across ${words} words.</small>`}
function metaTagGenerator(){const title=(document.getElementById('pageTitle').value||'').trim();const desc=(document.getElementById('pageDesc').value||'').trim();const url=(document.getElementById('pageUrl').value||'').trim();const r=document.getElementById('result');if(!title||!desc){r.innerHTML='Please enter at least a title and description.';return}const safe=s=>s.replace(/&/g,'&amp;').replace(/"/g,'&quot;').replace(/</g,'&lt;');let out=`&lt;title&gt;${safe(title)}&lt;/title&gt;\n&lt;meta name="description" content="${safe(desc)}"&gt;`;if(url)out+=`\n&lt;link rel="canonical" href="${safe(url)}"&gt;\n&lt;meta property="og:title" content="${safe(title)}"&gt;\n&lt;meta property="og:description" content="${safe(desc)}"&gt;\n&lt;meta property="og:url" content="${safe(url)}"&gt;`;r.innerHTML=`<pre>${out}</pre>`}
function readingTime(){const wpm=Math.max(50,parseInt(document.getElementById('wpm').value)||200);const text=(document.getElementById('textInput').value||'').trim();const words=text?text.split(/\s+/).length:0;const minutes=Math.max(1,Math.ceil(words/wpm));document.getElementById('result').innerHTML=`${minutes} min read <small>${words} words at ${wpm} words per minute.</small>`}
function slugGenerator(){const text=(document.getElementById('slugText').value||'').trim();const slug=text.toLowerCase().normalize('NFKD').replace(/[\u0300-\u036f]/g,'').replace(/[^a-z0-9]+/g,'-').replace(/^-+|-+$/g,'');document.getElementById('result').innerHTML=slug||'Please enter text.'}
function robotsGenerator(){const site=(document.getElementById('siteUrl').value||'').trim().replace(/\/+$/,'');const dis=(document.getElementById('disallowPath').value||'').trim();const sitemap=site?`${site}/sitemap.xml`:'https://example.com/sitemap.xml';const out=`User-agent: *\nAllow: /\n${dis?`Disallow: ${dis}\n`:''}\nSitemap: ${sitemap}`;document.getElementById('result').innerHTML=`<pre>${tpEscape(out)}</pre>`}
function sitemapGenerator(){const lines=(document.getElementById('urlList').value||'').split(/\n+/).map(x=>x.trim()).filter(Boolean);const r=document.getElementById('result');if(!lines.length){r.innerHTML='Please enter at least one URL.';return}const esc=s=>s.replace(/&/g,'&amp;').replace(/</g,'&lt;');const xml=`<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${lines.map(u=>`  <url><loc>${esc(u)}</loc></url>`).join('\n')}\n</urlset>`;r.innerHTML=`<pre>${xml.replace(/</g,'&lt;').replace(/>/g,'&gt;')}</pre>`}
function htmlMinifier(){const input=document.getElementById('textInput').value||'';const out=input.replace(/>\s+</g,'><').replace(/\s{2,}/g,' ').trim();document.getElementById('result').innerHTML=`<pre>${tpEscape(out)}</pre><small>Minified from ${input.length} to ${out.length} characters.</small>`}
function urlCodec(mode){const el=document.getElementById('textInput');try{el.value=mode==='encode'?encodeURIComponent(el.value):decodeURIComponent(el.value);document.getElementById('result').innerHTML=`URL ${mode}d successfully.`}catch(e){document.getElementById('result').innerHTML='This text could not be decoded. Check the encoded format.'}}
function pdfPageCounter(){const file=document.getElementById('pdfFile').files[0];const r=document.getElementById('result');if(!file){r.innerHTML='Please select a PDF file.';return}const reader=new FileReader();reader.onload=()=>{const text=new TextDecoder('latin1').decode(new Uint8Array(reader.result));const count=(text.match(/\/Type\s*\/Page\b/g)||[]).length;r.innerHTML=`Estimated pages: ${count||'Unknown'} <small>${file.name} · ${(file.size/1024/1024).toFixed(2)} MB. Encrypted or unusual PDFs may not count perfectly.</small>`};reader.readAsArrayBuffer(file)}
function imageSizeChecker(){const file=document.getElementById('imageFile').files[0];const r=document.getElementById('result');if(!file){r.innerHTML='Please select an image file.';return}const img=new Image();img.onload=()=>{r.innerHTML=`${img.width} x ${img.height} pixels <small>${file.type||'Image'} · ${(file.size/1024).toFixed(1)} KB</small>`;URL.revokeObjectURL(img.src)};img.src=URL.createObjectURL(file)}
function fileSizeConverter(){const value=parseFloat(document.getElementById('fileSize').value);const unit=document.getElementById('fileUnit').value;const r=document.getElementById('result');if(isNaN(value)){r.innerHTML='Please enter a file size.';return}const powers={Bytes:0,KB:1,MB:2,GB:3};const bytes=value*Math.pow(1024,powers[unit]);r.innerHTML=`${bytes.toFixed(0)} Bytes <small>${(bytes/1024).toFixed(2)} KB · ${(bytes/1024/1024).toFixed(2)} MB · ${(bytes/1024/1024/1024).toFixed(4)} GB</small>`}
function loanCalculator(){const amount=parseFloat(document.getElementById('loanAmount').value);const rate=parseFloat(document.getElementById('loanRate').value);const years=parseFloat(document.getElementById('loanYears').value);const r=document.getElementById('result');if(isNaN(amount)||isNaN(rate)||isNaN(years)||amount<=0||years<=0){r.innerHTML='Please enter valid loan details.';return}const months=years*12;const monthly=rate/100/12;const payment=monthly?amount*monthly/(1-Math.pow(1+monthly,-months)):amount/months;const total=payment*months;r.innerHTML=`Estimated monthly payment: ${payment.toFixed(2)} <small>Total paid: ${total.toFixed(2)} · Interest: ${(total-amount).toFixed(2)}</small>`}
async function sha256Hash(){const text=document.getElementById('textInput').value||'';const r=document.getElementById('result');if(!text){r.innerHTML='Please enter text to hash.';return}const data=new TextEncoder().encode(text);const hash=await crypto.subtle.digest('SHA-256',data);const hex=[...new Uint8Array(hash)].map(b=>b.toString(16).padStart(2,'0')).join('');r.innerHTML=hex}
function characterCounter(){const t=document.getElementById('textInput').value||'';document.getElementById('result').innerHTML=`${t.length} characters <small>${(t.match(/\S/g)||[]).length} without spaces · ${t.split(/\n/).length} lines · ${t.trim()?t.trim().split(/\n\s*\n/).length:0} paragraphs</small>`}
function metaLength(){const d=document.getElementById('pageDesc').value||'';const n=d.length;document.getElementById('result').innerHTML=`${n} characters <small>${n<120?'Could be too short':n>160?'May be too long':'Good common range'} for many search snippets.</small>`}
function serpPreview(){const title=document.getElementById('pageTitle').value||'Example Page Title';const url=document.getElementById('pageUrl').value||'https://example.com/page';const desc=document.getElementById('pageDesc').value||'Your page description preview will appear here.';document.getElementById('result').innerHTML=`<div style="font-weight:400"><div style="color:#1a0dab;font-size:18px">${tpEscape(title)}</div><div style="color:#006621">${tpEscape(url)}</div><div>${tpEscape(desc)}</div></div>`}
function readability(){const t=(document.getElementById('textInput').value||'').trim();const words=t?t.split(/\s+/):[];const sentences=Math.max(1,(t.match(/[.!?]+/g)||[]).length);const syllables=words.join(' ').toLowerCase().split(/\s+/).reduce((a,w)=>a+Math.max(1,(w.match(/[aeiouy]+/g)||[]).length),0);const score=206.835-1.015*(words.length/sentences)-84.6*(syllables/Math.max(1,words.length));document.getElementById('result').innerHTML=`Readability score: ${score.toFixed(1)} <small>${words.length} words · ${sentences} sentences. Higher is usually easier to read.</small>`}
function textCleaner(){const el=document.getElementById('textInput');el.value=(el.value||'').replace(/[ \t]+/g,' ').replace(/\n{3,}/g,'\n\n').trim();document.getElementById('result').innerHTML='Text cleaned successfully.'}
function textDiff(){const a=(document.getElementById('textA').value||'').split('\n');const b=(document.getElementById('textB').value||'').split('\n');const max=Math.max(a.length,b.length);let out=[];for(let i=0;i<max;i++){if(a[i]!==b[i])out.push(`Line ${i+1}: ${a[i]||''} → ${b[i]||''}`)}document.getElementById('result').innerHTML=`<pre>${tpEscape(out.join('\n')||'No line differences found.')}</pre>`}
function duplicateText(){const lines=(document.getElementById('textInput').value||'').split(/\n+/).map(x=>x.trim()).filter(Boolean);const seen=new Map();lines.forEach(l=>seen.set(l,(seen.get(l)||0)+1));const dup=[...seen.entries()].filter(([,c])=>c>1);document.getElementById('result').innerHTML=dup.length?`<pre>${tpEscape(dup.map(([l,c])=>`${c}x ${l}`).join('\n'))}</pre>`:'No duplicate lines found.'}
function blogTitle(){const t=(document.getElementById('topic').value||'your topic').trim();const ideas=[`How to ${t}: A Simple Guide`,`Best ${t} Tips for Beginners`,`${t}: Common Mistakes to Avoid`,`A Practical Checklist for ${t}`,`Why ${t} Matters and How to Start`];document.getElementById('result').innerHTML=`<pre>${tpEscape(ideas.join('\n'))}</pre>`}
function articleOutline(){const t=(document.getElementById('topic').value||'Topic').trim();const a=(document.getElementById('audience').value||'readers').trim();document.getElementById('result').innerHTML=`<pre>${tpEscape(`H1: ${t}\nIntro: Why ${a} care about ${t}\nH2: Key basics\nH2: Step-by-step process\nH2: Examples\nH2: Common mistakes\nH2: FAQs\nConclusion: Next steps`)}</pre>`}
function pdfCompressGuide(){const f=document.getElementById('pdfFile').files[0];if(!f){result.innerHTML='Please select a PDF.';return}document.getElementById('result').innerHTML=`${f.name} is ${(f.size/1024/1024).toFixed(2)} MB <small>To reduce size, compress images before creating the PDF, remove unused pages, or export with lower image quality.</small>`}
function pdfMetadata(){const f=document.getElementById('pdfFile').files[0];if(!f){document.getElementById('result').innerHTML='Please select a PDF.';return}document.getElementById('result').innerHTML=`${f.name} <small>${f.type||'application/pdf'} · ${(f.size/1024/1024).toFixed(2)} MB · Last modified ${new Date(f.lastModified).toLocaleDateString()}</small>`}
function drawImageToCanvas(file,cb){const img=new Image();img.onload=()=>cb(img);img.src=URL.createObjectURL(file)}
function canvasDownload(canvas,name,type='image/png',quality=.85){canvas.toBlob(b=>{const a=document.createElement('a');a.href=URL.createObjectURL(b);a.download=name;a.click();document.getElementById('result').innerHTML=`Created ${name} <small>${(b.size/1024).toFixed(1)} KB</small>`},type,quality)}
function imageCompressor(){const f=document.getElementById('imageFile').files[0];if(!f)return result.innerHTML='Please select an image.';drawImageToCanvas(f,img=>{const c=document.createElement('canvas');c.width=img.width;c.height=img.height;c.getContext('2d').drawImage(img,0,0);canvasDownload(c,'compressed.jpg','image/jpeg',parseFloat(document.getElementById('quality').value)||.7)})}
function imageResizer(){const f=document.getElementById('imageFile').files[0];if(!f)return result.innerHTML='Please select an image.';drawImageToCanvas(f,img=>{const w=parseInt(document.getElementById('imgWidth').value)||img.width;const h=parseInt(document.getElementById('imgHeight').value)||img.height;const c=document.createElement('canvas');c.width=w;c.height=h;c.getContext('2d').drawImage(img,0,0,w,h);canvasDownload(c,'resized.png')})}
function imageCropper(){const f=document.getElementById('imageFile').files[0];if(!f)return result.innerHTML='Please select an image.';drawImageToCanvas(f,img=>{const size=parseInt(document.getElementById('cropSize').value)||512;const side=Math.min(img.width,img.height);const c=document.createElement('canvas');c.width=size;c.height=size;c.getContext('2d').drawImage(img,(img.width-side)/2,(img.height-side)/2,side,side,0,0,size,size);canvasDownload(c,'cropped.png')})}
function imageConvert(){const f=document.getElementById('imageFile').files[0];if(!f)return result.innerHTML='Please select an image.';const slug=location.pathname;const type=slug.includes('webp')?'image/webp':slug.includes('png-to-jpg')?'image/jpeg':'image/png';const ext=type==='image/jpeg'?'jpg':type==='image/webp'?'webp':'png';drawImageToCanvas(f,img=>{const c=document.createElement('canvas');c.width=img.width;c.height=img.height;c.getContext('2d').drawImage(img,0,0);canvasDownload(c,`converted.${ext}`,type,.9)})}
function imageToPdf(){const f=document.getElementById('imageFile').files[0];if(!f)return result.innerHTML='Please select an image.';const url=URL.createObjectURL(f);const w=window.open('','_blank');w.document.write(`<!doctype html><title>Save image as PDF</title><style>body{margin:0;display:grid;place-items:center;min-height:100vh}img{max-width:95vw;max-height:95vh}@media print{button{display:none}}</style><button onclick="print()" style="position:fixed;top:12px;right:12px">Print / Save as PDF</button><img src="${url}" alt="Image">`);document.getElementById('result').innerHTML='Opened a print-ready page. Use Print / Save as PDF in your browser.'}
function imageToBase64(){const f=document.getElementById('imageFile').files[0];if(!f)return result.innerHTML='Please select an image.';const r=new FileReader();r.onload=()=>document.getElementById('result').innerHTML=`<pre>${tpEscape(String(r.result).slice(0,5000))}</pre>`;r.readAsDataURL(f)}
function base64ToImage(){const v=document.getElementById('textInput').value.trim();const valid=/^data:image\/(?:png|jpeg|jpg|webp|gif);base64,[a-z0-9+/=\s]+$/i.test(v);document.getElementById('preview').replaceChildren();if(valid){const img=document.createElement('img');img.src=v;img.alt='Base64 image preview';img.style.cssText='max-width:100%;margin-top:14px';document.getElementById('preview').appendChild(img)}document.getElementById('result').innerHTML=valid?'Preview generated.':'Paste a valid PNG, JPG, WebP or GIF Base64 data URL.'}
function faviconGenerator(){const f=document.getElementById('imageFile').files[0];if(!f)return result.innerHTML='Please select an image.';drawImageToCanvas(f,img=>{const c=document.createElement('canvas');c.width=32;c.height=32;c.getContext('2d').drawImage(img,0,0,32,32);canvasDownload(c,'favicon.png')})}
function passportPhoto(){const f=document.getElementById('imageFile').files[0];if(!f)return result.innerHTML='Please select an image.';const format=document.getElementById('passportSize')?.value||'35x45';const [w,h]=format==='2x2'?[600,600]:[700,900];drawImageToCanvas(f,img=>{const target=w/h;const source=img.width/img.height;let sx=0,sy=0,sw=img.width,sh=img.height;if(source>target){sw=img.height*target;sx=(img.width-sw)/2}else{sh=img.width/target;sy=(img.height-sh)/2}const c=document.createElement('canvas');c.width=w;c.height=h;c.getContext('2d').drawImage(img,sx,sy,sw,sh,0,0,w,h);canvasDownload(c,`passport-photo-${format}.jpg`,'image/jpeg',.92)})}
function canvasBlob(canvas,type,quality){return new Promise(resolve=>canvas.toBlob(resolve,type,quality))}
async function imageTargetCompress(){const f=document.getElementById('imageFile').files[0];if(!f)return result.innerHTML='Please select an image.';const target=Math.max(10,Number(document.getElementById('targetKb')?.value)||100)*1024;drawImageToCanvas(f,async img=>{let width=img.width,height=img.height,quality=.9,blob=null,canvas=document.createElement('canvas');for(let attempt=0;attempt<18;attempt++){canvas.width=Math.max(1,Math.round(width));canvas.height=Math.max(1,Math.round(height));canvas.getContext('2d').drawImage(img,0,0,canvas.width,canvas.height);blob=await canvasBlob(canvas,'image/jpeg',quality);if(blob&&blob.size<=target)break;if(quality>.35)quality-=.08;else{width*=.85;height*=.85;quality=.72}}if(!blob)return result.innerHTML='The browser could not create the compressed image.';const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='compressed-target.jpg';a.click();result.innerHTML=`Created compressed-target.jpg <small>${(blob.size/1024).toFixed(1)} KB · ${canvas.width} × ${canvas.height}px. ${blob.size>target?'The image could not reach the target without further resizing.':'Target reached.'}</small>`})}
function schemaGenerator(){const type=document.getElementById('schemaType').value;const name=document.getElementById('pageTitle').value||'Name';const url=document.getElementById('pageUrl').value||location.origin;document.getElementById('result').innerHTML=`<pre>${tpEscape(JSON.stringify({'@context':'https://schema.org','@type':type,name,url},null,2))}</pre>`}
function faqSchema(){const lines=(document.getElementById('textInput').value||'').split('\n').filter(Boolean);const mainEntity=lines.map(l=>{const [q,a]=l.split('|');return {'@type':'Question',name:(q||'Question').trim(),acceptedAnswer:{'@type':'Answer',text:(a||'Answer').trim()}}});document.getElementById('result').innerHTML=`<pre>${tpEscape(JSON.stringify({'@context':'https://schema.org','@type':'FAQPage',mainEntity},null,2))}</pre><small>Google no longer displays FAQ rich results. Use this markup only for a platform or workflow that still consumes it.</small>`}
function ogGenerator(){metaTagGenerator()}
function twitterCard(){const title=document.getElementById('pageTitle').value||'';const desc=document.getElementById('pageDesc').value||'';document.getElementById('result').innerHTML=`<pre>&lt;meta name="twitter:card" content="summary_large_image"&gt;\n&lt;meta name="twitter:title" content="${tpEscape(title)}"&gt;\n&lt;meta name="twitter:description" content="${tpEscape(desc)}"&gt;</pre>`}
function utmBuilder(){try{const u=new URL(document.getElementById('baseUrl').value||location.origin);[['utm_source','utmSource'],['utm_medium','utmMedium'],['utm_campaign','utmCampaign']].forEach(([p,id])=>{const v=document.getElementById(id).value;if(v)u.searchParams.set(p,v)});document.getElementById('result').textContent=String(u)}catch(e){document.getElementById('result').textContent='Enter a valid absolute URL.'}}
function jsonFormatter(){try{document.getElementById('result').innerHTML=`<pre>${tpEscape(JSON.stringify(JSON.parse(document.getElementById('textInput').value),null,2))}</pre>`}catch(e){result.innerHTML='Invalid JSON.'}}
function jsonMinifier(){try{document.getElementById('result').innerHTML=`<pre>${tpEscape(JSON.stringify(JSON.parse(document.getElementById('textInput').value)))}</pre>`}catch(e){result.innerHTML='Invalid JSON.'}}
function jsonToCsv(){try{const arr=JSON.parse(document.getElementById('textInput').value);const keys=Object.keys(arr[0]||{});const csv=[keys.join(','),...arr.map(o=>keys.map(k=>JSON.stringify(o[k]??'')).join(','))].join('\n');result.innerHTML=`<pre>${tpEscape(csv)}</pre>`}catch(e){result.innerHTML='Enter a JSON array of objects.'}}
function csvToJson(){const rows=document.getElementById('textInput').value.trim().split('\n').map(r=>r.split(','));const keys=rows.shift()||[];result.innerHTML=`<pre>${tpEscape(JSON.stringify(rows.map(r=>Object.fromEntries(keys.map((k,i)=>[k,r[i]||'']))),null,2))}</pre>`}
function xmlFormatter(){const x=(document.getElementById('textInput').value||'').replace(/>\s*</g,'>\n<');result.innerHTML=`<pre>${x.replace(/</g,'&lt;')}</pre>`}
function cssMinifier(){const x=(document.getElementById('textInput').value||'').replace(/\/\*[\s\S]*?\*\//g,'').replace(/\s+/g,' ').replace(/\s*([{}:;,])\s*/g,'$1').trim();result.innerHTML=`<pre>${tpEscape(x)}</pre>`}
function jsMinifier(){const x=(document.getElementById('textInput').value||'').replace(/\/\/.*$/gm,'').replace(/\s+/g,' ').trim();result.innerHTML=`<pre>${tpEscape(x)}</pre>`}
function base64Codec(mode){const el=document.getElementById('textInput');try{el.value=mode==='encode'?btoa(unescape(encodeURIComponent(el.value))):decodeURIComponent(escape(atob(el.value)));result.innerHTML=`Base64 ${mode}d successfully.`}catch(e){result.innerHTML='Could not process this Base64 text.'}}
function uuidGenerator(){const n=Math.min(100,Math.max(1,parseInt(document.getElementById('count').value)||5));result.innerHTML=`<pre>${Array.from({length:n},()=>crypto.randomUUID()).join('\n')}</pre>`}
function profitMargin(){const cost=parseFloat(document.getElementById('cost').value);const price=parseFloat(document.getElementById('price').value);if(isNaN(cost)||isNaN(price))return result.innerHTML='Enter cost and price.';const profit=price-cost;result.innerHTML=`Profit: ${profit.toFixed(2)} <small>Margin: ${(profit/price*100).toFixed(2)}% · Markup: ${(profit/cost*100).toFixed(2)}%</small>`}
function vatCalculator(){const price=parseFloat(document.getElementById('price').value);const rate=parseFloat(document.getElementById('taxRate').value);if(isNaN(price)||isNaN(rate))return result.innerHTML='Enter price and tax rate.';const tax=price*rate/100;result.innerHTML=`Tax: ${tax.toFixed(2)} <small>Total with tax: ${(price+tax).toFixed(2)} · Price before tax from total: ${(price/(1+rate/100)).toFixed(2)}</small>`}
function dateDiff(){const a=new Date(document.getElementById('startDate').value);const b=new Date(document.getElementById('endDate').value);if(isNaN(a)||isNaN(b))return result.innerHTML='Select both dates.';const days=Math.round(Math.abs(b-a)/86400000);result.innerHTML=`${days} days <small>${(days/7).toFixed(1)} weeks</small>`}
function unitConverter(){const v=parseFloat(document.getElementById('unitValue').value);const t=document.getElementById('unitType').value;if(isNaN(v))return result.innerHTML='Enter a value.';const m={'kg-lb':v*2.20462,'lb-kg':v/2.20462,'cm-in':v/2.54,'in-cm':v*2.54,'c-f':v*9/5+32,'f-c':(v-32)*5/9};result.innerHTML=`${m[t].toFixed(4)}`}
function passwordStrength(){const p=document.getElementById('passwordInput').value||'';let s=0;if(p.length>=12)s++;if(/[a-z]/.test(p)&&/[A-Z]/.test(p))s++;if(/\d/.test(p))s++;if(/[^a-zA-Z0-9]/.test(p))s++;result.innerHTML=`Strength: ${['Very weak','Weak','Fair','Good','Strong'][s]} <small>Use long unique passwords and a password manager.</small>`}
function qrGenerator(){const text=encodeURIComponent(document.getElementById('textInput')?.value||prompt('Enter QR text or URL')||'');if(!text)return result.innerHTML='Enter text or URL.';result.innerHTML=`<img alt="QR code" style="max-width:220px;background:#fff;padding:10px" src="https://api.qrserver.com/v1/create-qr-code/?size=220x220&data=${text}"><small>QR image generated from the entered text.</small>`}
function tpEscape(s){return String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
function tpNormalize(s){return String(s||'').toLowerCase().replace(/[^a-z0-9\s]/g,' ').replace(/\s+/g,' ').trim()}
function tpSentences(text){return (String(text||'').replace(/\s+/g,' ').match(/[^.!?]+[.!?]?/g)||[]).map(s=>s.trim()).filter(s=>s.length>3)}
function textSimilarity(){const a=document.getElementById('textA').value||'';const b=document.getElementById('textB').value||'';const r=document.getElementById('result');if(!a.trim()||!b.trim()){r.innerHTML='Please enter both text blocks.';return}const wordsA=new Set(tpNormalize(a).split(' ').filter(Boolean));const wordsB=new Set(tpNormalize(b).split(' ').filter(Boolean));const shared=[...wordsA].filter(w=>wordsB.has(w));const union=new Set([...wordsA,...wordsB]);const score=union.size?shared.length/union.size*100:0;const sentA=tpSentences(a).map(s=>[s,tpNormalize(s)]).filter(([,n])=>n.length>20);const sentB=new Set(tpSentences(b).map(tpNormalize).filter(n=>n.length>20));const matches=sentA.filter(([,n])=>sentB.has(n)).map(([s])=>s);const sample=matches.slice(0,10).map(s=>`- ${s}`).join('\n');r.innerHTML=`Similarity estimate: ${score.toFixed(1)}% <small>${shared.length} shared unique words · ${matches.length} matching sentence${matches.length===1?'':'s'}. This compares only the text you paste.</small>${matches.length?`<pre>${tpEscape(sample)}</pre>`:''}`}
function duplicateSentences(){const text=document.getElementById('textInput').value||'';const r=document.getElementById('result');if(!text.trim()){r.innerHTML='Please paste content to check.';return}const seen=new Map();tpSentences(text).forEach(sentence=>{const n=tpNormalize(sentence);if(n.length<20)return;const current=seen.get(n)||{sentence,count:0};current.count++;seen.set(n,current)});const dup=[...seen.values()].filter(item=>item.count>1).sort((a,b)=>b.count-a.count);if(!dup.length){r.innerHTML='No repeated sentences found. <small>Short sentence fragments are ignored for cleaner results.</small>';return}r.innerHTML=`${dup.length} repeated sentence${dup.length===1?'':'s'} found <small>Review these before publishing.</small><pre>${tpEscape(dup.slice(0,25).map(item=>`${item.count}x ${item.sentence}`).join('\n'))}</pre>`}
function textHumanizer(){const el=document.getElementById('textInput');const tone=document.getElementById('tone')?.value||'natural';const r=document.getElementById('result');let text=(el.value||'').trim();if(!text){r.innerHTML='Please paste text to rewrite.';return}const phrases=[[/\bin conclusion,?\s*/gi,''],[/\bit is important to note that\b/gi,'notably'],[/\bin order to\b/gi,'to'],[/\bdue to the fact that\b/gi,'because'],[/\bat this point in time\b/gi,'now'],[/\butilize\b/gi,'use'],[/\bassist\b/gi,'help'],[/\bcommence\b/gi,'start'],[/\bterminate\b/gi,'end'],[/\bapproximately\b/gi,'about']];phrases.forEach(([a,b])=>text=text.replace(a,b));text=text.replace(/\s+/g,' ').replace(/\s+([,.!?;:])/g,'$1').replace(/([.!?])\s+/g,'$1\n\n').trim();let sentences=tpSentences(text).map(s=>s.charAt(0).toUpperCase()+s.slice(1));if(tone==='friendly')sentences=sentences.map(s=>s.replace(/\bWe recommend\b/g,'A good option is').replace(/\bYou should\b/g,'You can'));if(tone==='professional')sentences=sentences.map(s=>s.replace(/\bvery\b/gi,'highly').replace(/\ba lot of\b/gi,'many'));const out=sentences.join('\n\n');r.innerHTML=`<pre>${tpEscape(out)}</pre><small>Review the rewritten text for accuracy and tone before publishing.</small>`}
async function dictionaryLookup(){const word=(document.getElementById('wordInput').value||'').trim().toLowerCase();const r=document.getElementById('result');if(!word){r.innerHTML='Please enter a word.';return}r.innerHTML='Looking up word...';try{const res=await fetch(`https://api.dictionaryapi.dev/api/v2/entries/en/${encodeURIComponent(word)}`);if(!res.ok)throw new Error('not found');const data=await res.json();const entry=data[0]||{};const phonetic=entry.phonetic||entry.phonetics?.find(p=>p.text)?.text||'';const defs=(entry.meanings||[]).flatMap(m=>(m.definitions||[]).slice(0,3).map(d=>`${m.partOfSpeech||'word'}: ${d.definition}${d.example?` Example: ${d.example}`:''}`)).slice(0,8);r.innerHTML=`<strong>${tpEscape(entry.word||word)}</strong>${phonetic?` <small>${tpEscape(phonetic)}</small>`:''}<pre>${tpEscape(defs.join('\n\n')||'No definitions found.')}</pre>`}catch(e){r.innerHTML='No definition found. <small>Check spelling or try a simpler English word.</small>'}}
async function wordRelation(type){const word=(document.getElementById('wordInput').value||'').trim().toLowerCase();const r=document.getElementById('result');if(!word){r.innerHTML='Please enter a word.';return}const rel=type==='ant'?'rel_ant':'rel_syn';r.innerHTML='Finding words...';try{const res=await fetch(`https://api.datamuse.com/words?${rel}=${encodeURIComponent(word)}&max=30`);const data=await res.json();const words=data.map(x=>x.word).filter(Boolean);r.innerHTML=words.length?`<pre>${tpEscape(words.join('\n'))}</pre><small>Choose words that fit your sentence and meaning.</small>`:`No ${type==='ant'?'antonyms':'synonyms'} found for this word.`}catch(e){r.innerHTML='Could not load word suggestions. Please try again later.'}}
function synonymFinder(){wordRelation('syn')}
function antonymFinder(){wordRelation('ant')}
function seedValue(){return (document.getElementById('seedKeyword')?.value||'').trim()}
function cleanSeed(){return seedValue().toLowerCase().replace(/\s+/g,' ').trim()}
function outputList(items,note=''){result.innerHTML=`<pre>${tpEscape(items.join('\n'))}</pre>${note?`<small>${tpEscape(note)}</small>`:''}`}
function keywordResearch(){const seed=cleanSeed();if(!seed)return result.innerHTML='Please enter a seed keyword.';const items=[`${seed} tool`,`${seed} checker`,`${seed} generator`,`${seed} online`,`${seed} free`,`best ${seed} tool`,`how to ${seed}`,`${seed} examples`,`${seed} for beginners`,`${seed} guide`,`${seed} template`,`${seed} tips`,`free ${seed} online`,`simple ${seed} tool`,`${seed} vs alternatives`,`what is ${seed}`,`${seed} checklist`,`${seed} for website`,`${seed} for SEO`,`${seed} step by step`];outputList([...new Set(items)],'Idea generator only. It does not show live search volume or competition data.')}
function longTailKeywords(){const seed=cleanSeed();if(!seed)return result.innerHTML='Please enter a seed keyword.';const starts=['how to','best free','free online','simple','easy','quick','beginner','advanced','small business','for students','for bloggers','for website owners'];const ends=['tool','checker','generator','template','examples','guide','tips','checklist','without signup','online free'];outputList([...new Set([...starts.map(x=>`${x} ${seed}`),...ends.map(x=>`${seed} ${x}`)])],'Group similar phrases by intent before creating pages.')}
function keywordSuggestions(){const seed=cleanSeed();if(!seed)return result.innerHTML='Please enter a seed keyword.';const items=[`What is ${seed}?`,`How does ${seed} work?`,`How to use ${seed}?`,`Why is ${seed} important?`,`Best ${seed} tools`,`Free ${seed} tools`,`${seed} examples`,`${seed} checklist`,`${seed} vs ${seed} tool`,`${seed} for beginners`,`${seed} for small business`,`${seed} mistakes`,`${seed} tips`,`${seed} guide`,`${seed} alternatives`,`${seed} online`,`${seed} calculator`,`${seed} template`];outputList(items,'These are generated topic patterns, not live autocomplete data.')}
function seoTitleGenerator(){const seed=seedValue()||'Your Topic';const audience=(document.getElementById('audience')?.value||'beginners').trim()||'beginners';const items=[`${seed}: Simple Guide for ${audience}`,`Best ${seed} Tips for ${audience}`,`${seed} Tool - Free Online Helper`,`How to Use ${seed} Step by Step`,`Free ${seed} Generator for Quick Results`,`${seed} Checklist: What to Review Before Publishing`,`${seed} Examples and Practical Tips`,`What Is ${seed}? A Clear Beginner Guide`];outputList(items,'Edit the title so it accurately matches the final page.')}
function metaDescriptionGenerator(){const topic=(document.getElementById('seedKeyword')?.value||'your page').trim();const benefit=(document.getElementById('benefit')?.value||'get quick, useful results').trim();const items=[`Use this ${topic} tool to ${benefit}. Simple, fast and easy to use in your browser.`,`Try a free ${topic} helper to ${benefit}, review results and improve your page before publishing.`,`Learn about ${topic}, check useful details and ${benefit} with a clean online tool from ToolPinch.`,`Create better ${topic} results with a simple browser tool built for quick everyday work.`];outputList(items.map(x=>`${x} (${x.length} characters)`),'Check the final length and make sure the description matches visible page content.')}
function seoContentBrief(){const seed=seedValue()||'Main keyword';const audience=(document.getElementById('audience')?.value||'readers').trim()||'readers';const brief=[`Primary keyword: ${seed}`,`Audience: ${audience}`,'',`Suggested title: ${seed}: Practical Guide for ${audience}`,'',`H1: ${seed}`,'H2: What it means','H2: Why it matters','H2: How to use it step by step','H2: Common mistakes','H2: Examples','H2: FAQs','',`Related terms: ${seed} tool, ${seed} checker, ${seed} examples, ${seed} guide, free ${seed}`,'',`FAQs:`,`What is ${seed}?`,`How do I use ${seed}?`,`Is ${seed} free?`,`What should I check before publishing?`];outputList(brief,'Use this as a starting brief, then add real examples and original details.')}
function peopleAlsoAsk(){const seed=cleanSeed();if(!seed)return result.innerHTML='Please enter a keyword.';const qs=[`What is ${seed}?`,`How do I use ${seed}?`,`Why is ${seed} important?`,`What is the best ${seed} tool?`,`Can I use ${seed} for free?`,`How do beginners start with ${seed}?`,`What are common ${seed} mistakes?`,`How can I improve ${seed}?`,`What should I check before using ${seed}?`,`Is ${seed} useful for SEO?`];outputList(qs,'Generated question ideas only. Add only questions that genuinely fit the page.')}
function relatedKeywords(){const seed=cleanSeed();if(!seed)return result.innerHTML='Please enter a seed keyword.';const roots=seed.split(' ').filter(Boolean);const base=roots.length>1?roots[roots.length-1]:seed;const items=[`${seed} guide`,`${seed} tool`,`${seed} checker`,`${seed} generator`,`${seed} examples`,`${seed} template`,`${seed} tips`,`${base} research`,`${base} ideas`,`${base} questions`,`${base} content`,`${base} SEO`,`${base} writing`,`${base} planning`,`${seed} online`,`${seed} free`];outputList([...new Set(items)],'Use related ideas naturally. Do not stuff keywords into content.')}

function tpDateInZone(parts,zone){
  let stamp=Date.UTC(parts.year,parts.month-1,parts.day,parts.hour,parts.minute);
  const formatter=new Intl.DateTimeFormat('en-CA',{timeZone:zone,year:'numeric',month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit',hourCycle:'h23'});
  for(let i=0;i<3;i++){
    const current=Object.fromEntries(formatter.formatToParts(new Date(stamp)).filter(p=>p.type!=='literal').map(p=>[p.type,Number(p.value)]));
    const shown=Date.UTC(current.year,current.month-1,current.day,current.hour,current.minute);
    stamp+=Date.UTC(parts.year,parts.month-1,parts.day,parts.hour,parts.minute)-shown;
  }
  return new Date(stamp);
}
function worldCupTime(){
  const raw=document.getElementById('matchDateTime').value;
  const source=document.getElementById('sourceZone').value;
  const target=document.getElementById('targetZone').value;
  if(!raw)return result.innerHTML='Select a kickoff date and time.';
  const [date,time]=raw.split('T');
  const [year,month,day]=date.split('-').map(Number);
  const [hour,minute]=time.split(':').map(Number);
  const kickoff=tpDateInZone({year,month,day,hour,minute},source);
  const format=zone=>new Intl.DateTimeFormat('en-US',{timeZone:zone,weekday:'long',year:'numeric',month:'long',day:'numeric',hour:'numeric',minute:'2-digit',timeZoneName:'short'}).format(kickoff);
  result.innerHTML=`<strong>${tpEscape(format(target))}</strong><small>Converted from ${tpEscape(format(source))}. Confirm the original kickoff with the official schedule.</small>`;
}
function groupStandings(){
  const names=[0,1,2,3].map(i=>(document.getElementById(`team${i}`).value||`Team ${i+1}`).trim());
  const table=names.map((name,index)=>({name,index,p:0,w:0,d:0,l:0,gf:0,ga:0,gd:0,pts:0}));
  for(let i=0;i<6;i++){
    const a=document.getElementById(`m${i}a`).value;
    const b=document.getElementById(`m${i}b`).value;
    if(a===''||b==='')return result.innerHTML='Enter a score for all six group matches.';
    const [ai,bi]=document.getElementById(`m${i}teams`).value.split(',').map(Number);
    const ag=Number(a),bg=Number(b);
    if(ag<0||bg<0)return result.innerHTML='Scores cannot be negative.';
    const A=table[ai],B=table[bi];
    A.p++;B.p++;A.gf+=ag;A.ga+=bg;B.gf+=bg;B.ga+=ag;
    if(ag>bg){A.w++;A.pts+=3;B.l++}else if(bg>ag){B.w++;B.pts+=3;A.l++}else{A.d++;B.d++;A.pts++;B.pts++}
  }
  table.forEach(t=>t.gd=t.gf-t.ga);
  table.sort((a,b)=>b.pts-a.pts||b.gd-a.gd||b.gf-a.gf||a.index-b.index);
  const rows=table.map((t,i)=>`<tr><td>${i+1}</td><td>${tpEscape(t.name)}</td><td>${t.p}</td><td>${t.w}</td><td>${t.d}</td><td>${t.l}</td><td>${t.gf}</td><td>${t.ga}</td><td>${t.gd>0?'+':''}${t.gd}</td><td><strong>${t.pts}</strong></td></tr>`).join('');
  result.innerHTML=`<div class="table-scroll"><table class="sports-table"><thead><tr><th>#</th><th>Team</th><th>P</th><th>W</th><th>D</th><th>L</th><th>GF</th><th>GA</th><th>GD</th><th>Pts</th></tr></thead><tbody>${rows}</tbody></table></div><small>Sorted by points, goal difference and goals scored. Official rules may use additional tiebreakers.</small>`;
}
function thirdPlace(){
  const teams=[];
  for(let i=0;i<12;i++){
    const pts=document.getElementById(`thirdPts${i}`).value;
    const gd=document.getElementById(`thirdGd${i}`).value;
    const gf=document.getElementById(`thirdGf${i}`).value;
    if(pts===''||gd===''||gf==='')return result.innerHTML='Enter points, goal difference and goals scored for all 12 rows.';
    teams.push({order:i,name:(document.getElementById(`thirdName${i}`).value||`Group ${String.fromCharCode(65+i)} third`).trim(),pts:Number(pts),gd:Number(gd),gf:Number(gf)});
  }
  teams.sort((a,b)=>b.pts-a.pts||b.gd-a.gd||b.gf-a.gf||a.order-b.order);
  const rows=teams.map((t,i)=>`<tr class="${i<8?'qualifies':''}"><td>${i+1}</td><td>${tpEscape(t.name)}</td><td>${t.pts}</td><td>${t.gd>0?'+':''}${t.gd}</td><td>${t.gf}</td><td>${i<8?'Provisional qualifier':'Outside top eight'}</td></tr>`).join('');
  result.innerHTML=`<div class="table-scroll"><table class="sports-table"><thead><tr><th>#</th><th>Team</th><th>Pts</th><th>GD</th><th>GF</th><th>Status</th></tr></thead><tbody>${rows}</tbody></table></div><small>This simplified scenario table does not replace official tournament tiebreakers.</small>`;
}
window.tpBracketRounds=[];
function bracketPredictor(){
  const teams=Array.from({length:32},(_,i)=>(document.getElementById(`bracketTeam${i}`).value||`Team ${i+1}`).trim());
  window.tpBracketRounds=[teams];
  renderBracketRound(0);
  result.innerHTML='Round of 32 bracket created. <small>Select each winner and advance the bracket.</small>';
}
function renderBracketRound(roundIndex){
  const container=document.getElementById('bracketRounds');
  const teams=window.tpBracketRounds[roundIndex];
  const labels=['Round of 32','Round of 16','Quarterfinals','Semifinals','Final'];
  container.innerHTML='';
  window.tpBracketRounds.forEach((round,idx)=>{
    const matches=[];
    for(let i=0;i<round.length;i+=2){
      matches.push(`<div class="bracket-match"><select id="bracketWinner${idx}_${i/2}"><option value="${tpEscape(round[i])}">${tpEscape(round[i])}</option><option value="${tpEscape(round[i+1])}">${tpEscape(round[i+1])}</option></select></div>`);
    }
    container.innerHTML+=`<section class="bracket-round"><h3>${labels[idx]}</h3>${matches.join('')}${idx===window.tpBracketRounds.length-1?`<button class="btn light" type="button" onclick="advanceBracket(${idx})">${round.length===2?'Choose Champion':'Advance Winners'}</button>`:''}</section>`;
  });
}
function advanceBracket(roundIndex){
  const round=window.tpBracketRounds[roundIndex];
  const winners=[];
  for(let i=0;i<round.length/2;i++)winners.push(document.getElementById(`bracketWinner${roundIndex}_${i}`).value);
  if(winners.length===1){
    result.innerHTML=`Predicted champion: <strong>${tpEscape(winners[0])}</strong><small>Entertainment prediction only. No betting advice or official result is provided.</small>`;
    return;
  }
  window.tpBracketRounds=window.tpBracketRounds.slice(0,roundIndex+1);
  window.tpBracketRounds.push(winners);
  renderBracketRound(roundIndex+1);
  const summary=window.tpBracketRounds.map((r,i)=>`${['Round of 32','Round of 16','Quarterfinals','Semifinals','Final'][i]}: ${r.join(', ')}`).join('\n');
  result.innerHTML=`<pre>${tpEscape(summary)}</pre>`;
}
function tpPlayerStats(prefix){
  const apps=Number(document.getElementById(`apps${prefix}`).value);
  const goals=Number(document.getElementById(`goals${prefix}`).value);
  const assists=Number(document.getElementById(`assists${prefix}`).value);
  const minutes=Number(document.getElementById(`minutes${prefix}`).value);
  return {name:(document.getElementById(`player${prefix}`).value||`Player ${prefix}`).trim(),apps,goals,assists,minutes,gpg:apps?goals/apps:0,cpg:apps?(goals+assists)/apps:0,mpg:goals&&minutes?minutes/goals:null};
}
function playerComparison(){
  const a=tpPlayerStats('A'),b=tpPlayerStats('B');
  if(a.apps<=0||b.apps<=0)return result.innerHTML='Enter at least one appearance for both players.';
  const row=(label,x,y)=>`<tr><td>${label}</td><td>${x}</td><td>${y}</td></tr>`;
  result.innerHTML=`<div class="table-scroll"><table class="sports-table"><thead><tr><th>Metric</th><th>${tpEscape(a.name)}</th><th>${tpEscape(b.name)}</th></tr></thead><tbody>${row('Appearances',a.apps,b.apps)}${row('Goals',a.goals,b.goals)}${row('Assists',a.assists,b.assists)}${row('Goal contributions',a.goals+a.assists,b.goals+b.assists)}${row('Goals per game',a.gpg.toFixed(3),b.gpg.toFixed(3))}${row('Contributions per game',a.cpg.toFixed(3),b.cpg.toFixed(3))}${row('Minutes per goal',a.mpg?a.mpg.toFixed(1):'N/A',b.mpg?b.mpg.toFixed(1):'N/A')}</tbody></table></div><small>Use the same competition scope, data source and cutoff date for both players.</small>`;
}
function footballRate(){
  const name=(document.getElementById('ratePlayer').value||'Player').trim();
  const apps=Number(document.getElementById('rateApps').value);
  const goals=Number(document.getElementById('rateGoals').value);
  const assists=Number(document.getElementById('rateAssists').value);
  const minutes=Number(document.getElementById('rateMinutes').value);
  if(apps<=0)return result.innerHTML='Enter at least one appearance.';
  result.innerHTML=`<strong>${tpEscape(name)}</strong><small>Goals per game: ${(goals/apps).toFixed(3)}<br>Assists per game: ${(assists/apps).toFixed(3)}<br>Goal contributions per game: ${((goals+assists)/apps).toFixed(3)}<br>Minutes per goal: ${goals&&minutes?(minutes/goals).toFixed(1):'Not available'}</small>`;
}
function lineupBuilder(){
  const formation=document.getElementById('formation').value;
  const players=Array.from({length:11},(_,i)=>(document.getElementById(`lineup${i}`).value||`Player ${i+1}`).trim());
  const rowsByFormation={'4-3-3':[1,4,3,3],'4-4-2':[1,4,4,2],'4-2-3-1':[1,4,2,3,1],'3-5-2':[1,3,5,2],'3-4-3':[1,3,4,3]};
  const labelsByFormation={
    '4-3-3':['Goalkeeper','Defence','Midfield','Forwards'],
    '4-4-2':['Goalkeeper','Defence','Midfield','Forwards'],
    '4-2-3-1':['Goalkeeper','Defence','Holding midfield','Attacking midfield','Forward'],
    '3-5-2':['Goalkeeper','Defence','Midfield','Forwards'],
    '3-4-3':['Goalkeeper','Defence','Midfield','Forwards']
  };
  let cursor=0;
  const rows=rowsByFormation[formation].map((count,index)=>{
    const row=players.slice(cursor,cursor+count);
    cursor+=count;
    return {label:labelsByFormation[formation][index],players:row};
  });
  const pitch=document.getElementById('pitch');
  pitch.hidden=false;
  pitch.innerHTML=rows.map(r=>`<div class="pitch-row">${r.players.map(p=>`<span>${tpEscape(p)}</span>`).join('')}</div>`).join('');
  result.innerHTML=`<strong>${formation} Starting XI</strong><pre>${tpEscape(rows.map(r=>`${r.label}: ${r.players.join(', ')}`).join('\n'))}</pre>`;
}
function playerAge(){
  const name=(document.getElementById('agePlayer').value||'Player').trim();
  const birthRaw=document.getElementById('playerDob').value;
  const matchRaw=document.getElementById('matchDate').value;
  if(!birthRaw||!matchRaw)return result.innerHTML='Select both the date of birth and comparison date.';
  const birth=new Date(`${birthRaw}T00:00:00Z`);
  const match=new Date(`${matchRaw}T00:00:00Z`);
  if(match<birth)return result.innerHTML='The comparison date must be on or after the birth date.';
  let years=match.getUTCFullYear()-birth.getUTCFullYear();
  let months=match.getUTCMonth()-birth.getUTCMonth();
  let days=match.getUTCDate()-birth.getUTCDate();
  if(days<0){months--;days+=new Date(Date.UTC(match.getUTCFullYear(),match.getUTCMonth(),0)).getUTCDate()}
  if(months<0){years--;months+=12}
  const totalDays=Math.floor((match-birth)/86400000);
  result.innerHTML=`<strong>${tpEscape(name)}: ${years} years, ${months} months and ${days} days</strong><small>${totalDays.toLocaleString()} total days old on ${new Intl.DateTimeFormat('en-US',{dateStyle:'long',timeZone:'UTC'}).format(match)}.</small>`;
}

async function aiToolGenerate(task){
  const input=(document.getElementById('aiInput')?.value||'').trim();
  const tone=(document.getElementById('aiTone')?.value||'clear').trim();
  const r=document.getElementById('result');
  if(!input || input.length<5){r.innerHTML='Please enter a clear topic or short draft first.';return}
  if(input.length>2500){r.innerHTML='Please keep the input under 2500 characters.';return}
  r.innerHTML='Generating draft... <small>This may take a few seconds.</small>';
  try{
    const res=await fetch('/api/gemini',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({task,input,tone})});
    const data=await res.json().catch(()=>({}));
    if(!res.ok)throw new Error(data.error||'AI request failed.');
    r.innerHTML='<pre>'+tpEscape(data.text||'No result returned.')+'</pre><small>Review AI output for accuracy, originality, tone and policy-sensitive claims before publishing.</small>';
  }catch(error){
    r.innerHTML=tpEscape(error.message||'AI request failed. Please try again later.');
  }
}
