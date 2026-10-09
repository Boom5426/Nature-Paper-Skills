import {BASE,ORIGIN} from '../lib/site';
export function GET(){return new Response(`User-agent: *\nAllow: /\nSitemap: ${ORIGIN}${BASE}/sitemap.xml\n`,{headers:{'Content-Type':'text/plain'}});}
