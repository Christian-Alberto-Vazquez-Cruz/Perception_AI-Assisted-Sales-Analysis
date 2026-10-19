import test from 'node:test';
import assert from 'node:assert/strict';
import { consumeSSE } from './stream.js';

test('SSE handles arbitrary byte boundaries including Spanish UTF-8', async () => {
  const bytes = new TextEncoder().encode('event: delta\ndata: {"text":"caída"}\n\nevent: done\ndata: {"answer":"caída"}\n\n');
  const body = new ReadableStream({ start(c) { for (const b of bytes) c.enqueue(Uint8Array.of(b)); c.close(); } });
  const events = [];
  await consumeSSE(body, (name, data) => events.push([name, data]));
  assert.deepEqual(events, [['delta', {text:'caída'}], ['done', {answer:'caída'}]]);
});

test('SSE rejects abrupt disconnects', async () => {
  const body = new ReadableStream({ start(c) { c.enqueue(new TextEncoder().encode('event: delta\ndata: {"text":"incompleto"}\n\n')); c.close(); } });
  await assert.rejects(consumeSSE(body, () => {}), /antes de completar/);
});
