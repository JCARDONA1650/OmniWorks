import { Component, OnInit } from '@angular/core';
import { DocGeneratorService } from '../../core/services/doc-generator.service';
import { DocumentTemplate, DocumentGeneration, ExcelPreview } from '../../core/models/doc-generator.model';

type Step = 'templates' | 'data' | 'generating' | 'history';

@Component({
  selector: 'app-doc-generator',
  standalone: false,
  templateUrl: './doc-generator.component.html',
  styleUrls: ['./doc-generator.component.scss'],
})
export class DocGeneratorComponent implements OnInit {
  templates: DocumentTemplate[] = [];
  generations: DocumentGeneration[] = [];
  selectedTemplate: DocumentTemplate | null = null;

  step: Step = 'templates';
  loading = false;
  generating = false;
  uploadingTemplate = false;

  // Datos manuales
  manualData: Record<string, string> = {};
  dataMode: 'manual' | 'excel' = 'manual';

  // Excel
  excelFile: File | null = null;
  excelPreview: ExcelPreview | null = null;
  loadingPreview = false;

  // Subir plantilla
  showUploadForm = false;
  newTemplateName = '';
  newTemplateDesc = '';
  templateFile: File | null = null;

  // Biblioteca de plantillas de ejemplo
  sampleTemplates: { key: string; name: string }[] = [];
  showLibrary = false;

  constructor(private docService: DocGeneratorService) {}

  ngOnInit(): void {
    this.loadTemplates();
    this.loadHistory();
    this.loadSamples();
  }

  loadSamples(): void {
    this.docService.getSampleTemplates().subscribe({
      next: (s) => (this.sampleTemplates = s),
      error: () => {},
    });
  }

  downloadSample(key: string, name: string): void {
    this.docService.downloadSampleTemplate(key, name);
  }

  loadTemplates(): void {
    this.loading = true;
    this.docService.getTemplates().subscribe({
      next: (t) => { this.templates = t; this.loading = false; },
      error: () => (this.loading = false),
    });
  }

  loadHistory(): void {
    this.docService.getGenerations().subscribe({ next: (g) => (this.generations = g) });
  }

  selectTemplate(tmpl: DocumentTemplate): void {
    this.selectedTemplate = tmpl;
    this.manualData = {};
    tmpl.variables.forEach(v => (this.manualData[v] = ''));
    this.step = 'data';
  }

  back(): void {
    this.step = 'templates';
    this.selectedTemplate = null;
    this.excelFile = null;
    this.excelPreview = null;
  }

  // ── Subir plantilla ────────────────────────────────────────────────────
  onTemplateFileChange(event: Event): void {
    const input = event.target as HTMLInputElement;
    this.templateFile = input.files?.[0] || null;
    if (this.templateFile && !this.newTemplateName) {
      this.newTemplateName = this.templateFile.name.replace('.docx', '');
    }
  }

  uploadTemplate(): void {
    if (!this.templateFile || !this.newTemplateName.trim()) return;
    this.uploadingTemplate = true;
    const fd = new FormData();
    fd.append('file', this.templateFile);
    fd.append('name', this.newTemplateName);
    fd.append('description', this.newTemplateDesc);
    this.docService.uploadTemplate(fd).subscribe({
      next: (t) => {
        this.templates.unshift(t);
        this.showUploadForm = false;
        this.newTemplateName = '';
        this.newTemplateDesc = '';
        this.templateFile = null;
        this.uploadingTemplate = false;
      },
      error: () => (this.uploadingTemplate = false),
    });
  }

  deleteTemplate(event: Event, tmpl: DocumentTemplate): void {
    event.stopPropagation();
    if (!confirm(`¿Eliminar la plantilla "${tmpl.name}"?`)) return;
    this.docService.deleteTemplate(tmpl.id).subscribe({
      next: () => (this.templates = this.templates.filter(t => t.id !== tmpl.id)),
    });
  }

  // ── Excel ──────────────────────────────────────────────────────────────
  onExcelChange(event: Event): void {
    const input = event.target as HTMLInputElement;
    this.excelFile = input.files?.[0] || null;
    this.excelPreview = null;
    if (this.excelFile) this.previewExcel();
  }

  previewExcel(): void {
    if (!this.excelFile) return;
    this.loadingPreview = true;
    this.docService.previewExcel(this.excelFile).subscribe({
      next: (p) => { this.excelPreview = p; this.loadingPreview = false; },
      error: () => (this.loadingPreview = false),
    });
  }

  // ── Generar ────────────────────────────────────────────────────────────
  generateSingle(): void {
    if (!this.selectedTemplate) return;
    this.generating = true;
    this.docService.generateSingle(this.selectedTemplate.id, this.manualData).subscribe({
      next: (blob) => {
        this.docService.downloadBlob(blob, `${this.selectedTemplate!.name}.docx`);
        this.generating = false;
        this.loadHistory();
      },
      error: () => (this.generating = false),
    });
  }

  generateBulk(): void {
    if (!this.selectedTemplate || !this.excelFile) return;
    this.generating = true;
    this.docService.generateBulkFromExcel(this.selectedTemplate.id, this.excelFile).subscribe({
      next: (blob) => {
        this.docService.downloadBlob(blob, `documentos_${this.selectedTemplate!.name}.zip`);
        this.generating = false;
        this.loadHistory();
      },
      error: () => (this.generating = false),
    });
  }

  readonly exampleVar = '{{nombre}}';
  wrap(v: string): string { return '{{' + v + '}}'; }
  trackByVariable(index: number, item: string): string { return item; }
  objectKeys(obj: Record<string, string>): string[] { return Object.keys(obj); }

  formatDate(d: string): string {
    return new Date(d).toLocaleDateString('es-CO', { day: '2-digit', month: 'short', year: 'numeric' });
  }

  getStatusClass(s: string): string {
    const map: Record<string, string> = {
      completed: 'badge--active', error: 'badge--inactive',
      processing: 'badge--admin', pending: 'badge--user',
    };
    return map[s] || '';
  }

  getStatusLabel(s: string): string {
    const map: Record<string, string> = {
      completed: 'Completado', error: 'Error',
      processing: 'Procesando', pending: 'Pendiente',
    };
    return map[s] || s;
  }
}
