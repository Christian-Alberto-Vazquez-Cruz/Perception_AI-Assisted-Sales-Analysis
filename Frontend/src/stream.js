export async function consumeSSE(body, onEvent) {
  if (!body) throw new Error('El navegador no recibió un flujo de respuesta.');
  const reader = body.getReader();
  const decoder = new TextDecoder();
  let pending = '';
  let terminal = false;
  function dispatch(frame) {
    let event = 'message';
    const data = [];
    for (const line of frame.split('\n')) {
      if (line.startsWith('event:')) event = line.slice(6).trim();
      if (line.startsWith('data:')) data.push(line.slice(5).trimStart());
    }
    if (data.length) {
      onEvent(event, JSON.parse(data.join('\n')));
      if (event === 'done' || event === 'error') terminal = true;
    }
  }
  try {
    while (true) {
      const { value, done } = await reader.read();
      pending += done ? decoder.decode() : decoder.decode(value, { stream: true });
      pending = pending.replace(/\r\n/g, '\n');
      let end;
      while ((end = pending.indexOf('\n\n')) >= 0) {
        dispatch(pending.slice(0, end)); pending = pending.slice(end + 2);
      }
      if (done) break;
    }
    if (!terminal) throw new Error('La conexión terminó antes de completar la respuesta. Intenta de nuevo.');
  } finally { await reader.cancel().catch(() => {}); reader.releaseLock(); }
}
