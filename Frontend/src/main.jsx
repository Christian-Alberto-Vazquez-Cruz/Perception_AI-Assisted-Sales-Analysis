import React, { useEffect, useRef, useState } from 'react';
import { createRoot } from 'react-dom/client';
import ReactMarkdown from 'react-markdown';
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, BarChart, Bar, Cell } from 'recharts';
import './styles.css';
import { consumeSSE } from './stream.js';
import perceptionLogo from './assets/perception-icon.png';

const API = import.meta.env.VITE_API_URL || '/api';
const number = value => new Intl.NumberFormat('es-MX', { maximumFractionDigits: 2 }).format(value);
const short = value => new Intl.NumberFormat('es-MX', { notation: 'compact', maximumFractionDigits: 1 }).format(value);
const colors = ['#307263', '#83a897', '#ceab6e', '#a6b5c2', '#c18270'];

async function checked(response) {
  if (response.ok) return response;
  let detail;
  try { detail = (await response.json()).detail; } catch {  }
  throw new Error(typeof detail === 'string' ? detail : Array.isArray(detail) ? detail.slice(0, 3).map(e => `${e.loc.join('.')}: ${e.msg}`).join(' · ') : `No se pudo completar la solicitud (${response.status}).`);
}

function Icon({ name, size = 20 }) {
  const paths = { upload: <><path d="M12 16V3m-5 5 5-5 5 5"/><path d="M4 15v5h16v-5"/></>, arrow: <><path d="m5 12 14 0m-6-6 6 6-6 6"/></>, spark: <><path d="m12 3 2.5 6.5L21 12l-6.5 2.5L12 21l-2.5-6.5L3 12l6.5-2.5Z"/></>, chart: <><path d="M4 4v16h16M8 15l4-5 4 2 4-7"/></>, file: <><path d="M6 3h8l4 4v14H6zM14 3v5h4M9 12h6m-6 4h6"/></> };
  return <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">{paths[name] || paths.spark}</svg>;
}

function Sources({ sources, messageId }) {
  if (!sources?.length) return null;
  return <div className="sources"><p className="eyebrow">Fuentes de esta respuesta · {sources.length}</p><div className="source-list">{sources.map(source => <details key={source.id} id={`${messageId}-${source.id}`}><summary><span className={`source-tag ${source.kind}`}>{source.kind === 'metric' ? 'Métrica' : 'Guía'}</span>{source.title}<span className="source-plus">+</span></summary>{source.content ? <div className="source-body"><small>{source.document} · Hipótesis orientativa</small><p>{source.content}</p></div> : <pre>{JSON.stringify(source.data, null, 2)}</pre>}</details>)}</div></div>;
}

function Answer({ message }) {
  return <article className="message"><div className="question"><span>Tú</span><p>{message.question}</p></div><div className="answer"><div className="answer-author"><span className="ai-mark"><Icon name="spark" size={15}/></span> Perception <span className="muted">/ Análisis de ventas</span></div><div className="markdown"><ReactMarkdown components={{ a: ({ href, children }) => {
    const source = message.sources?.find(s => href === `#${s.id}`);
    return source ? <a href={`#${message.id}-${source.id}`} onClick={() => { const el = document.getElementById(`${message.id}-${source.id}`); if (el) el.open = true; }}>{children}</a> : <span>{children}</span>;
  } }}>{message.answer || (message.error ? 'No se pudo completar el análisis.' : 'Revisando tus métricas…')}</ReactMarkdown></div>{message.pending && <p className="pending">Generando · Texto provisional; comprobando enlaces al finalizar…</p>}{message.error && <p className="error" role="alert">{message.error}</p>}<Sources sources={message.sources} messageId={message.id}/></div></article>;
}

function App() {
  const [dataset, setDataset] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [question, setQuestion] = useState('');
  const [messages, setMessages] = useState([]);
  const [busy, setBusy] = useState(false);
  const [measure, setMeasure] = useState('importe');
  const [activeSection, setActiveSection] = useState(() => window.location.hash === '#assistant' ? 'assistant' : 'overview');
  const input = useRef(null);
  const requestLock = useRef(false);
  const chatInput = useRef(null);

  useEffect(() => {
    const syncSection = () => {
      const hash = window.location.hash;
      if (hash === '#assistant') setActiveSection('assistant');
      else if (!hash || hash === '#overview') setActiveSection('overview');
    };
    window.addEventListener('hashchange', syncSection);
    return () => window.removeEventListener('hashchange', syncSection);
  }, []);

  useEffect(() => {
    let active = true;
    fetch(`${API}/datasets/current`).then(async response => {
      if (response.status === 409) return;
      const result = await (await checked(response)).json();
      if (active) setDataset(result);
    }).catch(() => { if (active) setError('No hay conexión con el backend. Inicia FastAPI y recarga la página.'); }).finally(() => { if (active) setLoading(false); });
    return () => { active = false; };
  }, []);

  async function upload(file) {
    if (!file || requestLock.current) return;
    requestLock.current = true;
    setUploading(true); setError('');
    try {
      if (file.size > 15 * 1024 * 1024) throw new Error('El archivo debe pesar menos de 15 MB.');
      let records;
      try { records = JSON.parse(await file.text()); } catch { throw new Error('El archivo no contiene JSON válido.'); }
      const response = await checked(await fetch(`${API}/datasets`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(records) }));
      setDataset(await response.json()); setMessages([]);
    } catch (e) { setError(e.message); }
    finally { setUploading(false); requestLock.current = false; if (input.current) input.current.value = ''; }
  }

  async function ask(event, preset) {
    event?.preventDefault();
    const text = (preset || question).trim();
    if (!text || !dataset || requestLock.current) return;
    requestLock.current = true;
    const id = crypto.randomUUID();
    setMessages(old => [...old, { id, question: text, answer: '', pending: true, sources: [] }]);
    setQuestion(''); setBusy(true);
    const update = changes => setMessages(old => old.map(m => m.id === id ? { ...m, ...changes } : m));
    try {
      const response = await checked(await fetch(`${API}/chat`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ question: text, stream: true }) }));
      let accumulated = '';
      await consumeSSE(response.body, (event, data) => {
        if (event === 'sources') update({ sources: data.sources });
        if (event === 'delta') { accumulated += data.text; update({ answer: accumulated }); }
        if (event === 'done') update({ answer: data.answer, pending: false });
        if (event === 'error') { update({ answer: '', pending: false, error: data.message }); }
      });
    } catch (e) { update({ answer: '', pending: false, error: e.message }); }
    finally { setBusy(false); requestLock.current = false; chatInput.current?.focus(); }
  }

  const last = dataset?.monthly.at(-1);
  const variation = last?.[`variacion_${measure}_pct`];
  const suggestions = ['¿Qué guías tienes?', '¿Por qué han habido bajas?', '¿Cuál fue el día con mayor importe?'];

  return <div className="app-shell"><aside className="sidebar"><a className="brand" href="#overview" aria-label="Perception: resumen de ventas" onClick={() => setActiveSection('overview')}><span className="brand-icon"><img className="brand-logo" src={perceptionLogo} alt=""/></span><span>Perception</span></a><p className="nav-label">TU NEGOCIO</p><a className={`nav-item${activeSection === 'overview' ? ' active' : ''}`} href="#overview" aria-current={activeSection === 'overview' ? 'location' : undefined} onClick={() => setActiveSection('overview')}><Icon name="chart"/>Resumen de ventas</a><a className={`nav-item${activeSection === 'assistant' ? ' active' : ''}`} href="#assistant" aria-current={activeSection === 'assistant' ? 'location' : undefined} onClick={() => setActiveSection('assistant')}><Icon name="spark"/>Asistente IA</a><div className="sidebar-foot"><span className="status-dot"/>Una tienda · Un solo panorama</div></aside>
    <main><header className="topbar"><span>Mi tienda <span className="slash">/</span> <strong>Resumen</strong></span></header><div className="main-content" id="overview"><section className="page-title"><div><h1>Tu tienda, en perspectiva<span>.</span></h1></div><button className="primary" onClick={() => input.current.click()} disabled={busy || uploading || loading}><Icon name="upload"/>{uploading ? 'Procesando…' : dataset ? 'Reemplazar JSON' : 'Subir ventas'}</button><input ref={input} type="file" accept=".json,application/json" onChange={e => upload(e.target.files[0])} hidden aria-label="Archivo JSON de ventas"/></section>
    {error && <div className="error-banner" role="alert">{error}</div>}
    {loading ? <div className="empty-state">Conectando con tu tienda…</div> : !dataset ? <section className="empty-state"><div className="empty-icon"><Icon name="file" size={34}/></div><p className="eyebrow">EL PRIMER PASO ES TUYO</p><h2>Tus números tienen una historia.</h2><p>Sube tu JSON de ventas para ver gráficas y hacer preguntas.<br/>Necesitamos fecha, categoría, unidades e importe.</p><button className="primary" disabled={uploading} onClick={() => input.current.click()}><Icon name="upload"/>Seleccionar JSON</button><small>Un solo dataset activo · Cada carga reemplaza la anterior</small><p className="sample-hint">Para probar: usa examples/ventas.json incluido en el proyecto.</p></section> : <>
      <div className="dataset-toolbar"><span><span className="status-dot"/>Dataset activo <span className="muted">· {dataset.totals.desde} a {dataset.totals.hasta} · {number(dataset.totals.registros)} registros</span></span><div className="segmented" aria-label="Métrica de las gráficas">{['importe', 'unidades'].map(m => <button key={m} aria-pressed={measure === m} className={measure === m ? 'selected' : ''} onClick={() => setMeasure(m)}>{m === 'importe' ? 'Importe' : 'Unidades'}</button>)}</div></div>
      <section className="stats"><div className="stat"><span>Importe acumulado</span><strong>{number(dataset.totals.importe)}<small>u. monetarias</small></strong><p>Todos los registros cargados</p></div><div className="stat"><span>Unidades vendidas</span><strong>{number(dataset.totals.unidades)}</strong><p>{dataset.categories.length} categorías en tu tienda</p></div><div className="stat"><span>Cambio de {measure} · {last.mes}</span><strong className={variation < 0 ? 'negative' : variation > 0 ? 'positive' : ''}>{variation == null ? '—' : `${variation > 0 ? '+' : ''}${number(variation)}%`}</strong><p>{last.comparado_con ? `Frente a ${last.comparado_con} · Revisar cobertura` : 'Sin mes anterior comparable'}</p></div></section>
      <section className="charts"><div className="panel"><div className="panel-heading"><div><p className="eyebrow">LA EVOLUCIÓN</p><h2>Ventas por mes</h2></div><span className="legend"><i/>{measure === 'importe' ? 'Importe' : 'Unidades'}</span></div><div className="chart"><ResponsiveContainer width="100%" height="100%"><LineChart data={dataset.monthly} margin={{ top: 20, right: 16, bottom: 8, left: 0 }}><CartesianGrid vertical={false} stroke="#e9ece7" strokeDasharray="3 4"/><XAxis dataKey="mes" tick={{ fontSize: 11, fill: '#7a8780' }} tickLine={false} axisLine={false} dy={10}/><YAxis tickFormatter={short} tick={{ fontSize: 11, fill: '#7a8780' }} tickLine={false} axisLine={false} width={48}/><Tooltip formatter={v => [number(v), measure]} contentStyle={{ borderRadius: 10, border: '1px solid #e1e6df' }}/><Line type="linear" dataKey={measure} stroke="#307263" strokeWidth={3} isAnimationActive={false} dot={{ r: 4, fill: '#307263', stroke: '#fff', strokeWidth: 2 }} activeDot={{ r: 6 }}/></LineChart></ResponsiveContainer></div></div>
      <div className="panel"><div className="panel-heading"><div><p className="eyebrow">EL DETALLE</p><h2>Ventas por categoría</h2></div><span className="subtle-pill">Todo el periodo</span></div><div className="chart" style={{ height: Math.max(255, dataset.categories.length * 35) }}><ResponsiveContainer width="100%" height="100%"><BarChart layout="vertical" data={dataset.categories} margin={{ top: 18, right: 22, bottom: 0, left: 0 }}><CartesianGrid horizontal={false} stroke="#e9ece7" strokeDasharray="3 4"/><XAxis type="number" tickFormatter={short} tick={{ fontSize: 11, fill: '#7a8780' }} tickLine={false} axisLine={false}/><YAxis type="category" dataKey="categoria" tick={{ fontSize: 11, fill: '#55675f' }} tickLine={false} axisLine={false} width={95}/><Tooltip formatter={v => [number(v), measure]} cursor={{ fill: '#f2f5f0' }}/><Bar dataKey={measure} radius={[0, 5, 5, 0]} maxBarSize={28} isAnimationActive={false}>{dataset.categories.map((c, i) => <Cell key={c.categoria} fill={colors[i % colors.length]}/>)}</Bar></BarChart></ResponsiveContainer></div></div></section>
    </>}
    <section className="assistant panel" id="assistant"><div className="assistant-heading"><span className="assistant-icon"><Icon name="spark" size={24}/></span><div><p className="eyebrow">UNA CONVERSACIÓN CON TUS DATOS</p><h2>Pregunta. Entiende. Decide.</h2></div><span className="subtle-pill">GPT-OSS + tus fuentes</span></div>{!messages.length && <div className="chat-welcome"><p>¿Qué te gustaría entender de tu tienda?</p><span>Pregunta en tus palabras. Cada hallazgo apunta a su fuente.</span><div className="suggestions">{suggestions.map(s => <button key={s} disabled={!dataset || busy || uploading} onClick={e => ask(e, s)}>{s}<Icon name="arrow" size={16}/></button>)}</div></div>}<div className="messages" aria-live="polite">{messages.map(m => <Answer key={m.id} message={m}/>)}</div><form className="chat-form" onSubmit={ask}><input ref={chatInput} value={question} maxLength={2000} onChange={e => setQuestion(e.target.value)} placeholder={dataset ? 'Por ejemplo: ¿qué categoría bajó más en marzo?' : 'Sube tus ventas para comenzar…'} aria-label="Pregunta sobre tus ventas" disabled={!dataset || busy || uploading}/><button className="send" disabled={!dataset || !question.trim() || busy || uploading} aria-label="Enviar pregunta"><Icon name="arrow"/></button></form><p className="chat-footnote">{busy ? 'Consultando tus métricas y fuentes…' : 'Las causas son hipótesis para verificar. Perception te muestra la evidencia disponible.'}</p></section><footer><span className="footer-brand">Perception.</span><span>Datos claros. Decisiones con contexto</span></footer></div></main></div>;
}

createRoot(document.getElementById('root')).render(<React.StrictMode><App/></React.StrictMode>);
