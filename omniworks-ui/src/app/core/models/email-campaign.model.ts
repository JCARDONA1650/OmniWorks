export interface SMTPConfig {
  id: number;
  name: string;
  host: string;
  port: number;
  use_tls: boolean;
  use_ssl: boolean;
  username: string;
  password?: string;
  from_name: string;
  from_email: string;
  is_default: boolean;
  created_at: string;
}

export interface EmailTemplate {
  id: number;
  name: string;
  subject: string;
  html_body: string;
  text_body: string;
  variables: string[];
  created_at: string;
  updated_at: string;
}

export interface EmailCampaign {
  id: number;
  name: string;
  template: number | null;
  template_name: string;
  smtp_config: number | null;
  smtp_name: string;
  status: 'draft' | 'ready' | 'running' | 'paused' | 'completed' | 'error';
  batch_size: number;
  delay_seconds: number;
  total_recipients: number;
  sent_count: number;
  failed_count: number;
  progress_pct: number;
  started_at: string | null;
  completed_at: string | null;
  created_at: string;
  updated_at: string;
}

export interface EmailRecipient {
  id: number;
  email: string;
  variables: Record<string, string>;
  status: 'pending' | 'sent' | 'failed';
  sent_at: string | null;
  error_message: string;
}

export interface CampaignLog {
  id: number;
  level: 'info' | 'success' | 'warning' | 'error';
  message: string;
  created_at: string;
}

export const CAMPAIGN_STATUS_LABELS: Record<string, string> = {
  draft: 'Borrador', ready: 'Lista', running: 'Enviando',
  paused: 'Pausada', completed: 'Completada', error: 'Error',
};
