const fs = require('fs');
const filename = process.argv[2];
const content = fs.readFileSync(filename, 'utf-8');

let target, images = [];
function replaceContent(mdFileName, images) {
  let content = fs.readFileSync(mdFileName, 'utf-8');
  for (const { url, name } of images) {
    const regexp = url.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    content = content.replace(new RegExp(regexp, 'g'), name);
  }
  fs.writeFileSync(mdFileName, content);
}

for (const line of content.split('\n')) {
  if (line.startsWith('File: ')) {
    if (target) {
      const md = `src/${target}.md`;
      if (!fs.existsSync(md)) {
        console.error(`Markdown not found: ${md}`);
        process.exit(1);
      } else {
        replaceContent(md, images);
      }
    }


    const fullname = line.slice(6).trim().split('.');
    fullname.pop();
    const parts = fullname.join('.').split('/');
    parts.shift();
    target = parts.join('/');
    images = [];
    continue;
  }

  if (line.startsWith('  ')) {
    const [index, url, name] = line.trim().split('|');
    if (!fs.existsSync(`imgs/compressed/${target}/${name}.avif`)) {
      console.error(`Image not found: imgs/compressed/${target}/${name}.avif`);
      process.exit(1);
    }

    images.push({ url, name });
    continue;
  }

  if (line.trim() === '') {
    continue;
  }

  console.log(`Unrecognized line: ${line}`);
  process.exit(1);
}

if (target) {
  const md = `src/${target}.md`;
  if (!fs.existsSync(md)) {
    console.error(`Markdown not found: ${md}`);
  } else {
    replaceContent(md, images);
  }
}
