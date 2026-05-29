import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import {
  SMTPConfig, EmailTemplate, EmailCampaign,
  EmailRecipient, CampaignLog,
} from '../models/email-campaign.model';

@Injectable({ providedIn: 'root' })
export class EmailCampaignsService {
  private readonly API = `${environment.apiUrl}/campaigns`;

  constructor(private http: HttpClient) {}

  // ── SMTP ─────────────────────────────────────────────────────────────────
  getSMTPConfigs(): Observable<SMTPConfig[]> {
    return this.http.get<SMTPConfig[]>(`${this.API}/smtp/`);
  }
  createSMTP(data: Partial<SMTPConfig>): Observable<SMTPConfig> {
    return this.http.post<SMTPConfig>(`${this.API}/smtp/`, data);
  }
  updateSMTP(id: number, data: Partial<SMTPConfig>): Observable<SMTPConfig> {
    return this.http.patch<SMTPConfig>(`${this.API}/smtp/${id}/`, data);
  }
  deleteSMTP(id: number): Observable<void> {
    return this.http.delete<void>(`${this.API}/smtp/${id}/`);
  }
  testSMTP(id: number): Observable<{ detail: string }> {
    return this.http.post<{ detail: string }>(`${this.API}/smtp/${id}/test/`, {});
  }

  // ── Templates ─────────────────────────────────────────────────────────────
  getTemplates(): Observable<EmailTemplate[]> {
    return this.http.get<EmailTemplate[]>(`${this.API}/templates/`);
  }
  createTemplate(data: Partial<EmailTemplate>): Observable<EmailTemplate> {
    return this.http.post<EmailTemplate>(`${this.API}/templates/`, data);
  }
  updateTemplate(id: number, data: Partial<EmailTemplate>): Observable<EmailTemplate> {
    return this.http.patch<EmailTemplate>(`${this.API}/templates/${id}/`, data);
  }
  deleteTemplate(id: number): Observable<void> {
    return this.http.delete<void>(`${this.API}/templates/${id}/`);
  }

  // ── Campañas ──────────────────────────────────────────────────────────────
  getCampaigns(): Observable<EmailCampaign[]> {
    return this.http.get<EmailCampaign[]>(`${this.API}/`);
  }
  createCampaign(data: Partial<EmailCampaign>): Observable<EmailCampaign> {
    return this.http.post<EmailCampaign>(`${this.API}/`, data);
  }
  updateCampaign(id: number, data: Partial<EmailCampaign>): Observable<EmailCampaign> {
    return this.http.patch<EmailCampaign>(`${this.API}/${id}/`, data);
  }
  deleteCampaign(id: number): Observable<void> {
    return this.http.delete<void>(`${this.API}/${id}/`);
  }
  getCampaignStatus(id: number): Observable<EmailCampaign> {
    return this.http.get<EmailCampaign>(`${this.API}/${id}/status/`);
  }

  // ── Destinatarios ─────────────────────────────────────────────────────────
  getRecipients(id: number): Observable<{ total: number; recipients: EmailRecipient[] }> {
    return this.http.get<any>(`${this.API}/${id}/recipients/`);
  }
  importRecipientsJSON(id: number, recipients: any[], emailField = 'email'): Observable<any> {
    return this.http.post(`${this.API}/${id}/recipients/`, { recipients, email_field: emailField });
  }
  importRecipientsExcel(id: number, file: File, emailField = 'email'): Observable<any> {
    const fd = new FormData();
    fd.append('file', file);
    fd.append('email_field', emailField);
    return this.http.post(`${this.API}/${id}/recipients/`, fd);
  }

  // ── Control ───────────────────────────────────────────────────────────────
  startCampaign(id: number): Observable<EmailCampaign> {
    return this.http.post<EmailCampaign>(`${this.API}/${id}/start/`, {});
  }
  pauseCampaign(id: number): Observable<EmailCampaign> {
    return this.http.post<EmailCampaign>(`${this.API}/${id}/pause/`, {});
  }
  resumeCampaign(id: number): Observable<EmailCampaign> {
    return this.http.post<EmailCampaign>(`${this.API}/${id}/resume/`, {});
  }
  stopCampaign(id: number): Observable<EmailCampaign> {
    return this.http.post<EmailCampaign>(`${this.API}/${id}/stop/`, {});
  }

  // ── Logs ──────────────────────────────────────────────────────────────────
  getLogs(id: number, sinceId = 0): Observable<CampaignLog[]> {
    return this.http.get<CampaignLog[]>(`${this.API}/${id}/logs/?since_id=${sinceId}`);
  }

  // ── Exportar ─────────────────────────────────────────────────────────────
  exportResults(id: number): Observable<Blob> {
    return this.http.get(`${this.API}/${id}/export/`, { responseType: 'blob' });
  }

  downloadBlob(blob: Blob, filename: string): void {
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = filename; a.click();
    URL.revokeObjectURL(url);
  }
}
