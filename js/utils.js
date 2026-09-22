export const Utils = (() => {
  const escapeHtml = (value = '') => String(value).replace(/[&<>"']/g, ch => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[ch]));
  const normalize = (value = '') => String(value).normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().trim();
  const slugify = (value = '') => normalize(value).replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'');
  const fileName = path => decodeURIComponent(path.split('/').pop() || 'recurso.txt');
  const mimeFor = filename => {
    const ext=(filename.split('.').pop()||'').toLowerCase();
    return ext==='py'?'text/x-python;charset=utf-8':ext==='md'?'text/markdown;charset=utf-8':'text/plain;charset=utf-8';
  };
  const downloadText = (filename,text) => { const blob=new Blob([text],{type:mimeFor(filename)}); const url=URL.createObjectURL(blob); const a=document.createElement('a'); a.href=url;a.download=filename;document.body.appendChild(a);a.click();a.remove();URL.revokeObjectURL(url); };
  const copyText = async text => { if(navigator.clipboard&&window.isSecureContext){await navigator.clipboard.writeText(text);return;} const a=document.createElement('textarea');a.value=text;a.style.position='fixed';a.style.opacity='0';document.body.appendChild(a);a.select();document.execCommand('copy');a.remove(); };
  return {escapeHtml,normalize,slugify,fileName,downloadText,copyText};
})();
