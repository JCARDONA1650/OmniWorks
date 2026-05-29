export interface NoteCategory {
  id: number;
  name: string;
  color: string;
  notes_count: number;
}

export interface Note {
  id: number;
  title: string;
  content: string;
  preview?: string;
  note_type: 'quick' | 'report';
  category: number | null;
  category_name: string | null;
  category_color: string | null;
  is_pinned: boolean;
  has_offensive_content: boolean;
  created_at: string;
  updated_at: string;
}

export interface NoteHistory {
  id: number;
  title: string;
  content: string;
  saved_at: string;
}

export interface NoteAIResult {
  id: number;
  action: string;
  original_content: string;
  processed_content: string;
  tokens_used: number;
  provider: string;
  created_at: string;
}

export const AI_ACTIONS = [
  { value: 'summarize',   label: 'Resumir',                icon: 'align-left'    },
  { value: 'improve',     label: 'Mejorar redacción',      icon: 'edit-3'        },
  { value: 'report',      label: 'Convertir a informe',    icon: 'file-text'     },
  { value: 'tasks',       label: 'Extraer tareas',         icon: 'check-square'  },
  { value: 'key_points',  label: 'Puntos clave',           icon: 'target'        },
  { value: 'meeting',     label: 'Acta de reunión',        icon: 'users'         },
];

export interface NoteFilters {
  search?: string;
  type?: 'quick' | 'report' | '';
  category?: number | null;
  pinned?: boolean;
}
