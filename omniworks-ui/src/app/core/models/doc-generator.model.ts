export interface DocumentTemplate {
  id: number;
  name: string;
  description: string;
  file: string;
  filename: string;
  variables: string[];
  variable_count: number;
  is_active: boolean;
  created_at: string;
}

export interface DocumentGeneration {
  id: number;
  name: string;
  template: number;
  template_name: string;
  status: 'pending' | 'processing' | 'completed' | 'error';
  total_records: number;
  processed_records: number;
  progress_pct: number;
  error_message: string;
  created_at: string;
}

export interface ExcelPreview {
  total: number;
  columns: string[];
  preview: Record<string, string>[];
}
