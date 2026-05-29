export interface MeetingReport {
  date: string;
  objectives: string[];
  topics: string[];
  commitments: string[];
  summary: string;
  wordCount: number;
}

// ── Palabras clave por categoría ──────────────────────────────────────────

const OBJECTIVE_TRIGGERS: string[] = [
  'el objetivo', 'los objetivos', 'la meta', 'las metas',
  'el proposito', 'la finalidad', 'el motivo',
  'nos reunimos para', 'estamos aqui para', 'la reunion es para',
  'la reunion tiene como', 'hoy vamos a', 'hoy nos reunimos',
  'en esta reunion', 'el fin de', 'lo que queremos lograr',
  'lo que buscamos', 'se convoco para', 'la agenda de hoy',
  'queremos revisar', 'queremos definir', 'queremos hablar',
  'vamos a hablar', 'vamos a revisar', 'vamos a definir',
];

const COMMITMENT_TRIGGERS: string[] = [
  'se compromete', 'se comprometio', 'se comprometieron',
  'queda pendiente', 'quedan pendientes', 'quedamos en',
  'queda encargado', 'queda encargada', 'queda responsable',
  'va a encargarse', 'va a hacer', 'van a hacer',
  'debe enviar', 'debe hacer', 'debe revisar', 'debe presentar',
  'tiene que enviar', 'tiene que hacer', 'tiene que revisar',
  'tienen que', 'hay que', 'es necesario que', 'se necesita que',
  'se acuerda', 'se acordó', 'se acordo', 'se acordaron',
  'como acuerdo', 'como compromiso', 'tarea de', 'tarea para',
  'responsable de', 'encargado de', 'encargada de',
  'antes del', 'para el lunes', 'para el martes', 'para el miercoles',
  'para el jueves', 'para el viernes', 'para el proximo', 'proxima semana',
  'a mas tardar', 'fecha limite', 'plazo de', 'entrega de',
  'pendiente de', 'pendiente por', 'queda por', 'falta por',
];

const TOPIC_STARTERS: string[] = [
  'se hablo de', 'se hablo sobre', 'se menciono', 'se mencionó',
  'se discutio', 'se discutió', 'se presento', 'se presentó',
  'en cuanto a', 'con respecto a', 'sobre el tema', 'sobre la situacion',
  'respecto al', 'respecto a la', 'en relacion a', 'relacionado con',
];

// ── Utilidades ────────────────────────────────────────────────────────────

function norm(text: string): string {
  return text.toLowerCase()
    .normalize('NFD').replace(/[̀-ͯ]/g, '')
    .replace(/[^a-z0-9\s]/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

function capitalize(s: string): string {
  if (!s) return s;
  return s.charAt(0).toUpperCase() + s.slice(1).replace(/\s+$/, '');
}

function extractChunk(rawText: string, keywordStart: number, charsAfter = 180): string {
  const chunkEnd = Math.min(rawText.length, keywordStart + charsAfter);
  let chunk = rawText.substring(keywordStart, chunkEnd).trim();
  // Remove incomplete trailing word
  const lastSpace = chunk.lastIndexOf(' ');
  if (lastSpace > 60 && chunkEnd < rawText.length) chunk = chunk.substring(0, lastSpace);
  return chunk;
}

function wordsAroundKeyword(rawText: string, normText: string, kw: string, windowWords = 20): string {
  const pos = normText.indexOf(norm(kw));
  if (pos < 0) return '';
  // Find approximate word position in original text
  const beforeKw = rawText.substring(0, pos);
  const wordsBefore = beforeKw.split(/\s+/);
  const startWord = Math.max(0, wordsBefore.length - 3);
  const allWords = rawText.split(/\s+/);
  const endWord = Math.min(allWords.length, startWord + windowWords);
  return allWords.slice(startWord, endWord).join(' ');
}

function alreadyCaptured(list: string[], text: string): boolean {
  const normNew = norm(text).substring(0, 40);
  return list.some(existing => norm(existing).substring(0, 40) === normNew);
}

// ── Algoritmo principal ───────────────────────────────────────────────────

export function generateMeetingReport(rawTranscript: string): MeetingReport {
  const normText = norm(rawTranscript);
  const objectives: string[] = [];
  const commitments: string[] = [];
  const topics: string[] = [];

  // 1. Buscar objetivos ────────────────────────────────────────────────────
  for (const trigger of OBJECTIVE_TRIGGERS) {
    const pos = normText.indexOf(norm(trigger));
    if (pos >= 0) {
      const chunk = extractChunk(rawTranscript, pos, 200);
      if (chunk.split(' ').length >= 4 && !alreadyCaptured(objectives, chunk)) {
        objectives.push(capitalize(chunk));
        if (objectives.length >= 4) break;
      }
    }
  }

  // 2. Buscar compromisos ──────────────────────────────────────────────────
  for (const trigger of COMMITMENT_TRIGGERS) {
    const normTrigger = norm(trigger);
    let searchFrom = 0;
    while (searchFrom < normText.length) {
      const pos = normText.indexOf(normTrigger, searchFrom);
      if (pos < 0) break;
      // Retroceder para incluir sujeto (~4 palabras antes)
      const beforeText = rawTranscript.substring(0, pos);
      const prevWords = beforeText.trimEnd().split(/\s+/).slice(-4).join(' ');
      const chunk = (prevWords + ' ' + extractChunk(rawTranscript, pos, 180)).trim();
      if (chunk.split(' ').length >= 5 && !alreadyCaptured(commitments, chunk)) {
        commitments.push(capitalize(chunk));
      }
      searchFrom = pos + normTrigger.length;
      if (commitments.length >= 8) break;
    }
    if (commitments.length >= 8) break;
  }

  // 3. Temas detectados ────────────────────────────────────────────────────
  for (const trigger of TOPIC_STARTERS) {
    const pos = normText.indexOf(norm(trigger));
    if (pos >= 0) {
      const chunk = extractChunk(rawTranscript, pos, 200);
      if (chunk.split(' ').length >= 5 && !alreadyCaptured(topics, chunk)) {
        topics.push(capitalize(chunk));
        if (topics.length >= 6) break;
      }
    }
  }

  // 4. Si no hay temas explícitos, segmentar el texto en bloques temáticos ─
  if (topics.length === 0) {
    const words = rawTranscript.split(/\s+/).filter(Boolean);
    const chunkSize = 30;
    for (let i = 0; i < words.length && topics.length < 6; i += chunkSize) {
      const block = words.slice(i, i + chunkSize).join(' ');
      // Saltar bloques que ya están en objetivos o compromisos
      const normBlock = norm(block);
      const alreadyUsed =
        objectives.some(o => norm(o).includes(normBlock.substring(0, 20))) ||
        commitments.some(c => norm(c).includes(normBlock.substring(0, 20)));
      if (!alreadyUsed && block.split(' ').length >= 8) {
        topics.push(capitalize(block));
      }
    }
  }

  // 5. Resumen ejecutivo ───────────────────────────────────────────────────
  const summaryParts: string[] = [];
  if (objectives.length > 0) summaryParts.push(objectives[0]);
  if (topics.length > 0) summaryParts.push(topics[0]);
  if (commitments.length > 0) summaryParts.push(`Entre los compromisos: ${commitments[0].toLowerCase()}`);
  const rawSummary = summaryParts.join('. ');
  const summary = rawSummary.length > 450 ? rawSummary.substring(0, 450) + '...' : rawSummary;

  const wordCount = rawTranscript.split(/\s+/).filter(Boolean).length;

  const date = new Date().toLocaleDateString('es-CO', {
    weekday: 'long', year: 'numeric', month: 'long', day: 'numeric',
    hour: '2-digit', minute: '2-digit',
  });

  return { date, objectives, topics, commitments, summary, wordCount };
}

// ── Exportación como texto ────────────────────────────────────────────────

export function formatReportAsTxt(report: MeetingReport): string {
  const line = '─'.repeat(52);
  const bullet = (items: string[]) => items.map(i => `  • ${i}`).join('\n');
  const empty = '  (No identificado en la transcripción)';

  return [
    'INFORME DE REUNIÓN',
    `Fecha: ${report.date}`,
    line,
    '',
    'OBJETIVOS',
    report.objectives.length ? bullet(report.objectives) : empty,
    '',
    'COMPROMISOS Y ACUERDOS',
    report.commitments.length ? bullet(report.commitments) : empty,
    '',
    'TEMAS TRATADOS',
    report.topics.length ? bullet(report.topics) : empty,
    '',
    line,
    'RESUMEN EJECUTIVO',
    report.summary || '(Sin resumen generado)',
    '',
    `Total de palabras transcritas: ${report.wordCount}`,
  ].join('\n');
}
