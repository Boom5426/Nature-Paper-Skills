import { defineConfig } from '@playwright/test';
export default defineConfig({
 testDir:'./tests/browser',
 fullyParallel:true,
 workers:process.env.CI?2:3,
 retries:process.env.CI?1:0,
 timeout:30000,
 reporter:[['list'],['html',{open:'never'}],['json',{outputFile:'quality/results.json'}]],
 use:{baseURL:'http://127.0.0.1:4321/Nature-Paper-Skills/',trace:'retain-on-failure',screenshot:'only-on-failure',reducedMotion:'reduce',launchOptions:{executablePath:process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH||undefined,args:['--no-sandbox','--disable-dev-shm-usage']}},
 webServer:{command:'npm run preview -- --host 127.0.0.1 --port 4321',url:'http://127.0.0.1:4321/Nature-Paper-Skills/',reuseExistingServer:!process.env.CI,timeout:60000,stdout:'pipe',stderr:'pipe'},
});
