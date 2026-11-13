// Updates entries in checklist/progress.js without disturbing the others.
// Usage: node set_progress.js <path to progress.js> <path to updates.json>
const fs = require('fs');
const [file, updatesFile] = process.argv.slice(2);
const text = fs.readFileSync(file, 'utf8');
const data = JSON.parse(text.slice(text.indexOf('{'), text.lastIndexOf('}') + 1));
const updates = JSON.parse(fs.readFileSync(updatesFile, 'utf8'));
const now = Date.now();
for (const [id, patch] of Object.entries(updates)) {
  const base = data.steps[id] || { status: 'todo', verified: false, reviewed: false, fails: 0, notes: '' };
  data.steps[id] = Object.assign(base, patch, { t: now });
}
data.updated = new Date(now).toISOString();
const header = '// Saved checklist progress. Replace this file with the one the Export button\n' +
  '// in index.html downloads, then commit it.\n';
fs.writeFileSync(file, header + 'window.PROGRESS = ' + JSON.stringify(data, null, 2) + ';\n');
console.log('updated:', Object.keys(updates).join(', '), '| total entries:', Object.keys(data.steps).length);
