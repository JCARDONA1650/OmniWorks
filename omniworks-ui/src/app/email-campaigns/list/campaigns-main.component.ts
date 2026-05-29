import { Component, OnInit, OnDestroy } from '@angular/core';
import { Subject, interval, of } from 'rxjs';
import { takeUntil, switchMap, startWith, catchError } from 'rxjs/operators';
import { EmailCampaignsService } from '../../core/services/email-campaigns.service';
import {
  EmailCampaign, EmailTemplate, SMTPConfig,
  CampaignLog, EmailRecipient, CAMPAIGN_STATUS_LABELS,
} from '../../core/models/email-campaign.model';

type View = 'list' | 'new-campaign' | 'sending' | 'templates' | 'smtp';

@Component({
  selector: 'app-campaigns-main',
  standalone: false,
  templateUrl: './campaigns-main.component.html',
  styleUrls: ['./campaigns-main.component.scss'],
})
export class CampaignsMainComponent implements OnInit, OnDestroy {
  view: View = 'list';

  campaigns: EmailCampaign[] = [];
  templates: EmailTemplate[] = [];
  smtpConfigs: SMTPConfig[] = [];

  selectedCampaign: EmailCampaign | null = null;
  logs: CampaignLog[] = [];
  recipients: EmailRecipient[] = [];
  lastLogId = 0;

  loading = false;
  loadError = '';
  saving = false;
  importing = false;
  testingSmtp = false;
  smtpTestMsg = '';

  readonly statusLabels = CAMPAIGN_STATUS_LABELS;

  // Form nueva campaña
  campaignForm = { name: '', template: null as number | null, smtp_config: null as number | null, batch_size: 10, delay_seconds: 5 };
  importMode: 'excel' | 'manual' = 'excel';
  importFile: File | null = null;
  importEmailField = 'email';
  manualEmails = '';

  // Form plantilla
  templateForm = { name: '', subject: '', html_body: '', text_body: '' };
  editingTemplate: EmailTemplate | null = null;

  // Form SMTP
  smtpForm = { name: '', host: '', port: 587, use_tls: true, use_ssl: false, username: '', password: '', from_name: '', from_email: '', is_default: false };
  editingSmtp: SMTPConfig | null = null;

  private destroy$ = new Subject<void>();
  private pollStop$ = new Subject<void>();

  constructor(private svc: EmailCampaignsService) {}

  ngOnInit(): void {
    this.loadAll();
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
    this.pollStop$.next();
  }

  loadAll(): void {
    this.loading = true;
    this.loadError = '';
    // Carga campañas primero para mostrar la lista cuanto antes
    this.svc.getCampaigns().pipe(catchError(() => of([]))).subscribe({
      next: (res) => {
        this.campaigns = res;
        this.loading = false;
      },
    });
    // Plantillas y SMTP se cargan en paralelo sin bloquear la UI
    this.svc.getTemplates().pipe(catchError(() => of([]))).subscribe(t => (this.templates = t));
    this.svc.getSMTPConfigs().pipe(catchError(() => of([]))).subscribe(s => (this.smtpConfigs = s));
  }

  // ── Crear campaña ─────────────────────────────────────────────────────
  saveCampaign(): void {
    if (!this.campaignForm.name.trim()) return;
    this.saving = true;
    this.svc.createCampaign(this.campaignForm).subscribe({
      next: (c) => {
        this.campaigns.unshift(c);
        this.selectedCampaign = c;
        this.saving = false;
        this.view = 'list';
        this.resetCampaignForm();
      },
      error: () => (this.saving = false),
    });
  }

  resetCampaignForm(): void {
    this.campaignForm = { name: '', template: null, smtp_config: null, batch_size: 10, delay_seconds: 5 };
    this.importFile = null;
    this.manualEmails = '';
  }

  // ── Importar destinatarios ─────────────────────────────────────────────
  onFileChange(event: Event): void {
    this.importFile = (event.target as HTMLInputElement).files?.[0] || null;
  }

  importRecipients(campaignId: number): void {
    if (this.importMode === 'excel' && this.importFile) {
      this.importing = true;
      this.svc.importRecipientsExcel(campaignId, this.importFile, this.importEmailField).subscribe({
        next: (res) => { this.importing = false; this.loadCampaignDetail(campaignId); alert(`${res.imported} destinatarios importados.`); },
        error: () => (this.importing = false),
      });
    } else if (this.importMode === 'manual' && this.manualEmails.trim()) {
      const recipients = this.manualEmails.split('\n')
        .map(line => line.trim()).filter(e => e.includes('@'))
        .map(email => ({ email }));
      if (!recipients.length) return;
      this.importing = true;
      this.svc.importRecipientsJSON(campaignId, recipients).subscribe({
        next: (res) => { this.importing = false; this.loadCampaignDetail(campaignId); alert(`${res.imported} destinatarios importados.`); },
        error: () => (this.importing = false),
      });
    }
  }

  loadCampaignDetail(id: number): void {
    this.svc.getCampaignStatus(id).subscribe(c => {
      this.selectedCampaign = c;
      const idx = this.campaigns.findIndex(x => x.id === id);
      if (idx >= 0) this.campaigns[idx] = c;
    });
    this.svc.getRecipients(id).subscribe(r => (this.recipients = r.recipients.slice(0, 50)));
  }

  // ── Control de envío ─────────────────────────────────────────────────
  openSending(campaign: EmailCampaign): void {
    this.selectedCampaign = campaign;
    this.logs = [];
    this.lastLogId = 0;
    this.view = 'sending';
    this.loadCampaignDetail(campaign.id);
    this.startPolling(campaign.id);
  }

  startPolling(id: number): void {
    this.pollStop$.next();

    interval(2500).pipe(
      startWith(0),
      takeUntil(this.pollStop$),
      takeUntil(this.destroy$),
      switchMap(() => this.svc.getCampaignStatus(id).pipe(catchError(() => of(null)))),
    ).subscribe(c => {
      if (!c) return;
      this.selectedCampaign = c;
      const idx = this.campaigns.findIndex(x => x.id === id);
      if (idx >= 0) this.campaigns[idx] = c;
    });

    interval(2500).pipe(
      startWith(0),
      takeUntil(this.pollStop$),
      takeUntil(this.destroy$),
      switchMap(() => this.svc.getLogs(id, this.lastLogId).pipe(catchError(() => of([])))),
    ).subscribe(newLogs => {
      if (newLogs.length) {
        this.logs = [...this.logs, ...newLogs].slice(-200);
        this.lastLogId = newLogs[newLogs.length - 1].id;
      }
    });
  }

  stopPolling(): void { this.pollStop$.next(); }

  start(): void {
    if (!this.selectedCampaign) return;
    this.svc.startCampaign(this.selectedCampaign.id).subscribe(c => (this.selectedCampaign = c));
  }

  pause(): void {
    if (!this.selectedCampaign) return;
    this.svc.pauseCampaign(this.selectedCampaign.id).subscribe(c => (this.selectedCampaign = c));
  }

  resume(): void {
    if (!this.selectedCampaign) return;
    this.svc.resumeCampaign(this.selectedCampaign.id).subscribe(c => (this.selectedCampaign = c));
  }

  stop(): void {
    if (!this.selectedCampaign) return;
    this.svc.stopCampaign(this.selectedCampaign.id).subscribe(c => (this.selectedCampaign = c));
  }

  exportResults(): void {
    if (!this.selectedCampaign) return;
    this.svc.exportResults(this.selectedCampaign.id).subscribe(blob =>
      this.svc.downloadBlob(blob, `${this.selectedCampaign!.name}_resultados.xlsx`)
    );
  }

  deleteCampaign(campaign: EmailCampaign): void {
    if (!confirm(`¿Eliminar la campaña "${campaign.name}"?`)) return;
    this.svc.deleteCampaign(campaign.id).subscribe(() => {
      this.campaigns = this.campaigns.filter(c => c.id !== campaign.id);
    });
  }

  backToList(): void {
    this.stopPolling();
    this.view = 'list';
    this.selectedCampaign = null;
  }

  // ── Plantillas ────────────────────────────────────────────────────────
  saveTemplate(): void {
    if (!this.templateForm.name.trim() || !this.templateForm.subject.trim()) return;
    this.saving = true;
    const obs = this.editingTemplate
      ? this.svc.updateTemplate(this.editingTemplate.id, this.templateForm)
      : this.svc.createTemplate(this.templateForm);
    obs.subscribe({
      next: (t) => {
        if (this.editingTemplate) {
          const idx = this.templates.findIndex(x => x.id === t.id);
          if (idx >= 0) this.templates[idx] = t;
        } else {
          this.templates.unshift(t);
        }
        this.saving = false;
        this.editingTemplate = null;
        this.templateForm = { name: '', subject: '', html_body: '', text_body: '' };
      },
      error: () => (this.saving = false),
    });
  }

  editTemplate(t: EmailTemplate): void {
    this.editingTemplate = t;
    this.templateForm = { name: t.name, subject: t.subject, html_body: t.html_body, text_body: t.text_body };
  }

  deleteTemplate(t: EmailTemplate): void {
    if (!confirm(`¿Eliminar la plantilla "${t.name}"?`)) return;
    this.svc.deleteTemplate(t.id).subscribe(() => (this.templates = this.templates.filter(x => x.id !== t.id)));
  }

  // ── SMTP ──────────────────────────────────────────────────────────────
  saveSMTP(): void {
    if (!this.smtpForm.name.trim() || !this.smtpForm.host.trim()) return;
    this.saving = true;
    const obs = this.editingSmtp
      ? this.svc.updateSMTP(this.editingSmtp.id, this.smtpForm)
      : this.svc.createSMTP(this.smtpForm);
    obs.subscribe({
      next: (s) => {
        if (this.editingSmtp) {
          const idx = this.smtpConfigs.findIndex(x => x.id === s.id);
          if (idx >= 0) this.smtpConfigs[idx] = s;
        } else {
          this.smtpConfigs.unshift(s);
        }
        this.saving = false;
        this.editingSmtp = null;
        this.resetSmtpForm();
      },
      error: () => (this.saving = false),
    });
  }

  editSMTP(s: SMTPConfig): void {
    this.editingSmtp = s;
    this.smtpForm = { name: s.name, host: s.host, port: s.port, use_tls: s.use_tls, use_ssl: s.use_ssl, username: s.username, password: '', from_name: s.from_name, from_email: s.from_email, is_default: s.is_default };
  }

  testSMTP(s: SMTPConfig): void {
    this.testingSmtp = true;
    this.smtpTestMsg = '';
    this.svc.testSMTP(s.id).subscribe({
      next: (r) => { this.smtpTestMsg = r.detail; this.testingSmtp = false; },
      error: (e) => { this.smtpTestMsg = e.error?.detail || 'Error de conexión'; this.testingSmtp = false; },
    });
  }

  deleteSMTP(s: SMTPConfig): void {
    if (!confirm(`¿Eliminar la configuración "${s.name}"?`)) return;
    this.svc.deleteSMTP(s.id).subscribe(() => (this.smtpConfigs = this.smtpConfigs.filter(x => x.id !== s.id)));
  }

  resetSmtpForm(): void {
    this.smtpForm = { name: '', host: '', port: 587, use_tls: true, use_ssl: false, username: '', password: '', from_name: '', from_email: '', is_default: false };
  }

  // ── Utilidades ────────────────────────────────────────────────────────
  getStatusClass(s: string): string {
    const map: Record<string, string> = {
      draft: 'badge--user', ready: 'badge--admin', running: 'status--running',
      paused: 'status--paused', completed: 'badge--active', error: 'badge--inactive',
    };
    return map[s] || '';
  }

  formatDate(d: string | null): string {
    if (!d) return '—';
    return new Date(d).toLocaleString('es-CO', { day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit' });
  }

  get isRunning(): boolean { return this.selectedCampaign?.status === 'running'; }
  get isPaused(): boolean  { return this.selectedCampaign?.status === 'paused'; }
  get isCompleted(): boolean { return this.selectedCampaign?.status === 'completed'; }
  get canStart(): boolean {
    return ['ready', 'paused'].includes(this.selectedCampaign?.status || '');
  }
}
