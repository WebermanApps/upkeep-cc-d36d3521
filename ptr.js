/* Pull-to-refresh: works in iOS standalone; ignores inputs and swipe areas */
(function(){
var T=70,y0=null,d=0,s=document.createElement('div');
s.setAttribute('aria-hidden','true');
s.style.cssText='position:fixed;top:calc(env(safe-area-inset-top) + 8px);left:50%;width:32px;height:32px;margin-left:-16px;border-radius:50%;background:#fff;box-shadow:0 1px 4px rgba(0,0,0,.2);display:flex;align-items:center;justify-content:center;z-index:9999;opacity:0;transform:translateY(-48px);transition:opacity .15s;pointer-events:none';
s.innerHTML='<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#171717" stroke-width="2.5"><path d="M21 12a9 9 0 1 1-3-6.7"/><path d="M21 3v6h-6"/></svg>';
var st=document.createElement('style');st.textContent='@keyframes ptrspin{to{transform:rotate(360deg)}}.ptr-go svg{animation:ptrspin .7s linear infinite}';
document.head.appendChild(st);
function top(){return (document.scrollingElement||document.documentElement).scrollTop<=0}
function skip(t){return t.closest&&t.closest('input,textarea,select,[contenteditable],[data-no-ptr],.swipe,[class*=carousel],[class*=swipe]')}
addEventListener('touchstart',function(e){if(!document.body.contains(s))document.body.appendChild(s);y0=(e.touches.length===1&&top()&&!skip(e.target))?e.touches[0].clientY:null;d=0},{passive:true});
addEventListener('touchmove',function(e){if(y0===null)return;d=e.touches[0].clientY-y0;if(d<=0||!top()){s.style.opacity=0;return}
var p=Math.min(d,T*1.5);s.style.opacity=Math.min(1,p/T);s.style.transform='translateY('+(p/1.5-48)+'px) rotate('+p*4+'deg)'},{passive:true});
function end(){if(y0===null)return;y0=null;if(d>T&&top()){s.className='ptr-go';s.style.transform='translateY(16px)';
var u=new URL(location.href);u.searchParams.set('_r',Date.now());setTimeout(function(){location.replace(u.toString())},150)}else{s.style.opacity=0;s.style.transform='translateY(-48px)'}d=0}
addEventListener('touchend',end,{passive:true});addEventListener('touchcancel',function(){y0=null;s.style.opacity=0},{passive:true});
})();
