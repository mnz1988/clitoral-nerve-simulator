// Runs the checklist page's scripts against a stub DOM and checks behavior.
// Usage: node test_checklist.js <path to checklist folder>
const fs = require('fs');
const path = require('path');
const vm = require('vm');
const dir = process.argv[2];

function makeEl(tag) {
  const cls = new Set();
  const e = {
    tag, children: [], attrs: {}, listeners: {}, style: {}, value: '', checked: false, disabled: false,
    textContent: '', files: [],
    classList: {
      add: c => cls.add(c), remove: c => cls.delete(c),
      toggle: (c, on) => { if (on === undefined) on = !cls.has(c); on ? cls.add(c) : cls.delete(c); },
      contains: c => cls.has(c)
    },
    set className(v) { cls.clear(); String(v).split(/\s+/).filter(Boolean).forEach(c => cls.add(c)); },
    get className() { return [...cls].join(' '); },
    appendChild(c) { this.children.push(c); return c; },
    setAttribute(k, v) { this.attrs[k] = v; },
    getAttribute(k) { return this.attrs[k]; },
    addEventListener(t, f) { (this.listeners[t] = this.listeners[t] || []).push(f); },
    fire(t) { (this.listeners[t] || []).forEach(f => f.call(this, { target: this })); },
    focus() {}, click() {}, remove() {}
  };
  return e;
}
const ids = {};
const store = {};
const document = {
  createElement: makeEl,
  createTextNode: t => ({ text: t }),
  getElementById: id => ids[id] || (ids[id] = makeEl('#' + id)),
  body: makeEl('body'), activeElement: null
};
const sandbox = {
  window: {}, document,
  localStorage: { getItem: k => (k in store ? store[k] : null), setItem: (k, v) => { store[k] = v; } },
  console, Date, JSON, Math, Object, String, Blob: function () {}, URL: { createObjectURL: () => 'blob:x' },
  FileReader: function () {}, alert: m => { throw new Error('alert: ' + m); }
};
sandbox.window = sandbox;
vm.createContext(sandbox);

const html = fs.readFileSync(path.join(dir, 'index.html'), 'utf8');
const inline = html.match(/<script>([\s\S]*?)<\/script>/)[1];
vm.runInContext(fs.readFileSync(path.join(dir, 'steps.js'), 'utf8'), sandbox, { filename: 'steps.js' });
vm.runInContext(fs.readFileSync(path.join(dir, 'progress.js'), 'utf8'), sandbox, { filename: 'progress.js' });
// Check the saved progress refers only to real steps, then run behavior tests from a clean state.
const savedProgress = sandbox.PROGRESS;
const savedIds = Object.keys(savedProgress.steps || {});
const unknownSaved = savedIds.filter(id => !sandbox.CHECKLIST.steps.some(s => s.id === id));
sandbox.PROGRESS = { updated: null, steps: {}, amendments: [] };

// ---- data integrity ----
const D = sandbox.CHECKLIST;
const fail = [];
if (unknownSaved.length) fail.push('progress.js has unknown step ids: ' + unknownSaved.join());
console.log('saved progress entries:', savedIds.join(', ') || '(none)');
const seen = new Set();
const phaseIds = new Set(D.phases.map(p => p.id));
for (const s of D.steps) {
  if (seen.has(s.id)) fail.push('duplicate id ' + s.id);
  seen.add(s.id);
  if (!phaseIds.has(s.phase)) fail.push(s.id + ': unknown phase ' + s.phase);
  for (const f of ['title', 'kind', 'who', 'model', 'effort', 'why']) if (!s[f]) fail.push(s.id + ': missing ' + f);
  if (!Array.isArray(s.what) || !s.what.length) fail.push(s.id + ': no what');
  if (!Array.isArray(s.verify) || !s.verify.length) fail.push(s.id + ': no verify');
  if (s.review && !(s.review.who && s.review.ask)) fail.push(s.id + ': bad review');
  if (!['low', 'medium', 'high', 'xhigh', 'max'].includes(s.effort)) fail.push(s.id + ': bad effort');
  if (!/^(Haiku 5\.5|Sonnet 5\.5|Opus 5\.5|Fable 5\.2)$/.test(s.model)) fail.push(s.id + ': bad model');
}
for (const s of D.steps) for (const d of s.needs || []) {
  if (!seen.has(d)) fail.push(s.id + ': needs unknown ' + d);
  if (d === s.id) fail.push(s.id + ': needs itself');
}
// dependencies must not form a cycle, or no step in the cycle could ever become ready
{
  const stepMap = Object.fromEntries(D.steps.map(s => [s.id, s]));
  const mark = {};
  const visit = (id, trail) => {
    if (mark[id] === 2) return;
    if (mark[id] === 1) { fail.push('dependency cycle: ' + trail.concat(id).join(' -> ')); return; }
    mark[id] = 1;
    for (const d of (stepMap[id] && stepMap[id].needs) || []) visit(d, trail.concat(id));
    mark[id] = 2;
  };
  D.steps.forEach(s => visit(s.id, []));
}
// backticks must pair up so code spans render correctly
for (const s of D.steps) for (const t of [...s.what, ...s.verify, ...(s.get || [])])
  if ((t.split('`').length - 1) % 2) fail.push(s.id + ': unpaired backtick in "' + t.slice(0, 40) + '"');

// ---- run the page script ----
vm.runInContext(inline, sandbox, { filename: 'index.html<script>' });

function find(node, pred, out = []) {
  if (!node || !node.children) return out;
  for (const c of node.children) { if (c.tag && pred(c)) out.push(c); find(c, pred, out); }
  return out;
}
const root = ids['phases'];
const cards = find(root, e => e.tag === 'details');
if (cards.length !== D.steps.length) fail.push('cards ' + cards.length + ' != steps ' + D.steps.length);
if (!/^0 of \d+ steps complete/.test(ids['summary'].textContent)) fail.push('summary: ' + ids['summary'].textContent);
if (!/^Next ready step: 0\.1 /.test(ids['next'].textContent)) fail.push('next: ' + ids['next'].textContent);

// Step 0.1 (no review): done + verified => complete
const c01 = cards.find(c => c.attrs.id === 'step-0.1');
const sel = find(c01, e => e.tag === 'select')[0];
const boxes = find(c01, e => e.tag === 'input');
sel.value = 'done'; sel.fire('change');
if (c01.attrs['data-state'] !== 'waiting') fail.push('0.1 after done: ' + c01.attrs['data-state']);
boxes[0].checked = true; boxes[0].fire('change');
if (c01.attrs['data-state'] !== 'complete') fail.push('0.1 after verify: ' + c01.attrs['data-state']);
if (!/^1 of /.test(ids['summary'].textContent)) fail.push('summary after 0.1: ' + ids['summary'].textContent);

// Step 0.3 (has review): done + verified is still waiting until reviewed
const c03 = cards.find(c => c.attrs.id === 'step-0.3');
const sel3 = find(c03, e => e.tag === 'select')[0];
const boxes3 = find(c03, e => e.tag === 'input');
if (boxes3.length !== 2) fail.push('0.3 should have 2 checkboxes, has ' + boxes3.length);
sel3.value = 'done'; sel3.fire('change');
boxes3[0].checked = true; boxes3[0].fire('change');
if (c03.attrs['data-state'] !== 'waiting') fail.push('0.3 before review: ' + c03.attrs['data-state']);
boxes3[1].checked = true; boxes3[1].fire('change');
if (c03.attrs['data-state'] !== 'complete') fail.push('0.3 after review: ' + c03.attrs['data-state']);

// Two failed attempts => blocked, third click does nothing
const c05 = cards.find(c => c.attrs.id === 'step-0.5');
const btns = find(c05, e => e.tag === 'button');
const bFail = btns.find(b => b.textContent === 'Log failed attempt');
const bClear = btns.find(b => b.textContent === 'Clear after my decision');
bFail.fire('click');
if (c05.attrs['data-state'] === 'blocked') fail.push('0.5 blocked after one failure');
bFail.fire('click');
if (c05.attrs['data-state'] !== 'blocked') fail.push('0.5 not blocked after two: ' + c05.attrs['data-state']);
if (!bFail.disabled) fail.push('fail button still enabled after two');
bFail.fire('click');
const saved = JSON.parse(store['cns-checklist-v1']);
if (saved.steps['0.5'].fails !== 2) fail.push('fails went past 2: ' + saved.steps['0.5'].fails);
bClear.fire('click');
if (c05.attrs['data-state'] !== 'todo') fail.push('0.5 after clear: ' + c05.attrs['data-state']);

// Amendment draft
const g = id => document.getElementById(id);
g('aTitle').value = 'Test amendment'; g('aProblem').value = 'p'; g('aChange').value = 'c'; g('aStep').value = '';
ids['aAdd'].fire('click');
if (JSON.parse(store['cns-checklist-v1']).amendments.length !== 1) fail.push('amendment not saved');

// Filter: blocked only => nothing visible now
ids['fState'].value = 'complete'; ids['fState'].fire('change');
const visible = cards.filter(c => !c.classList.contains('hidden')).map(c => c.attrs.id);
if (visible.join() !== 'step-0.1,step-0.3') fail.push('filter complete shows: ' + visible.join());

console.log('steps:', D.steps.length, '| phases:', D.phases.length, '| with expert review:', D.steps.filter(s => s.review).length);
console.log(fail.length ? 'FAIL\n - ' + fail.join('\n - ') : 'PASS: all checks');
process.exit(fail.length ? 1 : 0);
