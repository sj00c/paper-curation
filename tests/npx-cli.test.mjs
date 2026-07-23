import assert from 'node:assert/strict';
import {
  mkdirSync,
  mkdtempSync,
  readFileSync,
  rmSync,
  writeFileSync,
} from 'node:fs';
import { tmpdir } from 'node:os';
import path from 'node:path';
import test from 'node:test';
import {
  createPlan,
  installSkill,
  loadDotEnv,
  listConfiguredTopics,
  parseArgs,
  runPlan,
} from '../bin/paper-curation.mjs';

const cwd = '/tmp/paper-cli-test';
const packageJson = JSON.parse(readFileSync(new URL('../package.json', import.meta.url), 'utf8'));


function lastStep(plan) {
  return plan.steps.at(-1);
}

function pythonSetupStep(plan) {
  return plan.steps.find((step) => step.args?.includes('pipeline/setup.py'));
}

const expectedManagedSkillIds = [
  'paper-curation',
  'paper-curation-router',
  'paper-curation-setup',
  'paper-curation-doctor',
  'paper-curation-topic',
  'paper-curation-search-register',
  'paper-curation-curate-review',
  'paper-curation-smoke',
  'paper-curation-deploy',
];

function makeSkillCheckout() {
  const root = mkdtempSync(path.join(tmpdir(), 'paper-curation-skill-'));
  mkdirSync(path.join(root, '.git'));
  mkdirSync(path.join(root, 'pipeline'));
  mkdirSync(path.join(root, 'skills'));
  writeFileSync(path.join(root, 'pipeline', 'setup.py'), '');
  for (const relativePath of [
    'SKILL.md.template',
    path.join('skills', 'manifest.json'),
    path.join('skills', 'SKILL.md.template'),
  ]) {
    writeFileSync(
      path.join(root, relativePath),
      readFileSync(new URL(`../${relativePath}`, import.meta.url), 'utf8'),
    );
  }
  return root;
}

const skillTargetSegments = {
  claude: ['.claude', 'skills'],
  codex: ['.codex', 'skills'],
  gjc: ['.gjc', 'agent', 'skills'],
};

function installedSkillPath(home, target, id) {
  return path.join(home, ...skillTargetSegments[target], id, 'SKILL.md');
}

test('package stays bootstrap-only while version is unpublished 0.0.0', () => {
  assert.equal(packageJson.name, 'paper-curation');
  assert.equal(packageJson.version, '0.0.0');
  assert.deepEqual(packageJson.bin, { 'paper-curation': './bin/paper-curation.mjs' });
  assert.deepEqual(packageJson.files, ['bin']);
  assert.deepEqual(packageJson.engines, { node: '>=18' });
  assert.deepEqual(packageJson.dependencies, {});
  assert.equal(packageJson.devDependencies, undefined);
  assert.equal(packageJson.optionalDependencies, undefined);
  assert.equal(packageJson.peerDependencies, undefined);
  for (const script of ['preinstall', 'install', 'postinstall', 'prepare', 'prepublishOnly']) {
    assert.equal(packageJson.scripts?.[script], undefined);
  }
  assert.doesNotMatch(packageJson.description, /\bnpx\b/i);
});

test('help is checkout-local and pins the current first-run and smoke journey', () => {
  const plan = createPlan(['--help'], { cwd, validateCheckout: false });
  assert.match(plan.help, /node \.\/bin\/paper-curation\.mjs skill install/);
  assert.match(plan.help, /node \.\/bin\/paper-curation\.mjs setup --fresh-config/);
  assert.doesNotMatch(plan.help, /setup --auth oauth --run-first/);
  assert.match(plan.help, /doctor --network --anthropic-smoke/);
  assert.match(plan.help, /node \.\/bin\/paper-curation\.mjs topic \[--dir PATH\] \[--json\]/);
  assert.match(plan.help, /--topic <configured-topic> --mode smoke --source zotero --smoke-limit 1 --strict-pdf --no-deploy/);
  assert.doesNotMatch(plan.help, /\bnpx\b/i);
  assert.doesNotMatch(plan.help, /github:/i);
  assert.deepEqual(plan.steps, []);
});

test('dotenv template values parse without exposing blank or comment entries', () => {
  const dir = mkdtempSync(path.join(tmpdir(), 'paper-curation-env-'));
  try {
    writeFileSync(
      path.join(dir, '.env'),
      [
        '# local credentials',
        'ZOTERO_API_KEY="zotero-test"',
        'ZOTERO_TOPIC_ALIAS=robotics # inline note',
        'OPENAI_API_KEY=',
        'export ZOTERO_DIR=/tmp/papers',
        'NOT VALID',
      ].join('\n'),
    );
    assert.deepEqual(loadDotEnv(dir), {
      ZOTERO_API_KEY: 'zotero-test',
      ZOTERO_TOPIC_ALIAS: 'robotics',
      ZOTERO_DIR: '/tmp/papers',
    });
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test('init accepts --dir after command options and constructs dry onboarding flow', () => {
  const plan = createPlan(['init', '--auth', 'oauth', '--dir', 'paper-curation'], { cwd });

  assert.equal(plan.targetDir, '/tmp/paper-cli-test/paper-curation');
  assert.equal(plan.steps[0].command, 'git');
  assert.deepEqual(plan.steps[0].args, [
    'clone',
    'https://github.com/jehyunlee/paper-curation.git',
    '/tmp/paper-cli-test/paper-curation',
  ]);
  assert.deepEqual(plan.steps[1], {
    action: 'installSkill',
    cwd: '/tmp/paper-cli-test/paper-curation',
  });
  assert.deepEqual(plan.steps[2].args, ['--version']);
  assert.deepEqual(plan.steps[2].minClaudeVersion, [2, 1, 205]);
  assert.deepEqual(plan.steps[2].unsetEnv, ['ANTHROPIC_API_KEY', 'ANTHROPIC_AUTH_TOKEN']);
  assert.deepEqual(plan.steps[3].args, ['auth', 'status']);
  assert.deepEqual(plan.steps[4].args, ['auth', 'login']);
  assert.equal(plan.steps[4].onlyIfPreviousFailed, true);
  assert.deepEqual(plan.steps[5].args, ['run', '-n', 'py312', 'python', '--version']);
  assert.deepEqual(plan.steps[6].args, ['create', '-n', 'py312', '-c', 'conda-forge', 'python=3.12', 'pip', '-y']);
  assert.equal(plan.steps[6].onlyIfPreviousFailed, true);
  assert.deepEqual(plan.steps[7].args.slice(0, 6), ['run', '-n', 'py312', 'python', '-c', "import sys; raise SystemExit(0 if sys.version_info[:2] == (3, 12) else 'The py312 environment must use Python 3.12')"]);
  assert.deepEqual(plan.steps[8].args, [
    'run',
    '-n',
    'py312',
    'python',
    'pipeline/setup.py',
    '--anthropic-auth',
    'oauth',
    '--no-install',
    '--no-run',
  ]);
  assert.deepEqual(plan.steps[9].args, ['run', '-n', 'py312', 'python', '-m', 'pip', 'install', '-r', 'requirements.txt']);
  assert.equal(pythonSetupStep(plan).env.PYTHONUTF8, '1');
  assert.deepEqual(pythonSetupStep(plan).unsetEnv, ['ANTHROPIC_API_KEY', 'ANTHROPIC_AUTH_TOKEN']);
});

test('OAuth setup opens login only when auth status fails', () => {
  const plan = createPlan(['setup', '--auth', 'oauth'], {
    cwd,
    validateCheckout: false,
  });
  const calls = [];
  runPlan(plan, (step) => {
    if (step.action) {
      calls.push(step.action);
      return;
    }
    calls.push(step.args.join(' '));
    if (step.args.join(' ') === 'auth status') throw new Error('not logged in');
  });

  assert.deepEqual(calls.slice(1, 4), ['--version', 'auth status', 'auth login']);
  assert.equal(calls.includes('auth login'), true);

  const authenticatedCalls = [];
  runPlan(plan, (step) => authenticatedCalls.push(step.action ?? step.args.join(' ')));
  assert.equal(authenticatedCalls.includes('auth login'), false);
});

test('setup supports --dir before command options and --run-first removes --no-run', () => {
  const plan = createPlan(['--dir=.', 'setup', '--auth=api-key', '--run-first'], {
    cwd,
    validateCheckout: false,
  });

  assert.equal(plan.targetDir, cwd);
  assert.deepEqual(pythonSetupStep(plan).args, [
    'run',
    '-n',
    'py312',
    'python',
    'pipeline/setup.py',
    '--anthropic-auth',
    'api-key',
    '--no-install',
  ]);
  assert.equal(lastStep(plan).unsetEnv, undefined);
});

test('fresh config is explicit and conflicting config modes fail', () => {
  const plan = createPlan(['setup', '--fresh-config'], {
    cwd,
    validateCheckout: false,
  });
  assert.equal(plan.parsed.auth, 'auto');
  assert.equal(plan.parsed.configMode, 'fresh');
  assert.equal(plan.steps[0].action, 'installSkill');
  assert.deepEqual(pythonSetupStep(plan).args.slice(-2), ['--fresh-config', '--no-run']);
  assert.throws(
    () => parseArgs(['setup', '--fresh-config', '--reuse-config']),
    /mutually exclusive/,
  );
});

test('topic command is dependency-free read-only and fails closed without config', () => {
  const dir = mkdtempSync(path.join(tmpdir(), 'paper-curation-topic-'));
  try {
    mkdirSync(path.join(dir, '.git'));
    mkdirSync(path.join(dir, 'pipeline'));
    writeFileSync(path.join(dir, 'pipeline', 'setup.py'), '');

    const plan = createPlan(['topic', '--dir', dir], { cwd });
    assert.equal(plan.readDotEnv, false);
    assert.deepEqual(plan.steps, [{ action: 'listTopics', cwd: dir, json: false }]);
    assert.throws(
      () => listConfiguredTopics(dir),
      /No config\.json found.*setup --fresh-config/,
    );
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test('topic command lists arbitrary aliases without exposing collection values or secrets', () => {
  const dir = mkdtempSync(path.join(tmpdir(), 'paper-curation-topic-'));
  try {
    mkdirSync(path.join(dir, '.git'));
    mkdirSync(path.join(dir, 'pipeline'));
    writeFileSync(path.join(dir, 'pipeline', 'setup.py'), '');
    writeFileSync(
      path.join(dir, 'config.json'),
      JSON.stringify({
        zotero: {
          api_key: 'zotero-secret',
          collections: {
            'robotics-lab': 'Collection Name',
            '사용자 주제': 'SECRET_COLLECTION_VALUE',
          },
        },
        anthropic: { api_key: 'anthropic-secret' },
      }),
    );

    const plan = createPlan(['topic', 'list', '--json', '--dir', dir], { cwd });
    const calls = [];
    runPlan(plan, (step) => calls.push(step));
    assert.deepEqual(calls, [{ action: 'listTopics', cwd: dir, json: true }]);
    assert.deepEqual(listConfiguredTopics(dir), ['robotics-lab', '사용자 주제']);

    const scanned = JSON.stringify({ topics: listConfiguredTopics(dir), count: 2 });
    assert.match(scanned, /robotics-lab/);
    assert.match(scanned, /사용자 주제/);
    assert.doesNotMatch(scanned, /Collection Name|SECRET_COLLECTION_VALUE|zotero-secret|anthropic-secret/);
    assert.equal(plan.steps.some((step) => step.args?.includes('pipeline/setup.py')), false);
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test('dependency-free skill installer renders the managed manifest into deterministic destinations', () => {
  const root = makeSkillCheckout();
  const home = mkdtempSync(path.join(tmpdir(), 'paper-curation-home-'));
  try {
    const result = installSkill(root, home);

    assert.deepEqual(result.installed, expectedManagedSkillIds);
    assert.deepEqual(result.skipped, []);
    assert.deepEqual(result.stale, []);

    const rootSkill = readFileSync(path.join(root, 'SKILL.md'), 'utf8');
    assert.match(rootSkill, /paper-curation-managed-skill/);
    assert.match(rootSkill, new RegExp(root.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')));
    for (const target of Object.keys(skillTargetSegments)) {
      assert.deepEqual(result.targets[target].installed, expectedManagedSkillIds);
      assert.deepEqual(result.targets[target].skipped, []);
      assert.deepEqual(result.targets[target].stale, []);
      for (const id of expectedManagedSkillIds) {
        const installed = readFileSync(installedSkillPath(home, target, id), 'utf8');
        assert.match(installed, new RegExp(`Managed id: \`${id}\``));
        assert.match(installed, new RegExp(root.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')));
        assert.match(installed, /node \.\/bin\/paper-curation\.mjs/);
      }
      const topicSkill = readFileSync(installedSkillPath(home, target, 'paper-curation-topic'), 'utf8');
      assert.match(topicSkill, /node \.\/bin\/paper-curation\.mjs topic/);
      assert.doesNotMatch(topicSkill, /setup --reuse-config/);
      assert.match(readFileSync(installedSkillPath(home, target, 'paper-curation-deploy'), 'utf8'), /--mode deploy/);
      assert.match(readFileSync(installedSkillPath(home, target, 'paper-curation-smoke'), 'utf8'), /PAPER_CURATION_NO_DEPLOY=1/);
      assert.match(readFileSync(installedSkillPath(home, target, 'paper-curation-smoke'), 'utf8'), /--no-deploy/);
    }
  } finally {
    rmSync(root, { recursive: true, force: true });
    rmSync(home, { recursive: true, force: true });
  }
});

test('managed skill installer is idempotent and refuses unmanaged collisions', () => {
  const root = makeSkillCheckout();
  const home = mkdtempSync(path.join(tmpdir(), 'paper-curation-home-'));
  try {
    const unmanagedPath = installedSkillPath(home, 'claude', 'paper-curation-doctor');
    mkdirSync(path.dirname(unmanagedPath), { recursive: true });
    writeFileSync(unmanagedPath, 'user-owned doctor skill\n');

    const first = installSkill(root, home);
    const second = installSkill(root, home);

    assert.equal(readFileSync(unmanagedPath, 'utf8'), 'user-owned doctor skill\n');
    assert.deepEqual(first.skipped, ['paper-curation-doctor']);
    assert.deepEqual(second.skipped, ['paper-curation-doctor']);
    assert.deepEqual(second.targets.claude.skipped, ['paper-curation-doctor']);
    assert.deepEqual(second.targets.claude.installed, expectedManagedSkillIds.filter((id) => id !== 'paper-curation-doctor'));
    assert.deepEqual(second.targets.codex.installed, expectedManagedSkillIds);
    assert.deepEqual(second.targets.gjc.installed, expectedManagedSkillIds);
  } finally {
    rmSync(root, { recursive: true, force: true });
    rmSync(home, { recursive: true, force: true });
  }
});

test('managed skill installer reports stale managed ids without deleting them', () => {
  const root = makeSkillCheckout();
  const home = mkdtempSync(path.join(tmpdir(), 'paper-curation-home-'));
  try {
    const stalePath = installedSkillPath(home, 'claude', 'paper-curation-old');
    mkdirSync(path.dirname(stalePath), { recursive: true });
    writeFileSync(stalePath, '<!-- paper-curation-managed-skill -->\nold\n');

    const result = installSkill(root, home);

    assert.deepEqual(result.stale, ['paper-curation-old']);
    assert.deepEqual(result.targets.claude.stale, ['paper-curation-old']);
    assert.deepEqual(result.targets.codex.stale, []);
    assert.deepEqual(result.targets.gjc.stale, []);
    assert.equal(readFileSync(stalePath, 'utf8'), '<!-- paper-curation-managed-skill -->\nold\n');
  } finally {
    rmSync(root, { recursive: true, force: true });
    rmSync(home, { recursive: true, force: true });
  }
});

test('managed skill templates stay harness-only and package stays dependency-free', () => {
  const scanned = [
    readFileSync(new URL('../SKILL.md.template', import.meta.url), 'utf8'),
    readFileSync(new URL('../skills/SKILL.md.template', import.meta.url), 'utf8'),
    readFileSync(new URL('../skills/manifest.json', import.meta.url), 'utf8'),
  ].join('\n');

  assert.doesNotMatch(scanned, /Agent\(/);
  assert.doesNotMatch(scanned, /python pipeline\//);
  assert.doesNotMatch(scanned, /\bai4s\b/i);
  assert.doesNotMatch(scanned, /\bscisci\b/i);
  assert.doesNotMatch(scanned, /setup --reuse-config/);
  assert.equal((scanned.match(/node \.\/bin\/paper-curation\.mjs/g) ?? []).length >= expectedManagedSkillIds.length, true);
  assert.deepEqual(packageJson.dependencies, {});
  assert.equal(packageJson.devDependencies, undefined);
  assert.equal(packageJson.optionalDependencies, undefined);
  assert.equal(packageJson.peerDependencies, undefined);
});

test('doctor delegates smoke flags through conda run in the selected checkout', () => {
  const plan = createPlan(['doctor', '--dir', '.', '--network', '--topic', 'robotics', '--anthropic-smoke'], {
    cwd,
    validateCheckout: false,
  });

  assert.equal(plan.steps.length, 1);
  assert.equal(plan.steps[0].command, 'conda');
  assert.equal(plan.steps[0].cwd, cwd);
  assert.deepEqual(plan.steps[0].args, [
    'run',
    '-n',
    'py312',
    'python',
    'pipeline/doctor.py',
    '--network',
    '--topic',
    'robotics',
    '--anthropic-smoke',
  ]);
  assert.equal(plan.steps[0].env.PYTHONUTF8, '1');
});

test('run transparently forwards smoke and no-deploy args only after --', () => {
  const plan = createPlan(['run', '--dir', '.', '--', '--mode', 'smoke', '--smoke-limit', '3', '--no-deploy'], {
    cwd,
    validateCheckout: false,
  });

  assert.equal(plan.help, undefined);
  assert.deepEqual(plan.parsed.forwarded, ['--mode', 'smoke', '--smoke-limit', '3', '--no-deploy']);
  assert.deepEqual(plan.steps[0].args, [
    'run',
    '-n',
    'py312',
    'python',
    'pipeline/run_full.py',
    '--mode',
    'smoke',
    '--smoke-limit',
    '3',
    '--no-deploy',
  ]);
  assert.throws(
    () => createPlan(['run', '--mode', 'smoke'], { cwd, validateCheckout: false }),
    /Unknown option: --mode/,
  );
});

test('auth commands delegate to Claude without checkout validation or secret arguments', () => {
  assert.deepEqual(parseArgs(['auth', 'status']).forwarded, ['status']);

  const status = createPlan(['auth', 'status'], { cwd });
  assert.deepEqual(status.steps[0].args, ['auth', 'status']);
  assert.equal(status.steps[0].stdio, 'inherit');
  assert.deepEqual(status.steps[0].unsetEnv, ['ANTHROPIC_API_KEY', 'ANTHROPIC_AUTH_TOKEN']);

  const setupToken = createPlan(['auth', 'setup-token'], { cwd });
  assert.deepEqual(setupToken.steps[0].args, ['setup-token']);
  assert.equal(setupToken.steps[0].stdio, 'inherit');
  assert.deepEqual(setupToken.steps[0].unsetEnv, ['ANTHROPIC_API_KEY', 'ANTHROPIC_AUTH_TOKEN']);
});

test('invalid auth modes produce a clear error', () => {
  assert.throws(
    () => parseArgs(['init', '--auth', 'token']),
    /Invalid --auth value 'token'/,
  );
});
