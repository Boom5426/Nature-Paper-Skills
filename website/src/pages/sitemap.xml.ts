import {routes,url,ORIGIN} from '../lib/site';
export function GET(){
 const entries=routes.flatMap(route=>(['en','zh'] as const).map(locale=>`<url><loc>${ORIGIN}${url(locale,route)}</loc><xhtml:link rel="alternate" hreflang="en" href="${ORIGIN}${url('en',route)}"/><xhtml:link rel="alternate" hreflang="zh-CN" href="${ORIGIN}${url('zh',route)}"/></url>`));
 return new Response(`<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">${entries.join('')}</urlset>`,{headers:{'Content-Type':'application/xml'}});
}
