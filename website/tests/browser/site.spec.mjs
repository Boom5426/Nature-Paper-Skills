import { test,expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';
import {mkdir} from 'node:fs/promises';
import repository from '../../src/data/repository.json' with {type: 'json'};
const counts=repository.counts;
const routes=['','workflow/','tasks/','examples/first-revision/','skills/','install/','docs/'];
for(const locale of ['','zh/'])for(const route of routes){
 test(`route ${locale}${route||'home'}`,async({page})=>{
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  const response=await page.goto(locale+route||'./');expect(response?.status()).toBe(200);
  await expect(page.locator('h1')).toHaveCount(1);await expect(page.locator('html')).toHaveAttribute('lang',locale?'zh-CN':'en');
  await expect(page.locator('h1')).toBeVisible();expect((await page.locator('main').innerText()).trim().length).toBeGreaterThan(150);expect(errors).toEqual([]);
 });
}
for(const locale of ['','zh/'])for(const route of ['','install/','skills/','examples/first-revision/'])for(const width of [375,768,1024,1440,1920]){
 test(`layout ${locale||'en/'}${route||'home'} ${width}`,async({page})=>{
  await page.setViewportSize({width,height:950});await page.goto(locale+route||'./');await page.evaluate(()=>document.fonts.ready);
  expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1)).toBe(true);
  await mkdir('quality/screenshots',{recursive:true});
  await page.screenshot({path:`quality/screenshots/${locale?'zh':'en'}_${route.replaceAll('/','-')||'home'}_${width}.png`,fullPage:true,animations:'disabled'});
 });
}
for(const locale of ['','zh/'])for(const route of ['','install/','skills/','examples/first-revision/']){
 test(`accessibility ${locale||'en/'}${route||'home'}`,async({page})=>{
  await page.goto(locale+route||'./');const result=await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21aa']).analyze();
  expect(result.violations.map(v=>({id:v.id,description:v.description,nodes:v.nodes.map(n=>({target:n.target,summary:n.failureSummary}))}))).toEqual([]);
 });
}
test('workflow and section tabs support click and keyboard',async({page})=>{
 await page.goto('./');await page.locator('#stage-tab-3').click();await expect(page.locator('#stage-panel-3')).toBeVisible();
 await page.locator('#stage-tab-3').press('ArrowRight');await expect(page.locator('#stage-tab-4')).toBeFocused();await expect(page.locator('#stage-panel-4')).toBeVisible();
 await page.locator('#contract-tab-0').click();await page.locator('#contract-tab-0').press('End');await expect(page.locator('#contract-panel-3')).toBeVisible();
});
test('mobile menu closes on Escape and restores focus',async({page})=>{
 await page.setViewportSize({width:375,height:812});await page.goto('./');const button=page.locator('.menu-toggle');
 await button.click();await expect(page.locator('#site-navigation')).toBeVisible();await page.keyboard.press('Escape');await expect(button).toBeFocused();await expect(page.locator('#site-navigation')).not.toBeVisible();
});
test('language switch keeps the current route and anchor',async({page})=>{
 await page.goto('tasks/#rebuttal');await page.locator('[data-locale-switch]').click();await expect(page).toHaveURL(/\/zh\/tasks\/#rebuttal$/);await expect(page.locator('html')).toHaveAttribute('lang','zh-CN');
});
test('skill search, profile filters and empty-state reset work',async({page})=>{
 await page.goto('skills/');await expect(page.locator('[data-skill]:visible')).toHaveCount(counts.all);
 await page.selectOption('#skill-profile','recommended');await expect(page.locator('[data-skill]:visible')).toHaveCount(counts.recommended);
 await page.selectOption('#skill-profile','figures');await expect(page.locator('[data-skill]:visible')).toHaveCount(counts.figures);
 await page.fill('#skill-search','absolutely-no-matching-skill');await expect(page.locator('[data-no-results]')).toBeVisible();
 await page.locator('[data-reset-catalog]').click();await expect(page.locator('[data-skill]:visible')).toHaveCount(counts.all);
 await page.selectOption('#skill-category','figure');await expect(page.locator('[data-skill]:visible')).toHaveCount(repository.skills.filter(s=>s.category==='figure').length);
 await page.selectOption('#skill-category','all');await page.fill('#skill-search','摘要');await expect(page.locator('[data-skill]:visible').first()).toBeVisible();
});
test('installation follows the chosen profile and blocks unsupported shells',async({page})=>{
 await page.goto('install/');await page.locator('input[name=agent][value=claude]').check({force:true});await page.locator('input[name=method][value=command]').check({force:true});
 await expect(page.locator('#install-content')).toContainText('--agent claude --set all --on-conflict keep');
 await page.locator('input[name=profile][value=figures]').check({force:true});await expect(page.locator('#install-content')).toContainText('--set recommended --figure');
 await page.selectOption('#install-os','windows');await expect(page.locator('input[name=method][value=command]')).toBeDisabled();await expect(page.locator('input[name=method][value=prompt]')).toBeChecked();
 await expect(page.locator('#install-content')).not.toContainText('curl -fsSL');await expect(page.locator('[data-install-notice]')).toContainText('unverified');
 await page.locator('input[name=agent][value=web]').check({force:true});await expect(page.locator('#install-os')).toBeDisabled();await expect(page.locator('#install-content')).toContainText('persistent');
 await expect(page.locator('#install-content')).toContainText(`${counts.figures} skills`);
});
test('copy button copies the complete task, and failure has a manual fallback',async({page,context})=>{
 await context.grantPermissions(['clipboard-read','clipboard-write']);await page.goto('tasks/');const expected=await page.locator('#task-prompt-section').textContent();
 await page.locator('[data-copy=task-prompt-section]').click();expect(await page.evaluate(()=>navigator.clipboard.readText())).toBe(expected);
 await page.evaluate(()=>{Object.defineProperty(navigator,'clipboard',{configurable:true,value:{writeText:()=>Promise.reject(new Error('test-denied'))}});});
 await page.locator('[data-copy=task-prompt-section]').click();await expect(page.locator('[data-copy=task-prompt-section]')).toContainText('Text selected');expect(await page.evaluate(()=>getSelection()?.toString())).toBe(expected);
});
test('example highlighting changes presentation but not the source text',async({page})=>{
 await page.goto('examples/first-revision/');const original=await page.locator('.example-grid').textContent();await page.locator('[data-highlight-toggle]').click();await expect(page.locator('[data-highlight-toggle]')).toHaveAttribute('aria-pressed','false');expect(await page.locator('.example-grid').textContent()).toBe(original);
});
test('essential pages remain readable and linked without JavaScript',async({browser})=>{
 const context=await browser.newContext({javaScriptEnabled:false,viewport:{width:375,height:812}});const page=await context.newPage();
 for(const path of ['','skills/','install/']){await page.goto(`http://127.0.0.1:4321/Nature-Paper-Skills/${path}`);await expect(page.locator('h1')).toBeVisible();expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1)).toBe(true);}
 await expect(page.locator('#install-content')).toContainText('INSTALL.md');await page.goto('http://127.0.0.1:4321/Nature-Paper-Skills/skills/');await expect(page.locator('[data-skill]')).toHaveCount(counts.all);await context.close();
});
