/** Pure, shared installation text builder. It never executes a command. */
export const repositoryURL = 'https://github.com/Boom5426/Nature-Paper-Skills';
const installerURL = 'https://raw.githubusercontent.com/Boom5426/Nature-Paper-Skills/main/install.sh';
export const profileFlags = { recommended:'--set recommended', figures:'--set recommended --figure', all:'--set all' };
export const agents = ['codex','claude','web'];
export const operatingSystems = ['linux','macos','windows','wsl'];
export const methods = ['prompt','command','clone'];
/** @param {{agent:string,os:string,profile:string,method:string,locale:string}} options
 * @param {{all:number,recommended:number,figures:number}} counts */
export function buildInstallation(options, counts) {
 const {agent,os,profile,method,locale}=options;
 if(!agents.includes(agent)||!operatingSystems.includes(os)||!methods.includes(method)||!Object.hasOwn(profileFlags,profile)||!['en','zh'].includes(locale))throw new TypeError('Invalid installation selection');
 for(const count of Object.values(counts))if(!Number.isSafeInteger(count)||count<=0)throw new TypeError('Invalid profile count');
 const zh=locale==='zh';const t=(en,cn)=>zh?cn:en;
 const flags=profileFlags[profile];const count=counts[profile];
 const agentName=agent==='codex'?'Codex':agent==='claude'?'Claude Code':'ChatGPT Work';
 const osName={linux:'Linux',macos:'macOS',windows:t('native Windows','原生 Windows'),wsl:'WSL2'}[os];
 const profileName={all:t('full workflow','完整工作流'),recommended:t('writing and review stack','写作与审稿组合'),figures:t('writing and review stack with the figure add-on','写作审稿与图形扩展组合')}[profile];
 const localArgs=`--agent ${agent} ${flags}`;
 const invocation=agent==='codex'?'$paper-workflow':'/paper-workflow';
 const blocked=method!=='prompt'&&(agent==='web'||os==='windows');
 if(blocked)return {text:t('This environment does not have a verified copy-and-run shell route. Choose the agent-assisted instruction and read the environment guide.','当前环境没有经过确认的直接 Shell 安装路径。请选择 Agent 安装指令，并阅读对应环境指南。'),verification:'',notice:t('Do not run a Bash command in native PowerShell, or treat files in a web sandbox as account registration.','不要在原生 PowerShell 中直接执行 Bash，也不要把网页沙箱文件视为账号注册。'),blocked:true,kind:'notice'};
 const retrieval=t('If the page cannot be read, use an available GitHub tool or git clone to retrieve main and read INSTALL.md from the repository root; do not substitute search snippets.','如果页面无法读取，使用可用的 GitHub 工具或 git clone 获取 main 分支，再读取根目录 INSTALL.md；不要用搜索摘要替代原文。');
 if(agent==='web')return {
  text:t(`Read ${repositoryURL}/blob/main/INSTALL.md. Check whether this ChatGPT Work account exposes a supported persistent skill/plugin registration flow. If available, follow it to install the ${profileName} (${count} skills), preserving the explicit profile ${flags}, and report the registered ID and whether new-chat invocation was actually tested. If no supported registration flow is available, stop and report the missing capability. Downloading files or creating a sandbox directory is not account installation.\n\n${retrieval}`,`读取 ${repositoryURL}/blob/main/INSTALL.md。检查此 ChatGPT Work 账号是否提供受支持的技能或插件持久注册流程。若可用，按指南安装${profileName}（${count} 个技能），保留明确的 ${flags} 选择，报告注册 ID 与是否实际测试了新会话调用。若缺少注册流程，停止并说明缺失能力。下载文件或在沙箱建立目录不等于安装到账号。\n\n${retrieval}`),
  verification:t('Confirm persistent account/workspace registration and a new-chat invocation. Package integrity alone does not verify either.','确认账号或工作区持久注册，以及新会话实际调用。打包完整性检查无法证明这两项。'),
  notice:t('Persistent web registration and new-chat invocation remain unverified for this repository. A supported account/workspace flow is required.','本仓库的网页版持久注册与新会话调用尚未验证，需要账号或工作区提供受支持的流程。'),blocked:false,kind:'prompt'};
 const notice=os==='windows'?t('Native Windows client discovery remains unverified. The agent must identify its actual environment. Do not install runtimes or switch to WSL automatically.','原生 Windows 客户端的技能发现仍未验证。Agent 必须确认实际运行环境，不应自动安装运行时或切换到 WSL。'):os==='wsl'?t('Use the same WSL distribution as the agent. Changing the terminal alone does not switch the client; no live Windows/WSL invocation test is recorded.','与 Agent 使用同一个 WSL 发行版。更换终端不等于切换客户端；目前没有记录 Windows/WSL 实际调用测试。'):t('Documented Bash route; requires Python 3.9+, curl and tar for remote installation. Skill files do not install optional plotting or editing tools.','已文档化的 Bash 路径；需要 Python 3.9+，远程安装还需 curl 和 tar。安装技能文件不会安装可选绘图或编辑工具。');
 const verifyCommand=method==='clone'?`bash install.sh ${localArgs} --doctor`:`curl -fsSL ${installerURL} | bash -s -- ${localArgs} --doctor`;
 const verification=(os==='windows'?t('Ask the agent to run the documented installation checks for the actual native skill directory.','请 Agent 按指南对实际原生技能目录执行安装检查。'):verifyCommand)+t(`\n\nFile checks are not client discovery. Refresh or open a new ${agentName} session, invoke ${invocation}, then run the first-revision example.`,`\n\n文件检查不等于客户端已经发现技能。刷新或新建 ${agentName} 会话，调用 ${invocation}，再运行第一次修订案例。`);
 let content;
 if(method==='prompt')content=t(`Read and follow ${repositoryURL}/blob/main/INSTALL.md. Install the ${profileName} (${count} skills) for my local ${agentName} environment on ${osName}, explicitly using ${flags}, and verify the same profile. Preserve existing skills and local changes. Report the installed path, count, preserved entries, doctor result and whether actual new-session discovery was tested. Do not install extra runtimes or switch environments without approval.\n\n${retrieval}`,`读取并执行 ${repositoryURL}/blob/main/INSTALL.md，为我的 ${osName} 本地 ${agentName} 环境安装${profileName}（${count} 个技能），明确使用 ${flags}，并对同一组合执行验证。保留现有技能与本地修改。报告安装路径、数量、保留项、doctor 结果，以及是否实际测试了新会话技能发现。未经允许，不安装额外运行时或切换环境。\n\n${retrieval}`);
 else if(method==='command')content=`curl -fsSL ${installerURL} | bash -s -- ${localArgs} --on-conflict keep`;
 else content=`git clone --depth 1 --branch main ${repositoryURL}.git Nature-Paper-Skills &&\ncd Nature-Paper-Skills &&\nbash install.sh ${localArgs} --on-conflict keep`;
 return {text:content,verification,notice,blocked:false,kind:method==='prompt'?'prompt':'bash'};
}
