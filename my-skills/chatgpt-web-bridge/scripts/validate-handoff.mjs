#!/usr/bin/env node

import { createHash } from 'node:crypto';
import { readFile, readdir, stat } from 'node:fs/promises';
import { join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const PACKET_SECTIONS = [
  '## Objective',
  '## Acceptance',
  '## Task State',
  '## Evidence',
  '## Constraints',
  '## Questions',
];

const RESULT_SECTIONS = [
  '## Verdict',
  '## Assumptions',
  '## Evidence Used',
  '## Proposed Changes',
  '## Tests',
  '## Risks',
  '## Unknowns',
];

const IMAGE_TASK_SECTIONS = [
  '## Prompt',
  '## Save Location',
  '## Acceptance',
];

const SECRET_PATTERNS = [
  /-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----/i,
  /\bAKIA[0-9A-Z]{16}\b/,
  /\bgh[pousr]_[A-Za-z0-9]{20,}\b/,
  /\bsk-[A-Za-z0-9_-]{20,}\b/,
  /\b(?:api[_-]?key|access[_-]?token|client[_-]?secret|password)\s*[:=]\s*(?!\[REDACTED\])\S+/i,
];

const MODEL_STATUSES = new Set(['verified', 'unverified']);
const CHECK_STATUSES = new Set(['passed', 'failed', 'not_run']);
const LOCAL_CHANGE_STATUSES = new Set(['applied', 'no_changes_needed', 'failed', 'not_run']);
const PRIVACY_FIELDS = [
  'scope_minimized',
  'credentials_scan_passed',
  'semantic_privacy_reviewed',
  'raw_diff_excluded',
  'unrelated_files_excluded',
];
const TASK_TYPES = new Set(['reasoning', 'image']);
const TRANSPORTS = new Set(['codex-in-app-browser', 'user-chrome', 'host-browser-use']);
const IMAGE_FORMATS = new Set(['png', 'jpeg', 'webp', 'gif']);

export function estimateTokens(text) {
  const cjk = (text.match(/[\u3400-\u9fff\uf900-\ufaff]/g) ?? []).length;
  const nonCjk = text.replace(/[\u3400-\u9fff\uf900-\ufaff]/g, '');
  return cjk + Math.ceil(nonCjk.length / 4);
}

export function sha256Text(text) {
  return createHash('sha256').update(text, 'utf8').digest('hex');
}

export function sha256Buffer(buffer) {
  return createHash('sha256').update(buffer).digest('hex');
}

export function detectImageFormat(buffer) {
  if (buffer.length >= 8 && buffer.subarray(0, 8).equals(Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]))) {
    return 'png';
  }
  if (buffer.length >= 3 && buffer[0] === 0xff && buffer[1] === 0xd8 && buffer[2] === 0xff) {
    return 'jpeg';
  }
  if (buffer.length >= 6 && buffer.subarray(0, 6).toString('ascii').startsWith('GIF8')) {
    return 'gif';
  }
  if (buffer.length >= 12 && buffer.subarray(0, 4).toString('ascii') === 'RIFF'
    && buffer.subarray(8, 12).toString('ascii') === 'WEBP') {
    return 'webp';
  }
  return null;
}

function normalizeText(text) {
  return text.replace(/\r\n?/g, '\n');
}

function exactLineCount(lines, value) {
  return lines.filter((line) => line.trim() === value).length;
}

function validateContract(text, { start, end, sections, idField }) {
  const errors = [];
  const normalized = normalizeText(text);
  const lines = normalized.trim().split('\n');
  const openingCount = exactLineCount(lines, start);
  const closingCount = exactLineCount(lines, end);
  if (openingCount !== 1) errors.push(`opening marker must appear exactly once: ${start}`);
  if (closingCount !== 1) errors.push(`closing marker must appear exactly once: ${end}`);
  if (lines[0]?.trim() !== start || lines.at(-1)?.trim() !== end) {
    errors.push('non-empty text exists outside the contract markers');
  }

  const idPattern = new RegExp(`^${idField}:\\s*\\S+\\s*$`);
  const idCount = lines.filter((line) => idPattern.test(line)).length;
  if (idCount !== 1) errors.push(`${idField} must appear exactly once`);

  let previous = -1;
  for (const section of sections) {
    const count = exactLineCount(lines, section);
    const index = lines.findIndex((line) => line.trim() === section);
    if (count === 0) errors.push(`missing required section: ${section}`);
    else if (count > 1) errors.push(`required section must appear exactly once: ${section}`);
    else if (index < previous) errors.push(`section out of order: ${section}`);
    previous = Math.max(previous, index);
  }
  return errors;
}

function scanSecrets(text, label) {
  if (SECRET_PATTERNS.some((pattern) => pattern.test(text))) {
    return [`${label} contains a likely secret; redact it before browser transmission`];
  }
  return [];
}

export function validatePacket(text) {
  const errors = validateContract(text, {
    start: 'BEGIN_CONTEXT_PACKET',
    end: 'END_CONTEXT_PACKET',
    sections: PACKET_SECTIONS,
    idField: 'packet_id',
  });
  const reasonerCount = normalizeText(text)
    .split('\n')
    .filter((line) => /^requested_reasoner:\s*\S.+$/.test(line)).length;
  if (reasonerCount !== 1) errors.push('requested_reasoner must appear exactly once');
  const tokens = estimateTokens(text);
  if (tokens > 3000) errors.push(`packet exceeds 3000 approximate tokens: ${tokens}`);
  errors.push(...scanSecrets(text, 'packet'));
  return errors;
}

export function validateResult(text) {
  const errors = validateContract(text, {
    start: 'BEGIN_REASONING_RESULT',
    end: 'END_REASONING_RESULT',
    sections: RESULT_SECTIONS,
    idField: 'packet_id',
  });
  errors.push(...scanSecrets(text, 'result'));
  return errors;
}

export function validateImageTask(text) {
  const errors = validateContract(text, {
    start: 'BEGIN_IMAGE_TASK',
    end: 'END_IMAGE_TASK',
    sections: IMAGE_TASK_SECTIONS,
    idField: 'task_id',
  });
  const lines = normalizeText(text).split('\n');
  const modelCount = lines.filter((line) => /^requested_model:\s*\S.+$/.test(line)).length;
  if (modelCount !== 1) errors.push('requested_model must appear exactly once');
  const countLines = lines.filter((line) => /^count:\s*\d+\s*$/.test(line));
  if (countLines.length !== 1) errors.push('count must appear exactly once as a positive integer');
  else if (Number.parseInt(countLines[0].replace(/^count:\s*/, ''), 10) < 1) {
    errors.push('count must be at least 1');
  }
  const tokens = estimateTokens(text);
  if (tokens > 1000) errors.push(`image task exceeds 1000 approximate tokens: ${tokens}`);
  errors.push(...scanSecrets(text, 'image task'));
  return errors;
}

function contractId(text, idField) {
  return text.match(new RegExp(`^${idField}:\\s*(\\S+)`, 'm'))?.[1];
}

export function validatePair(packet, result) {
  const errors = [
    ...validatePacket(packet).map((error) => `packet: ${error}`),
    ...validateResult(result).map((error) => `result: ${error}`),
  ];
  const sentId = contractId(packet, 'packet_id');
  const returnedId = contractId(result, 'packet_id');
  if (sentId && returnedId && sentId !== returnedId) {
    errors.push(`packet_id mismatch: sent ${sentId}, returned ${returnedId}`);
  }
  return errors;
}

export async function scanImagesDir(directory, { count, minBytes = 1024 } = {}) {
  const errors = [];
  const images = [];
  let entries;
  try {
    entries = (await readdir(resolve(directory), { withFileTypes: true }))
      .filter((entry) => entry.isFile());
  } catch (error) {
    return { errors: [`images directory cannot be read: ${error.message}`], images };
  }
  if (entries.length === 0) errors.push('images directory is empty');
  for (const entry of entries) {
    const path = join(resolve(directory), entry.name);
    const buffer = await readFile(path);
    const format = detectImageFormat(buffer);
    const sha256 = sha256Buffer(buffer);
    if (format === null) {
      errors.push(`${entry.name} is not a recognized png/jpeg/webp/gif file`);
      continue;
    }
    if (buffer.length < minBytes) {
      errors.push(`${entry.name} is only ${buffer.length} bytes; likely a placeholder or error page`);
      continue;
    }
    images.push({ path, bytes: buffer.length, format, sha256 });
  }
  if (Number.isInteger(count) && images.length !== count) {
    errors.push(`expected ${count} valid images, found ${images.length}`);
  }
  return { errors, images };
}

function validateModelRecord(receipt, field, errors) {
  const model = receipt[field];
  if (!model || typeof model !== 'object') {
    errors.push(`missing model record: ${field}`);
    return;
  }
  if (typeof model.requested !== 'string' || !model.requested.trim()) {
    errors.push(`${field}.requested must be a non-empty string`);
  }
  if (!MODEL_STATUSES.has(model.status)) {
    errors.push(`${field}.status must be verified or unverified`);
  }
  if (typeof model.evidence !== 'string' || !model.evidence.trim()) {
    errors.push(`${field}.evidence must be a non-empty local evidence note`);
  }
  if (model.status === 'verified' && (typeof model.observed !== 'string' || !model.observed.trim())) {
    errors.push(`${field}.observed is required when status is verified`);
  }
  if (field === 'chatgpt_model') {
    for (const evidenceField of ['preflight_visible', 'postflight_visible']) {
      if (typeof model[evidenceField] !== 'boolean') {
        errors.push(`${field}.${evidenceField} must be boolean`);
      }
    }
  }
}

function validateArtifact(receipt, field, errors) {
  const artifact = receipt.artifacts?.[field];
  if (!artifact || typeof artifact !== 'object') {
    errors.push(`missing artifact record: ${field}`);
    return;
  }
  if (typeof artifact.path !== 'string' || !artifact.path.trim()) {
    errors.push(`artifacts.${field}.path must be a non-empty string`);
  }
  if (typeof artifact.sha256 !== 'string' || !/^[a-f0-9]{64}$/.test(artifact.sha256)) {
    errors.push(`artifacts.${field}.sha256 must be 64 lowercase hex characters`);
  }
}

export function validateReceipt(receipt) {
  const errors = [];
  if (!receipt || typeof receipt !== 'object' || Array.isArray(receipt)) {
    return ['receipt must be a JSON object'];
  }
  if (receipt.schema_version !== 2) errors.push('schema_version must be 2');
  if (!TASK_TYPES.has(receipt.task_type)) errors.push('task_type must be reasoning or image');
  if (typeof receipt.task_id !== 'string' || !receipt.task_id.trim()) {
    errors.push('missing task_id');
  }
  if (!TRANSPORTS.has(receipt.transport)) {
    errors.push('transport must be codex-in-app-browser, user-chrome, or host-browser-use');
  }
  if (!receipt.artifacts || typeof receipt.artifacts !== 'object') {
    errors.push('missing artifacts');
    return errors;
  }
  validateArtifact(receipt, 'packet', errors);
  if (!Number.isInteger(receipt.artifacts.packet?.approximate_tokens) || receipt.artifacts.packet.approximate_tokens < 1) {
    errors.push('artifacts.packet.approximate_tokens must be a positive integer');
  }
  if (receipt.task_type === 'reasoning') {
    validateArtifact(receipt, 'result', errors);
  }
  if (receipt.task_type === 'image') {
    const images = receipt.artifacts.images;
    if (!Array.isArray(images) || images.length === 0) {
      errors.push('artifacts.images must be a non-empty array for image tasks');
    } else {
      images.forEach((image, index) => {
        if (typeof image?.path !== 'string' || !image.path.trim()) {
          errors.push(`artifacts.images[${index}].path must be a non-empty string`);
        }
        if (typeof image?.sha256 !== 'string' || !/^[a-f0-9]{64}$/.test(image.sha256)) {
          errors.push(`artifacts.images[${index}].sha256 must be 64 lowercase hex characters`);
        }
        if (!Number.isInteger(image?.bytes) || image.bytes < 1) {
          errors.push(`artifacts.images[${index}].bytes must be a positive integer`);
        }
        if (!IMAGE_FORMATS.has(image?.format)) {
          errors.push(`artifacts.images[${index}].format must be png, jpeg, webp, or gif`);
        }
      });
    }
  }
  validateArtifact(receipt, 'browser_evidence', errors);
  validateModelRecord(receipt, 'host_model', errors);
  validateModelRecord(receipt, 'chatgpt_model', errors);
  if (!receipt.privacy_review || typeof receipt.privacy_review !== 'object') {
    errors.push('missing privacy_review');
  } else {
    for (const field of PRIVACY_FIELDS) {
      if (typeof receipt.privacy_review[field] !== 'boolean') {
        errors.push(`privacy_review.${field} must be boolean`);
      }
    }
  }
  if (!new Set(['verified', 'failed']).has(receipt.browser_transport)) {
    errors.push('browser_transport must be verified or failed');
  }
  for (const field of [
    'packet_validation',
    'result_validation',
    'pair_validation',
    'images_validation',
    'local_revalidation',
    'tests',
  ]) {
    if (!CHECK_STATUSES.has(receipt[field])) {
      errors.push(`${field} must be passed, failed, or not_run`);
    }
  }
  if (!receipt.adoption || typeof receipt.adoption !== 'object') {
    errors.push('missing adoption record');
  } else {
    if (!CHECK_STATUSES.has(receipt.adoption.status)) {
      errors.push('adoption.status must be passed, failed, or not_run');
    }
    for (const field of ['accepted', 'rejected', 'deferred', 'local_evidence']) {
      if (!Array.isArray(receipt.adoption[field])) errors.push(`adoption.${field} must be an array`);
    }
  }
  if (!receipt.local_changes || typeof receipt.local_changes !== 'object') {
    errors.push('missing local_changes record');
  } else {
    if (!LOCAL_CHANGE_STATUSES.has(receipt.local_changes.status)) {
      errors.push('local_changes.status is invalid');
    }
    if (typeof receipt.local_changes.reason !== 'string' || !receipt.local_changes.reason.trim()) {
      errors.push('local_changes.reason must be non-empty');
    }
  }
  return errors;
}

export function receiptCompletionErrors(receipt) {
  const errors = validateReceipt(receipt);
  if (errors.length) return errors;
  if (receipt.host_model.status !== 'verified') errors.push('host_model is not verified');
  if (receipt.chatgpt_model.status !== 'verified') errors.push('chatgpt_model is not verified');
  if (!receipt.chatgpt_model.preflight_visible) errors.push('chatgpt_model preflight evidence is not verified');
  if (!receipt.chatgpt_model.postflight_visible) errors.push('chatgpt_model postflight evidence is not verified');
  if (receipt.browser_transport !== 'verified') errors.push('browser transport is not verified');
  for (const field of PRIVACY_FIELDS) {
    if (!receipt.privacy_review[field]) errors.push(`privacy_review.${field} is not passed`);
  }
  if (receipt.packet_validation !== 'passed') errors.push('packet_validation is not passed');
  if (receipt.adoption.status !== 'passed') errors.push('adoption is not passed');
  if (receipt.local_changes.status === 'applied') {
    if (receipt.local_revalidation !== 'passed') errors.push('local_revalidation is not passed');
    if (receipt.tests !== 'passed') errors.push('tests is not passed');
  } else if (receipt.local_changes.status === 'no_changes_needed') {
    if (!CHECK_STATUSES.has(receipt.local_revalidation)) errors.push('local_revalidation is invalid');
  } else {
    errors.push('local_changes is not complete');
  }
  if (receipt.task_type === 'reasoning') {
    if (receipt.result_validation !== 'passed') errors.push('result_validation is not passed');
    if (receipt.pair_validation !== 'passed') errors.push('pair_validation is not passed');
  }
  if (receipt.task_type === 'image') {
    if (receipt.images_validation !== 'passed') errors.push('images_validation is not passed');
  }
  return errors;
}

export async function verifyReceiptArtifacts(receipt, baseDirectory) {
  const errors = [];
  for (const field of ['packet', 'result', 'browser_evidence']) {
    const artifact = receipt.artifacts?.[field];
    if (!artifact?.path || !artifact?.sha256) continue;
    try {
      const content = await readFile(resolve(baseDirectory, artifact.path));
      const actual = sha256Buffer(content);
      if (actual !== artifact.sha256) {
        errors.push(`${field} sha256 mismatch: expected ${artifact.sha256}, actual ${actual}`);
      }
    } catch (error) {
      errors.push(`${field} artifact cannot be read: ${error.message}`);
    }
  }
  const images = receipt.artifacts?.images;
  if (Array.isArray(images)) {
    for (const [index, image] of images.entries()) {
      if (!image?.path || !image?.sha256) continue;
      try {
        const content = await readFile(resolve(baseDirectory, image.path));
        const actual = sha256Buffer(content);
        if (actual !== image.sha256) {
          errors.push(`images[${index}] sha256 mismatch: expected ${image.sha256}, actual ${actual}`);
        }
      } catch (error) {
        errors.push(`images[${index}] artifact cannot be read: ${error.message}`);
      }
    }
  }
  return errors;
}

function parseArgs(argv) {
  const [mode, firstPath, secondPath] = argv;
  const options = { mode, firstPath, secondPath, count: undefined, minBytes: undefined };
  if (!['packet', 'result', 'pair', 'image', 'images', 'receipt', 'complete', 'hash'].includes(mode)) {
    throw new Error('invalid mode');
  }
  if (!firstPath || (mode === 'pair' && !secondPath)) {
    throw new Error('missing required path argument');
  }
  if (mode === 'images') {
    for (let index = 2; index < argv.length; index += 1) {
      if (argv[index] === '--count' && Number.isInteger(Number.parseInt(argv[index + 1], 10))) {
        options.count = Number.parseInt(argv[index + 1], 10);
        index += 1;
      } else if (argv[index] === '--min-bytes' && Number.isInteger(Number.parseInt(argv[index + 1], 10))) {
        options.minBytes = Number.parseInt(argv[index + 1], 10);
        index += 1;
      } else {
        throw new Error(`unknown or incomplete argument: ${argv[index]}`);
      }
    }
  } else if (argv.length > 2 && mode !== 'pair') {
    throw new Error(`unexpected argument: ${argv[2]}`);
  }
  return options;
}

async function main() {
  let options;
  try {
    options = parseArgs(process.argv.slice(2));
  } catch (error) {
    console.error('usage: validate-handoff.mjs <packet|result|image> <markdown-file>');
    console.error('   or: validate-handoff.mjs pair <packet-file> <result-file>');
    console.error('   or: validate-handoff.mjs images <dir> [--count <n>] [--min-bytes <n>]');
    console.error('   or: validate-handoff.mjs <receipt|complete> <receipt-json>');
    console.error('   or: validate-handoff.mjs hash <artifact-file>');
    console.error(error.message);
    process.exitCode = 2;
    return;
  }

  if (options.mode === 'images') {
    const { errors, images } = await scanImagesDir(options.firstPath, {
      count: options.count,
      minBytes: options.minBytes,
    });
    for (const image of images) {
      console.log(`${image.format} ${image.bytes} ${image.sha256}  ${image.path}`);
    }
    if (errors.length) {
      for (const error of errors) console.error(`ERROR: ${error}`);
      process.exitCode = 1;
      return;
    }
    console.log(`OK: ${images.length} valid image(s)`);
    return;
  }

  const text = await readFile(options.firstPath, 'utf8');
  if (options.mode === 'hash') {
    console.log(`${sha256Text(text)}  ${options.firstPath}`);
    return;
  }
  const second = options.mode === 'pair' ? await readFile(options.secondPath, 'utf8') : undefined;
  const parsedReceipt = ['receipt', 'complete'].includes(options.mode) ? JSON.parse(text) : undefined;
  const errors = options.mode === 'packet'
    ? validatePacket(text)
    : options.mode === 'result'
      ? validateResult(text)
      : options.mode === 'image'
        ? validateImageTask(text)
        : options.mode === 'pair'
          ? validatePair(text, second)
          : options.mode === 'receipt'
            ? validateReceipt(parsedReceipt)
            : receiptCompletionErrors(parsedReceipt);
  if (options.mode === 'complete') {
    errors.push(...await verifyReceiptArtifacts(parsedReceipt, process.cwd()));
  }
  if (errors.length) {
    for (const error of errors) console.error(`ERROR: ${error}`);
    process.exitCode = 1;
    return;
  }
  const suffix = ['packet', 'result', 'image'].includes(options.mode)
    ? ` (~${estimateTokens(text)} tokens)`
    : options.mode === 'receipt' && receiptCompletionErrors(parsedReceipt).length
      ? ' (incomplete)'
      : '';
  console.log(`OK: valid ${options.mode}${suffix}`);
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  await main();
}
