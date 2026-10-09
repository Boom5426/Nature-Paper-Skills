import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  site: 'https://boom5426.github.io',
  base: '/Nature-Paper-Skills',
  trailingSlash: 'always',
  output: 'static',
  vite: { plugins: [tailwindcss()] },
  build: { inlineStylesheets: 'never' },
  devToolbar: { enabled: false },
});
