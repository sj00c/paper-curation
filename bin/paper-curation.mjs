#!/usr/bin/env node
import { spawnSync } from 'node:child_process';
import { existsSync, readFileSync, realpathSync } from 'node:fs';
import path from 'node:path';
import process from 'node:process';
import { fileURLToPath } from 'node:url';

const REPO_URL = 'https://github.com/jehyunlee/paper-curation.git';
const ENV_NAME = 'py312';
const VALID_AUTH = new Set(['auto', 'oauth', 'api-key']);
const OAUTH_UNSET_ENV = ['ANTHROPIC_API_KEY', 'ANTHROPIC_AUTH_TOKEN'];
const MIN_CLAUDE_VERSION = [2, 1, 205];

class CliError extends Error {
  constructor(message, code = 1) {
    super(message);
    this.name = 'CliError';
    this.code = code;
  }
}

function usage() {
  return `paper-curation: dependency-free onboarding for paper-curation

Usage:
  paper-curation init [--dir PATH] [--auth auto|oauth|api-key] [--run-first]
  paper-curation setup [--dir PATH] [--auth auto|oauth|api-key] [--run-first]
  paper-curation doctor [--dir PATH] [--network] [--topic TOPIC]
  paper-curation run [--dir PATH] -- [run_full.py args...]
  paper-curation auth status
  paper-curation auth setup-token
  paper-curation help

Defaults:
  --dir paper-curation for init, current directory for other commands.
  --auth auto.
  setup/init pass --no-run to Python setup unless --run-first is present.

Getting started in an existing checkout:
  paper-curation setup --auth oauth

  Setup creates the untracked local config.json, validates the Zotero key, lists
  collections for selection, and creates pdf_cache automatically. Export alone
  never creates config.json. Copy .env.example to .env to paste the two required
  keys (Zotero and Gemini) into one editable file.
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
    return { command: 'help', dir: null, auth: 'auto', runFirst: false, forwarded: [] };
  }

  let command = null;
  let dir = null;
  let auth = 'auto';
  let runFirst = false;
  let forwarded = [];

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

    if (token.startsWith('--')) {
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

    if (command === 'auth' && !forwarded.length) {
      forwarded.push(token);
      continue;
    }
    if (command === 'doctor') {
      forwarded.push(token);
      continue;
    }

    throw new CliError(`Unexpected argument: ${token}`);
  }

  if (!command) command = 'help';
  if (!VALID_AUTH.has(auth)) {
    throw new CliError(`Invalid --auth value '${auth}'. Expected auto, oauth, or api-key.`);
  }

  return { command, dir, auth, runFirst, forwarded };
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


function requireCheckout(dir) {
  if (!isCheckout(dir)) {
    throw new CliError(`Not a paper-curation checkout: ${dir}. Run 'paper-curation init --dir ${dir}' first.`);
  }
}

function buildEnvironmentSetupSteps(cwd, auth, runFirst) {
  const setupArgs = ['pipeline/setup.py', '--anthropic-auth', auth];
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
    condaStep(cwd, ['python', '-m', 'pip', 'install', '-r', 'requirements.txt']),
    condaStep(cwd, ['python', ...setupArgs], setupOptions),
  );
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
    steps.push(...buildEnvironmentSetupSteps(targetDir, parsed.auth, parsed.runFirst));
    return { parsed, targetDir, steps };
  }

  if (parsed.command === 'setup') {
    if (options.validateCheckout !== false) requireCheckout(targetDir);
    return { parsed, targetDir, steps: buildEnvironmentSetupSteps(targetDir, parsed.auth, parsed.runFirst) };
  }

  if (parsed.command === 'doctor') {
    if (options.validateCheckout !== false) requireCheckout(targetDir);
    return { parsed, targetDir, steps: [condaStep(targetDir, ['python', 'pipeline/doctor.py', ...parsed.forwarded])] };
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
    const dotEnv = loadDotEnv(plan.targetDir);
    runPlan(plan, (step) => spawnChecked(step, dotEnv));
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
