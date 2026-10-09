const isZh = document.documentElement.lang === 'zh-CN';
const toggle = document.querySelector<HTMLButtonElement>('.menu-toggle');
const nav = document.querySelector<HTMLElement>('#site-navigation');
function closeMenu(restore = false) {
  nav?.removeAttribute('data-open');
  toggle?.setAttribute('aria-expanded','false');
  if (restore) toggle?.focus();
}
toggle?.addEventListener('click', () => {
  const open = toggle.getAttribute('aria-expanded') !== 'true';
  nav?.setAttribute('data-open', String(open));
  toggle.setAttribute('aria-expanded', String(open));
});
document.addEventListener('keydown', e => { if(e.key==='Escape' && toggle?.getAttribute('aria-expanded')==='true') closeMenu(true); });
document.addEventListener('click', e => { if (e.target instanceof Node && !nav?.contains(e.target) && !toggle?.contains(e.target)) closeMenu(); });
nav?.querySelectorAll('a').forEach(a => a.addEventListener('click',()=>closeMenu()));
const languageLink = document.querySelector<HTMLAnchorElement>('[data-locale-switch]');
function syncLanguageHash() { if(languageLink) {const target=new URL(languageLink.href);target.hash=location.hash;languageLink.href=target.href;} }
syncLanguageHash(); addEventListener('hashchange',syncLanguageHash);

document.querySelectorAll<HTMLElement>('[data-tabs]').forEach(group => {
  const tabs = Array.from(group.querySelectorAll<HTMLButtonElement>('[role="tab"]'));
  const panels = Array.from(group.querySelectorAll<HTMLElement>('[role="tabpanel"]'));
  const activate = (tab: HTMLButtonElement, focus = false) => {
    tabs.forEach(t => { const selected=t===tab;t.setAttribute('aria-selected',String(selected));t.tabIndex=selected?0:-1; });
    panels.forEach(p => {p.hidden = p.id!==tab.getAttribute('aria-controls');});
    if(focus) tab.focus();
  };
  tabs.forEach((tab,index) => {
    tab.addEventListener('click',()=>activate(tab));
    tab.addEventListener('keydown',e=>{
      let next=index;
      if(e.key==='ArrowRight'||e.key==='ArrowDown')next=(index+1)%tabs.length;
      else if(e.key==='ArrowLeft'||e.key==='ArrowUp')next=(index-1+tabs.length)%tabs.length;
      else if(e.key==='Home')next=0;
      else if(e.key==='End')next=tabs.length-1;
      else return;
      e.preventDefault();activate(tabs[next],true);
    });
  });
});

document.querySelectorAll<HTMLButtonElement>('[data-copy]').forEach(button => {
  const original = button.textContent || '';
  let timeout: ReturnType<typeof setTimeout>;
  button.addEventListener('click',async()=>{
    const target=document.getElementById(button.dataset.copy || '');
    if(!target) return;
    const feedback=document.getElementById('copy-feedback');
    clearTimeout(timeout);
    try {
      if(!navigator.clipboard?.writeText) throw new Error('Clipboard not available');
      await navigator.clipboard.writeText(target.textContent || '');
      const msg=isZh?'已复制':'Copied';button.textContent=msg;if(feedback)feedback.textContent=msg;
    } catch {
      const range=document.createRange();range.selectNodeContents(target);const selection=getSelection();selection?.removeAllRanges();selection?.addRange(range);target.focus();
      const msg=isZh?'已选中文本，请手动复制':'Text selected — copy manually';button.textContent=msg;if(feedback)feedback.textContent=msg;
    }
    timeout=setTimeout(()=>{button.textContent=original;},2400);
  });
});

document.querySelectorAll<HTMLButtonElement>('[data-highlight-toggle]').forEach(button=>button.addEventListener('click',()=>{
  const root=button.closest('[data-example]');
  const highlighted=root?.classList.toggle('highlight-on') || false;
  button.setAttribute('aria-pressed',String(highlighted));
}));
