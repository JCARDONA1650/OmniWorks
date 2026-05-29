OFFENSIVE_WORDS = [
    'mierda', 'puta', 'puto', 'hijueputa', 'hijueputa', 'coño', 'verga',
    'malparido', 'malparida', 'imbecil', 'idiota', 'estupido', 'estupida',
    'pendejo', 'pendeja', 'marica', 'gonorrea', 'hp', 'hdp', 'ctm',
    'bastardo', 'bastarda', 'cabron', 'cabrona', 'joder', 'follar',
]


def contains_offensive_content(text: str) -> bool:
    if not text:
        return False
    normalized = text.lower()
    return any(word in normalized for word in OFFENSIVE_WORDS)
