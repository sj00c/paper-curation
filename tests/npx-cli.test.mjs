import assert from 'node:assert/strict';
import { mkdtempSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import path from 'node:path';
import test from 'node:test';
import { createPlan, loadDotEnv, parseArgs } from '../bin/paper-curation.mjs';

const cwd = '/tmp/paper-cli-test';

function lastStep(plan) {
  return plan.steps.at(-1);
}

test('help is available without constructing commands', () => {
  const plan = createPlan(['--help'], { cwd, validateCheckout: false });
  assert.match(plan.help, /paper-curation init/);
  assert.match(plan.help, /paper-curation inspect/);
  assert.match(plan.help, /paper-curation deploy --topic TOPIC/);
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
  assert.deepEqual(plan.steps[1].args, ['--version']);
  assert.deepEqual(plan.steps[1].minClaudeVersion, [2, 1, 205]);
  assert.deepEqual(plan.steps[1].unsetEnv, ['ANTHROPIC_API_KEY', 'ANTHROPIC_AUTH_TOKEN']);
  assert.deepEqual(plan.steps[2].args, ['auth', 'status']);
  assert.deepEqual(plan.steps[3].args, ['run', '-n', 'py312', 'python', '--version']);
  assert.deepEqual(plan.steps[4].args, ['create', '-n', 'py312', '-c', 'conda-forge', 'python=3.12', 'pip', '-y']);
  assert.equal(plan.steps[4].onlyIfPreviousFailed, true);
  assert.deepEqual(plan.steps[5].args.slice(0, 6), ['run', '-n', 'py312', 'python', '-c', "import sys; raise SystemExit(0 if sys.version_info[:2] == (3, 12) else 'The py312 environment must use Python 3.12')"]);
  assert.deepEqual(plan.steps[6].args, ['run', '-n', 'py312', 'python', '-m', 'pip', 'install', '-r', 'requirements.txt']);
  assert.deepEqual(plan.steps[7].args, ['run', '-n', 'py312', 'python', '-m', 'pip', 'install', '-e', '.']);
  assert.deepEqual(lastStep(plan).args, [
    'run',
    '-n',
    'py312',
    'python',
    'pipeline/setup.py',
    '--anthropic-auth',
    'oauth',
  ]);
  assert.equal(lastStep(plan).env.PYTHONUTF8, '1');
  assert.deepEqual(lastStep(plan).unsetEnv, ['ANTHROPIC_API_KEY', 'ANTHROPIC_AUTH_TOKEN']);
});

test('setup supports --dir before command options and --run-first is explicit', () => {
  const plan = createPlan(['--dir=.', 'setup', '--auth=api-key', '--run-first'], {
    cwd,
    validateCheckout: false,
  });

  assert.equal(plan.targetDir, cwd);
  assert.deepEqual(plan.steps.at(-2).args, [
    'run', '-n', 'py312', 'python', '-m', 'pip', 'install', '-e', '.',
  ]);
  assert.deepEqual(lastStep(plan).args, [
    'run',
    '-n',
    'py312',
    'python',
    'pipeline/setup.py',
    '--anthropic-auth',
    'api-key',
    '--run-first',
  ]);
  assert.equal(lastStep(plan).unsetEnv, undefined);
});

test('doctor delegates flags through conda run in the selected checkout', () => {
  const plan = createPlan(['doctor', '--dir', '.', '--network', '--topic', 'robotics'], {
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
  ]);
  assert.equal(plan.steps[0].env.PYTHONUTF8, '1');
});

test('inspect delegates to the read-only Python inspector in the selected checkout', () => {
  const plan = createPlan(['inspect', '--dir', '.'], {
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
    'pipeline/inspect_installation.py',
  ]);
  assert.equal(plan.steps[0].env.PYTHONUTF8, '1');
});

test('run forwards only arguments after -- without treating --help as CLI help', () => {
  const plan = createPlan(['run', '--dir', '.', '--', '--help', '--topic', 'x'], {
    cwd,
    validateCheckout: false,
  });

  assert.equal(plan.help, undefined);
  assert.deepEqual(plan.parsed.forwarded, ['--help', '--topic', 'x']);
  assert.deepEqual(plan.steps[0].args, [
    'run',
    '-n',
    'py312',
    'python',
    'pipeline/run_full.py',
    '--help',
    '--topic',
    'x',
  ]);
});

test('friendly workflow commands use the authoritative Python module CLI', () => {
  const cases = [
    {
      argv: ['build', '--topic', 'example-topic'],
      expected: ['python', '-m', 'paper_curation.cli', 'build', '--topic', 'example-topic'],
    },
    {
      argv: ['update', '--topic', 'example-topic'],
      expected: ['python', '-m', 'paper_curation.cli', 'update', '--topic', 'example-topic'],
    },
    {
      argv: ['serve', '--topic', 'example-topic', '--port', '8123'],
      expected: ['python', '-m', 'paper_curation.cli', 'serve', '--topic', 'example-topic', '--', '--port', '8123'],
    },
    {
      argv: ['query', '--topic', 'example-topic', '--query', 'test query', '--top-k', '3'],
      expected: ['python', '-m', 'paper_curation.cli', 'query', '--topic', 'example-topic', '--query', 'test query', '--', '--top-k', '3'],
    },
    {
      argv: ['validate', '--topic', 'example-topic'],
      expected: ['python', '-m', 'paper_curation.cli', 'validate', '--topic', 'example-topic'],
    },
    {
      argv: ['repair', '--topic', 'example-topic'],
      expected: ['python', '-m', 'paper_curation.cli', 'repair', '--topic', 'example-topic'],
    },
    {
      argv: ['deploy', '--topic', 'example-topic'],
      expected: ['python', '-m', 'paper_curation.cli', 'deploy', '--topic', 'example-topic'],
    },
  ];

  for (const { argv, expected } of cases) {
    const plan = createPlan(argv, { cwd, validateCheckout: false });
    assert.deepEqual(plan.steps[0].args, ['run', '-n', 'py312', ...expected], argv.join(' '));
    assert.equal(plan.steps[0].args.includes('pipeline'), false, argv.join(' '));
  }
});

test('topic-bound friendly commands reject missing topics', () => {
  for (const command of ['build', 'update', 'query', 'validate', 'repair', 'deploy']) {
    assert.throws(
      () => createPlan([command], { cwd, validateCheckout: false }),
      new RegExp(`${command} requires --topic TOPIC`),
    );
  }
});

test('query requires an explicit query in addition to its topic', () => {
  assert.throws(
    () => createPlan(['query', '--topic', 'example-topic'], { cwd, validateCheckout: false }),
    /query requires --query QUERY/,
  );
});

test('repair remains a preview until --execute is explicitly provided', () => {
  const preview = createPlan(['repair', '--topic', 'example-topic'], { cwd, validateCheckout: false });
  const execute = createPlan(['repair', '--topic', 'example-topic', '--execute'], {
    cwd,
    validateCheckout: false,
  });

  assert.deepEqual(preview.steps[0].args, [
    'run', '-n', 'py312', 'python', '-m', 'paper_curation.cli', 'repair', '--topic', 'example-topic',
  ]);
  assert.deepEqual(execute.steps[0].args, [
    'run', '-n', 'py312', 'python', '-m', 'paper_curation.cli', 'repair', '--topic', 'example-topic', '--execute',
  ]);
  assert.throws(() => parseArgs(['build', '--execute']), /only supported by repair/);
});

test('deploy stays separate from build and update plans', () => {
  const deploy = createPlan(['deploy', '--topic', 'example-topic'], { cwd, validateCheckout: false });
  const commandArgs = deploy.steps[0].args;

  assert.deepEqual(commandArgs, [
    'run', '-n', 'py312', 'python', '-m', 'paper_curation.cli', 'deploy', '--topic', 'example-topic',
  ]);
  assert.equal(commandArgs.includes('build'), false);
  assert.equal(commandArgs.includes('update'), false);
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
