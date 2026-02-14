#!/usr/bin/env node
const { readdirSync, readFileSync, existsSync, writeFileSync } = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const IMG_DIR = path.join('imgs', 'compressed');
const META_PATH = path.join('imgs', '_meta.txt');
const ENV_FILE = '.env';

readFileSync(ENV_FILE, 'utf8').split('\n').forEach(line => {
  const [key, value] = line.split('=');
  if (key && value && !process.env[key.trim()]) {
    process.env[key.trim()] = value.trim();
  }
});

const ACCOUNT_ID = process.env.R2_ACCOUNT_ID;
const BUCKET_NAME = process.env.R2_BUCKET;
const ACCESS_KEY = process.env.R2_ACCESS_KEY_ID;
const SECRET_KEY = process.env.R2_SECRET_ACCESS_KEY;

if (!ACCOUNT_ID || !BUCKET_NAME || !ACCESS_KEY || !SECRET_KEY) {
  console.error('Missing required env vars. Please set R2_ACCOUNT_ID, R2_BUCKET, R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY');
  process.exit(1);
}

const R2_URL = `https://${ACCOUNT_ID}.r2.cloudflarestorage.com/${BUCKET_NAME}`;

function curl(filePath) {
  return new Promise((resolve, reject) => {
    const curlArgs = [
      `${R2_URL}/${filePath}`,
      '-s',
      '-X', 'PUT',
      '--user', `'${ACCESS_KEY}:${SECRET_KEY}'`,
      '--aws-sigv4', 'aws:amz:auto:s3',
      '-H', "'x-amz-content-sha256: UNSIGNED-PAYLOAD'",
      '--data-binary', `@${path.join(IMG_DIR, filePath)}`
    ];

    try {
      const result = execSync(`curl '${R2_URL}/${filePath}' ${curlArgs.join(' ')}`, { encoding: 'utf8' });
      resolve(result);
    } catch (error) {
      reject(error);
    }
  });
}

function walkDir(dir) {
  const list = readdirSync(dir, { withFileTypes: true, recursive: true });

  return list.filter((e) => e.isFile()).map((e) => path.join(e.parentPath, e.name).substring(IMG_DIR.length + 1));
}

function readMeta() {
  if (!existsSync(META_PATH)) {
    return { exist: false, uploaded: new Set() };
  }
  const content = readFileSync(META_PATH, 'utf8');
  const files = content.split('\n').map(line => line.trim()).filter(line => line !== '');
  return { exist: true, uploaded: new Set(files) };
}

async function main() {
  const files = walkDir(IMG_DIR).filter(p => path.extname(p) === '.avif');
  if (files.length === 0) {
    console.log('No `avif` files found in', IMG_DIR);
    return;
  }
  const meta = readMeta();
  if (!meta.exist) {
    meta.uploaded = new Set(files);
  }

  for await (const f of files) {
    if (meta.uploaded.has(f)) {
      continue;
    }

    try {
      await curl(f);
      meta.uploaded.add(f);
      console.log('Uploaded', f);
    } catch (err) {
      console.error('Failed uploading', f, err.message);
      throw err;
    }
  }

  writeFileSync(META_PATH, Array.from(meta.uploaded).join('\n'), 'utf8');
  console.log('Wrote metadata to', META_PATH);
}

main().catch(err => { console.error(err); process.exit(1); });
