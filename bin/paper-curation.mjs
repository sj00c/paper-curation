#!/usr/bin/env node
import { spawnSync } from 'node:child_process';
import {
  existsSync,
  mkdirSync,
  readFileSync,
  readdirSync,
  realpathSync,
  writeFileSync,
} from 'node:fs';
import { homedir } from 'node:os';
import path from 'node:path';
import process from 'node:process';
import { fileURLToPath } from 'node:url';

const REPO_URL = 'https://github.com/jehyunlee/paper-curation.git';
const ENV_NAME = 'py312';
const VALID_AUTH = new Set(['auto', 'oauth', 'api-key']);
const OAUTH_UNSET_ENV = ['ANTHROPIC_API_KEY', 'ANTHROPIC_AUTH_TOKEN'];
const MIN_CLAUDE_VERSION = [2, 1, 205];
const MANAGED_SKILL_MARKER = '<!-- paper-curation-managed-skill -->';

class CliError extends Error {
  constructor(message, code = 1) {
    super(message);
    this.name = 'CliError';
    this.code = code;
  }
}

function usage() {
  return `paper-curation: dependency-free local bootstrap for paper-curation

Usage:
  node ./bin/paper-curation.mjs init [--dir PATH] [--auth auto|oauth|api-key] [--fresh-config|--reuse-config] [--run-first]
  node ./bin/paper-curation.mjs setup [--dir PATH] [--auth auto|oauth|api-key] [--fresh-config|--reuse-config] [--run-first]
  node ./bin/paper-curation.mjs skill install [--dir PATH]
  node ./bin/paper-curation.mjs doctor [--dir PATH] [--network] [--topic TOPIC] [--anthropic-smoke]
  node ./bin/paper-curation.mjs run [--dir PATH] -- [run_full.py args...]
  node ./bin/paper-curation.mjs auth status
  node ./bin/paper-curation.mjs auth setup-token
  node ./bin/paper-curation.mjs topic [--dir PATH] [--json]
  node ./bin/paper-curation.mjs help

Defaults:
  --dir paper-curation for init, current directory for other commands.
  --auth auto.
  setup/init pass --no-run to Python setup unless --run-first is present.

Safe first run from the current checkout:
  node ./bin/paper-curation.mjs skill install
  node ./bin/paper-curation.mjs setup --fresh-config
  node ./bin/paper-curation.mjs doctor --network --anthropic-smoke
  PAPER_CURATION_NO_DEPLOY=1 node ./bin/paper-curation.mjs run -- \\
    --topic <configured-topic> --mode smoke --source zotero --smoke-limit 1 --strict-pdf --no-deploy

  Setup never silently trusts an existing ignored config.json. Use --reuse-config
  only after confirming it belongs to the current user. Authentication defaults
  to auto and supports either Claude OAuth or an Anthropic Console API key.
  Put required keys in .env (recommended) instead of shell history:
    ZOTERO_API_KEY=...
    GEMINI_API_KEY=...

  The dependency-free skill installer runs before Python environment setup.
  Setup validates the Zotero key, supports selecting multiple collections, and
  creates local topic aliases and pdf_cache automatically.
`;
}

export function loadDotEnv(dir) {
  const envPath = path.join(dir, '.env');
  if (!existsSync(envPath)) return {};

  const values = {};
  for (const rawLine of readFileSync(envPath, 'utf8').split(/\r?\n/)) {
    let line = rawLine.trim();
    if (!line || line.startsWith('#')) continue;
    if (line.startsWith('export ')) line = line.slice(7).trim();
    const separator = line.indexOf('=');
    if (separator < 1) continue;

    const key = line.slice(0, separator).trim();
    if (!/^[A-Za-z_][A-Za-z0-9_]*$/.test(key)) continue;
    let value = line.slice(separator + 1).trim();
    if (
      value.length >= 2
      && value[0] === value.at(-1)
      && (value[0] === '"' || value[0] === "'")
    ) {
      value = value.slice(1, -1);
    } else {
      value = value.replace(/\s+#.*$/, '').trimEnd();
    }
    if (value) values[key] = value;
  }
  return values;
}

function isHelpToken(token) {
  return token === '-h' || token === '--help' || token === 'help';
}

function readOptionValue(argv, index, option) {
  const token = argv[index];
  const eq = token.indexOf('=');
  if (eq !== -1) return { value: token.slice(eq + 1), consumed: 1 };
  const value = argv[index + 1];
  if (!value || value.startsWith('--')) {
    throw new CliError(`${option} requires a value.`);
  }
  return { value, consumed: 2 };
}

export function parseArgs(argv) {
  const args = [...argv];
  const passthroughAt = args.indexOf('--');
  const cliArgs = passthroughAt === -1 ? args : args.slice(0, passthroughAt);
  if (args.length === 0 || cliArgs.some(isHelpToken)) {
    return {
      command: 'help',
      dir: null,
      auth: 'auto',
      configMode: 'prompt',
      runFirst: false,
      forwarded: [],
      json: false,
    };
  }

  let command = null;
  let dir = null;
  let auth = 'auto';
  let configMode = 'prompt';
  let runFirst = false;
  let forwarded = [];
  let json = false;

  for (let i = 0; i < args.length; i += 1) {
    const token = args[i];

    if (token === '--') {
      forwarded = args.slice(i + 1);
      break;
    }

    if (token === '--dir' || token.startsWith('--dir=')) {
      const parsed = readOptionValue(args, i, '--dir');
      dir = parsed.value;
      i += parsed.consumed - 1;
      continue;
    }

    if (token === '--auth' || token.startsWith('--auth=')) {
      const parsed = readOptionValue(args, i, '--auth');
      auth = parsed.value;
      i += parsed.consumed - 1;
      continue;
    }

    if (token === '--run-first') {
      runFirst = true;
      continue;
    }
    if (token === '--fresh-config' || token === '--reuse-config') {
      const requested = token === '--fresh-config' ? 'fresh' : 'reuse';
      if (configMode !== 'prompt' && configMode !== requested) {
        throw new CliError('--fresh-config and --reuse-config are mutually exclusive.');
      }
      configMode = requested;
      continue;
    }

    if (token.startsWith('--')) {
      if (command === 'topic' && token === '--json') {
        json = true;
        continue;
      }
      if (command === 'doctor') {
        forwarded.push(token);
        continue;
      }
      throw new CliError(`Unknown option: ${token}`);
    }

    if (!command) {
      command = token;
      continue;
    }

    if ((command === 'auth' || command === 'skill') && !forwarded.length) {
      forwarded.push(token);
      continue;
    }
    if (command === 'doctor') {
      forwarded.push(token);
      continue;
    }
    if (command === 'topic') {
      if (token === 'list' && !forwarded.length) {
        forwarded.push(token);
        continue;
      }
      throw new CliError(`Unexpected topic argument: ${token}`);
    }


    throw new CliError(`Unexpected argument: ${token}`);
  }

  if (!command) command = 'help';
  if (!VALID_AUTH.has(auth)) {
    throw new CliError(`Invalid --auth value '${auth}'. Expected auto, oauth, or api-key.`);
  }

  return {
    command,
    dir,
    auth,
    configMode,
    runFirst,
    forwarded,
    json,
  };
}

function resolveTargetDir(parsed, cwd) {
  const fallback = parsed.command === 'init' ? 'paper-curation' : '.';
  return path.resolve(cwd, parsed.dir ?? fallback);
}

function isCheckout(dir) {
  return existsSync(path.join(dir, '.git')) && existsSync(path.join(dir, 'pipeline', 'setup.py'));
}

function commandStep(command, args, options = {}) {
  return {
    command,
    args,
    cwd: options.cwd ?? process.cwd(),
    env: options.env ?? {},
    stdio: options.stdio ?? 'inherit',
    ...(options.unsetEnv?.length ? { unsetEnv: [...options.unsetEnv] } : {}),
    ...(options.minClaudeVersion ? { minClaudeVersion: [...options.minClaudeVersion] } : {}),
    ...(options.onlyIfPreviousFailed ? { onlyIfPreviousFailed: true } : {}),
  };
}

function condaStep(cwd, args, options = {}) {
  return commandStep('conda', ['run', '-n', ENV_NAME, ...args], {
    ...options,
    cwd,
    env: { ...options.env, PYTHONUTF8: '1' },
  });
}

function skillInstallStep(cwd) {
  return { action: 'installSkill', cwd };
}

function topicListStep(cwd, json = false) {
  return { action: 'listTopics', cwd, json };
}

function readManagedSkillManifest(cwd) {
  const manifestPath = path.join(cwd, 'skills', 'manifest.json');
  if (!existsSync(manifestPath)) {
    throw new CliError(`Missing managed skill manifest: ${manifestPath}`);
  }
  const manifest = JSON.parse(readFileSync(manifestPath, 'utf8'));
  if (!Array.isArray(manifest.skills) || manifest.skills.length === 0) {
    throw new CliError(`Managed skill manifest has no skills: ${manifestPath}`);
  }
  return manifest;
}

function renderSkillTemplate(template, values) {
  return template.replaceAll(/\{([a-zA-Z0-9_]+)\}/g, (match, key) => {
    if (Object.hasOwn(values, key)) return String(values[key]);
    throw new CliError(`Unknown skill template field: ${match}`);
  });
}

function formatList(values) {
  return values.length ? values.join(', ') : '(none)';
}

function hasManagedMarker(filePath) {
  return existsSync(filePath) && readFileSync(filePath, 'utf8').includes(MANAGED_SKILL_MARKER);
}

function findStaleManagedSkillIds(skillsHome, activeIds) {
  if (!existsSync(skillsHome)) return [];
  const stale = [];
  for (const entry of readdirSync(skillsHome, { withFileTypes: true })) {
    if (!entry.isDirectory() || activeIds.has(entry.name)) continue;
    const skillFile = path.join(skillsHome, entry.name, 'SKILL.md');
    if (hasManagedMarker(skillFile)) stale.push(entry.name);
  }
  return stale.sort();
}

export function installSkill(cwd, home = homedir()) {
  requireCheckout(cwd);
  const rootTemplatePath = path.join(cwd, 'SKILL.md.template');
  const internalTemplatePath = path.join(cwd, 'skills', 'SKILL.md.template');
  if (!existsSync(rootTemplatePath)) {
    throw new CliError(`Missing skill template: ${rootTemplatePath}`);
  }
  if (!existsSync(internalTemplatePath)) {
    throw new CliError(`Missing managed skill template: ${internalTemplatePath}`);
  }

  const manifest = readManagedSkillManifest(cwd);
  const rootTemplate = readFileSync(rootTemplatePath, 'utf8');
  const internalTemplate = readFileSync(internalTemplatePath, 'utf8');
  const projectSkill = path.join(cwd, 'SKILL.md');
  const skillsHome = path.join(home, '.claude', 'skills');
  const activeIds = new Set(manifest.skills.map((skill) => skill.id));
  const result = {
    installed: [],
    skipped: [],
    stale: findStaleManagedSkillIds(skillsHome, activeIds),
  };

  mkdirSync(skillsHome, { recursive: true });
  const manifestIds = manifest.skills.map((skill) => skill.id).join(', ');
  const rootContent = renderSkillTemplate(rootTemplate, {
    project_dir: cwd,
    manifest_ids: manifestIds,
    marker: MANAGED_SKILL_MARKER,
  });
  writeFileSync(projectSkill, rootContent, 'utf8');

  for (const skill of manifest.skills) {
    const skillDir = path.join(skillsHome, skill.id);
    const skillPath = path.join(skillDir, 'SKILL.md');
    if (existsSync(skillPath) && !hasManagedMarker(skillPath)) {
      result.skipped.push(skill.id);
      continue;
    }
    mkdirSync(skillDir, { recursive: true });
    const content = renderSkillTemplate(internalTemplate, {
      ...skill,
      project_dir: cwd,
      marker: MANAGED_SKILL_MARKER,
    });
    writeFileSync(skillPath, content, 'utf8');
    result.installed.push(skill.id);
  }

  process.stdout.write(
    `paper-curation: installed=${formatList(result.installed)} skipped=${formatList(result.skipped)} stale=${formatList(result.stale)}\n`,
  );
  return result;
}
function readJsonConfig(configPath) {
  try {
    return JSON.parse(readFileSync(configPath, 'utf8'));
  } catch (error) {
    if (error instanceof SyntaxError) {
      throw new CliError(`Malformed config.json at ${configPath}: ${error.message}`);
    }
    throw error;
  }
}

export function listConfiguredTopics(cwd) {
  const configPath = path.join(cwd, 'config.json');
  if (!existsSync(configPath)) {
    throw new CliError(
      `No config.json found in ${cwd}. Run 'node ./bin/paper-curation.mjs setup --fresh-config' to choose Zotero collections, or pass --dir PATH for an existing checkout.`,
    );
  }

  const config = readJsonConfig(configPath);
  const collections = config?.zotero?.collections;
  if (!collections || typeof collections !== 'object' || Array.isArray(collections)) {
    throw new CliError(
      `No topic aliases found in ${configPath}. Configure zotero.collections with 'node ./bin/paper-curation.mjs setup --fresh-config'.`,
    );
  }

  const topics = Object.keys(collections).filter((topic) => topic.length > 0);
  if (!topics.length) {
    throw new CliError(
      `No topic aliases found in ${configPath}. Configure zotero.collections with 'node ./bin/paper-curation.mjs setup --fresh-config'.`,
    );
  }
  return topics;
}

function printConfiguredTopics(cwd, json = false) {
  const topics = listConfiguredTopics(cwd);
  if (json) {
    process.stdout.write(`${JSON.stringify({ topics, count: topics.length })}\n`);
    return topics;
  }

  process.stdout.write(`paper-curation: configured topic aliases (${topics.length})\n`);
  for (const topic of topics) {
    process.stdout.write(`- ${JSON.stringify(topic)}\n`);
  }
  process.stdout.write('Use one alias as --topic <alias>. Run setup --fresh-config to change selections.\n');
  return topics;
}



function requireCheckout(dir) {
  if (!isCheckout(dir)) {
    throw new CliError(`Not a paper-curation checkout: ${dir}. Run 'paper-curation init --dir ${dir}' first.`);
  }
}

function buildEnvironmentSetupSteps(cwd, auth, runFirst, configMode = 'prompt') {
  const setupArgs = ['pipeline/setup.py', '--anthropic-auth', auth, '--no-install'];
  if (configMode === 'fresh') setupArgs.push('--fresh-config');
  if (configMode === 'reuse') setupArgs.push('--reuse-config');
  const setupOptions = auth === 'oauth' ? { unsetEnv: OAUTH_UNSET_ENV } : {};
  const steps = [];
  if (auth === 'oauth') {
    steps.push(commandStep('claude', ['--version'], {
      cwd,
      stdio: 'pipe',
      unsetEnv: OAUTH_UNSET_ENV,
      minClaudeVersion: MIN_CLAUDE_VERSION,
    }));
    steps.push(commandStep('claude', ['auth', 'status'], {
      cwd,
      unsetEnv: OAUTH_UNSET_ENV,
    }));
    steps.push(commandStep('claude', ['auth', 'login'], {
      cwd,
      unsetEnv: OAUTH_UNSET_ENV,
      onlyIfPreviousFailed: true,
    }));
  }
  if (!runFirst) setupArgs.push('--no-run');
  steps.push(
    commandStep('conda', ['run', '-n', ENV_NAME, 'python', '--version'], { cwd, env: { PYTHONUTF8: '1' } }),
    commandStep('conda', ['create', '-n', ENV_NAME, '-c', 'conda-forge', 'python=3.12', 'pip', '-y'], { cwd, env: { PYTHONUTF8: '1' }, onlyIfPreviousFailed: true }),
    condaStep(cwd, [
      'python',
      '-c',
      "import sys; raise SystemExit(0 if sys.version_info[:2] == (3, 12) else 'The py312 environment must use Python 3.12')",
    ]),
  );
  const setupStep = condaStep(cwd, ['python', ...setupArgs], setupOptions);
  const dependencyStep = condaStep(
    cwd,
    ['python', '-m', 'pip', 'install', '-r', 'requirements.txt'],
  );
  if (runFirst) steps.push(dependencyStep, setupStep);
  else steps.push(setupStep, dependencyStep);
  return steps;
}

export function createPlan(argv, options = {}) {
  const cwd = path.resolve(options.cwd ?? process.cwd());
  const parsed = parseArgs(argv);
  const targetDir = resolveTargetDir(parsed, cwd);

  if (parsed.command === 'help') {
    return { parsed, targetDir, help: usage(), steps: [] };
  }

  if (parsed.command === 'init') {
    const steps = [];
    if (!isCheckout(targetDir)) {
      steps.push(commandStep('git', ['clone', REPO_URL, targetDir], { cwd }));
    }
    steps.push(skillInstallStep(targetDir));
    steps.push(...buildEnvironmentSetupSteps(
      targetDir,
      parsed.auth,
      parsed.runFirst,
      parsed.configMode,
    ));
    return { parsed, targetDir, steps };
  }

  if (parsed.command === 'setup') {
    if (options.validateCheckout !== false) requireCheckout(targetDir);
    return {
      parsed,
      targetDir,
      steps: [
        skillInstallStep(targetDir),
        ...buildEnvironmentSetupSteps(
          targetDir,
          parsed.auth,
          parsed.runFirst,
          parsed.configMode,
        ),
      ],
    };
  }

  if (parsed.command === 'skill') {
    if (options.validateCheckout !== false) requireCheckout(targetDir);
    if (parsed.forwarded[0] !== 'install') {
      throw new CliError("Unknown skill command. Expected 'skill install'.");
    }
    return { parsed, targetDir, steps: [skillInstallStep(targetDir)] };
  }

  if (parsed.command === 'doctor') {
    if (options.validateCheckout !== false) requireCheckout(targetDir);
    return { parsed, targetDir, steps: [condaStep(targetDir, ['python', 'pipeline/doctor.py', ...parsed.forwarded])] };
  }

  if (parsed.command === 'topic') {
    if (options.validateCheckout !== false) requireCheckout(targetDir);
    return { parsed, targetDir, readDotEnv: false, steps: [topicListStep(targetDir, parsed.json)] };
  }

  if (parsed.command === 'run') {
    if (options.validateCheckout !== false) requireCheckout(targetDir);
    return { parsed, targetDir, steps: [condaStep(targetDir, ['python', 'pipeline/run_full.py', ...parsed.forwarded])] };
  }

  if (parsed.command === 'auth') {
    const subcommand = parsed.forwarded[0];
    if (subcommand === 'status') {
      return { parsed, targetDir: cwd, steps: [commandStep('claude', ['auth', 'status'], { cwd, unsetEnv: OAUTH_UNSET_ENV })] };
    }
    if (subcommand === 'setup-token') {
      return { parsed, targetDir: cwd, steps: [commandStep('claude', ['setup-token'], { cwd, unsetEnv: OAUTH_UNSET_ENV })] };
    }
    throw new CliError("Unknown auth command. Expected 'auth status' or 'auth setup-token'.");
  }

  throw new CliError(`Unknown command: ${parsed.command}`);
}

function printable(step) {
  if (step.action === 'installSkill') return `install paper-curation skill from ${step.cwd}`;
  if (step.action === 'listTopics') return `list paper-curation topics from ${step.cwd}`;
  return [step.command, ...step.args].join(' ');
}

function spawnChecked(step, dotEnv = {}) {
  const env = { ...dotEnv, ...process.env, ...step.env };
  for (const name of step.unsetEnv ?? []) delete env[name];
  const result = spawnSync(step.command, step.args, {
    cwd: step.cwd,
    env,
    stdio: step.stdio,
    shell: false,
  });

  if (result.error) {
    throw new CliError(`Failed to start '${printable(step)}': ${result.error.message}`);
  }
  if (typeof result.status === 'number' && result.status !== 0) {
    throw new CliError(`Command failed (${result.status}): ${printable(step)}`, result.status);
  }
  if (result.signal) {
    throw new CliError(`Command terminated by signal ${result.signal}: ${printable(step)}`);
  }
  if (step.minClaudeVersion) {
    const output = `${result.stdout ?? ''}${result.stderr ?? ''}`.trim();
    if (output) process.stdout.write(`${output}\n`);
    const match = output.match(/(\d+)\.(\d+)\.(\d+)/);
    const installed = match?.slice(1, 4).map(Number);
    const required = step.minClaudeVersion;
    const tooOld = !installed || installed.some(
      (part, index) => part !== required[index]
        && required.slice(0, index).every((value, prior) => installed[prior] === value)
        && part < required[index],
    );
    if (tooOld) {
      throw new CliError(
        `Claude Code >= ${required.join('.')} is required for OAuth structured output. Run 'claude update'.`,
      );
    }
  }
  return result;
}

export function runPlan(plan, runner = spawnChecked) {
  for (let i = 0; i < plan.steps.length; i += 1) {
    const step = plan.steps[i];
    if (step.action === 'installSkill') {
      if (runner === spawnChecked) installSkill(step.cwd);
      else runner(step);
      continue;
    }
    if (step.action === 'listTopics') {
      if (runner === spawnChecked) printConfiguredTopics(step.cwd, step.json);
      else runner(step);
      continue;
    }
    if (step.onlyIfPreviousFailed) continue;
    try {
      runner(step);
    } catch (error) {
      const next = plan.steps[i + 1];
      if (next?.onlyIfPreviousFailed) {
        runner(next);
        i += 1;
        continue;
      }
      throw error;
    }
  }
}

export function main(argv = process.argv.slice(2)) {
  try {
    const plan = createPlan(argv);
    if (plan.help) {
      process.stdout.write(plan.help);
      return 0;
    }
    const dotEnv = plan.readDotEnv === false ? {} : loadDotEnv(plan.targetDir);
    runPlan(plan, (step) => {
      if (step.action === 'installSkill') installSkill(step.cwd);
      else if (step.action === 'listTopics') printConfiguredTopics(step.cwd, step.json);
      else spawnChecked(step, dotEnv);
    });
    return 0;
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    process.stderr.write(`paper-curation: ${message}\n`);
    return error instanceof CliError ? error.code : 1;
  }
}

const invokedPath = process.argv[1];
if (invokedPath) {
  try {
    if (realpathSync(invokedPath) === realpathSync(fileURLToPath(import.meta.url))) {
      process.exitCode = main();
    }
  } catch {
    // Imported modules and broken launch symlinks must not execute implicitly.
  }
}
