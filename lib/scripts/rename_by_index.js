const fs = require('fs');
const filename = process.argv[2];
const content = fs.readFileSync(filename, 'utf-8');

function ensureFileExists(base) {
  return fs.existsSync(`${base}.jpeg`) ? 'jpeg'
    : fs.existsSync(`${base}.jpg`) ? 'jpg'
      : fs.existsSync(`${base}.png`) ? 'png'
        : fs.existsSync(`${base}.gif`) ? 'gif' : null;
}

let target;
for (const line of content.split('\n')) {
  if (line.startsWith('File: ')) {
    const fullname = line.slice(6).trim().split('.');
    fullname.pop();
    const parts = fullname.join('.').split('/');
    parts.shift();
    target = parts.join('/');
    continue;
  }

  if (line.startsWith('  ')) {
    const [index, url, name] = line.trim().split('|');
    const base = `imgs/src/${target}`;
    const comp = `imgs/compressed/${target}`;
    const extension = ensureFileExists(`${base}/${index}`);
    if (!extension) {
      if (!ensureFileExists(`${base}/${name}`)) {
        console.log(`File not found: ${base}/${index}.[jpeg|jpg|png|gif]`);
      }
      continue;
    }

    fs.renameSync(`${base}/${index}.${extension}`, `${base}/${name}.${extension}`);
    fs.renameSync(`${comp}/${index}.avif`, `${base}/${name}.avif`);
    continue;
  }

  if (line.trim() === '') {
    continue;
  }

  console.log(`Unrecognized line: ${line}`);
  process.exit(1);
}
