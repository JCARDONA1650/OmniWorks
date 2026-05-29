import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { DocumentTemplate, DocumentGeneration, ExcelPreview } from '../models/doc-generator.model';

@Injectable({ providedIn: 'root' })
export class DocGeneratorService {
  private readonly API = `${environment.apiUrl}/docs`;

  constructor(private http: HttpClient) {}

  getTemplates(): Observable<DocumentTemplate[]> {
    return this.http.get<DocumentTemplate[]>(`${this.API}/templates/`);
  }

  uploadTemplate(formData: FormData): Observable<DocumentTemplate> {
    return this.http.post<DocumentTemplate>(`${this.API}/templates/`, formData);
  }

  deleteTemplate(id: number): Observable<void> {
    return this.http.delete<void>(`${this.API}/templates/${id}/`);
  }

  getVariables(id: number): Observable<{ variables: string[] }> {
    return this.http.get<{ variables: string[] }>(`${this.API}/templates/${id}/variables/`);
  }

  generateSingle(templateId: number, data: Record<string, string>): Observable<Blob> {
    return this.http.post(`${this.API}/templates/${templateId}/generate/`, { data }, { responseType: 'blob' });
  }

  generateBulkFromExcel(templateId: number, excelFile: File): Observable<Blob> {
    const formData = new FormData();
    formData.append('excel', excelFile);
    return this.http.post(`${this.API}/templates/${templateId}/bulk/`, formData, { responseType: 'blob' });
  }

  generateBulkFromData(templateId: number, records: Record<string, string>[]): Observable<Blob> {
    return this.http.post(`${this.API}/templates/${templateId}/bulk/`, { records }, { responseType: 'blob' });
  }

  previewExcel(file: File): Observable<ExcelPreview> {
    const formData = new FormData();
    formData.append('excel', file);
    return this.http.post<ExcelPreview>(`${this.API}/import/preview/`, formData);
  }

  getGenerations(): Observable<DocumentGeneration[]> {
    return this.http.get<DocumentGeneration[]>(`${this.API}/generations/`);
  }

  getSampleTemplates(): Observable<{ key: string; name: string }[]> {
    return this.http.get<{ key: string; name: string }[]>(`${this.API}/samples/`);
  }

  downloadSampleTemplate(key: string, name: string): void {
    this.http.get(`${this.API}/samples/${key}/download/`, { responseType: 'blob' }).subscribe(blob => {
      this.downloadBlob(blob, `${name}.docx`);
    });
  }

  downloadBlob(blob: Blob, filename: string): void {
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
  }
}
