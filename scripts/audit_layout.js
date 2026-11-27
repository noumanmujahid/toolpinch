const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
const files=process.argv.slice(2);
(async()=>{const b=await chromium.launch();const out=[];
for(const vp of [{w:360,h:740,n:'phone360'},{w:768,h:1024,n:'tablet'},{w:1024,h:768,n:'laptop'},{w:1440,h:900,n:'wide'}]){
 const ctx=await b.newContext({viewport:{width:vp.w,height:vp.h}});
 for(const f of files){const p=await ctx.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message.slice(0,80)));
  try{await p.goto('http://localhost:8765/'+f,{waitUntil:'load',timeout:15000});}catch(e){out.push([vp.n,f,'LOAD FAIL']);await p.close();continue}
  await p.waitForTimeout(250);
  const r=await p.evaluate((W)=>{const iss=[];const de=document.documentElement;if(de.scrollWidth>W+1)iss.push('page scrolls sideways ('+de.scrollWidth+'px)');
   const inScroll=el=>{for(let x=el.parentElement;x;x=x.parentElement){const s=getComputedStyle(x);if(/(auto|scroll|hidden)/.test(s.overflowX))return true}return false};
   const seen=new Set();
   for(const el of document.querySelectorAll('body *')){const rc=el.getBoundingClientRect();if(!rc.width)continue;
     if(rc.right>W+2&&!inScroll(el)){const k=el.tagName+'.'+(el.className||'').toString().slice(0,30);if(!seen.has(k)){seen.add(k);iss.push('sticks out: '+k+' right='+Math.round(rc.right))}}}
   for(const el of document.querySelectorAll('input[type=number],input[type=text],input:not([type]),select,input[type=date],input[type=time]')){const rc=el.getBoundingClientRect();if(!rc.width||getComputedStyle(el).display==='none')continue;
     if(rc.width<64)iss.push('narrow input #'+(el.id||el.name)+' '+Math.round(rc.width)+'px');
     if(el.tagName==='INPUT'&&el.value&&el.scrollWidth>el.clientWidth+2)iss.push('clipped value #'+el.id);}
   for(const el of document.querySelectorAll('button, .mc-button')){if(el.scrollWidth>el.clientWidth+2)iss.push('button text clipped: '+el.textContent.trim().slice(0,30))}
   return iss.slice(0,8)},vp.w);
  if(errs.length)r.push('JS error: '+errs[0]);
  if(r.length)out.push([vp.n,f,r.join(' | ')]);
  await p.close()}
 await ctx.close()}
await b.close();console.log(out.length?out.map(x=>x.join(' :: ')).join('\n'):'ALL CLEAN')})();
