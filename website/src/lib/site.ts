export type Locale = 'en' | 'zh';
export const REPO = 'https://github.com/Boom5426/Nature-Paper-Skills';
export const BASE = '/Nature-Paper-Skills';
export const ORIGIN = 'https://boom5426.github.io';
export const routes = ['', 'workflow', 'tasks', 'examples/first-revision', 'skills', 'install', 'docs'] as const;
export type Route = typeof routes[number];
export function url(locale: Locale, path = ''): string {
  const [route, hash] = path.split('#');
  return `${BASE}/${locale === 'zh' ? 'zh/' : ''}${route.replace(/^\/+|\/+$/g, '')}${route ? '/' : ''}${hash ? `#${hash}` : ''}`;
}
export const source = (path: string) => `${REPO}/blob/main/${path}`;
export const text = (locale: Locale, en: string, zh: string) => locale === 'zh' ? zh : en;
export const sectionSource = 'skills/core/paper-workflow/references/section-contracts.md';
export const titles: Record<Route, [string, string]> = {
  '': ['Evidence-grounded scientific writing', '以证据为基础的科研写作'],
  workflow: ['The scientific writing workflow', '科学写作工作流'],
  tasks: ['Find your next manuscript task', '从你的论文任务开始'],
  'examples/first-revision': ['A first revision, with the evidence intact', '完成第一次修订，保留完整证据'],
  skills: ['The skill library', '技能目录'],
  install: ['A better workflow starts here', '从这里开始你的论文工作流'],
  docs: ['A guide for every next step', '找到下一步需要的指南'],
};
export const labels = (l: Locale) => ({
  source: text(l, 'View source', '查看源码'),
  input: text(l, 'What you provide', '你提供什么'),
  output: text(l, 'What you receive', '你得到什么'),
  copy: text(l, 'Copy prompt', '复制提示词'),
  copied: text(l, 'Copied', '已复制'),
  getStarted: text(l, 'Get started', '快速开始'),
  example: text(l, 'See a worked example', '查看完整示例'),
  openDocs: text(l, 'Read the guide', '阅读指南'),
});
