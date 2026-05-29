const OFFENSIVE_WORDS: string[] = [
  'mierda', 'puta', 'puto', 'hijueputa', 'verga', 'culo', 'pendejo',
  'pendeja', 'idiota', 'estupido', 'estupida', 'cabron', 'cabrona',
  'joder', 'hostia', 'cono', 'marica', 'hijodeputa', 'carajo', 'chingada',
  'chinga', 'culero', 'marica', 'mamon', 'mamona', 'pinche', 'ojete',
  'gonorrea', 'hijuemadre', 'malparido', 'malparida', 'guevon', 'guevona',
  'sapo', 'imbecil', 'bobo', 'bruto', 'animal', 'bestia', 'burro',
];

export function filterOffensiveWords(text: string): string {
  let result = text;
  for (const word of OFFENSIVE_WORDS) {
    // Match word with possible trailing 's' and accent variations
    const escaped = word.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const regex = new RegExp(`\\b${escaped}[sa]?\\b`, 'gi');
    result = result.replace(regex, '***');
  }
  return result;
}
