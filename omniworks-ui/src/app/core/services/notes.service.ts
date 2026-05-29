import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { Note, NoteCategory, NoteHistory, NoteFilters, NoteAIResult } from '../models/note.model';

@Injectable({ providedIn: 'root' })
export class NotesService {
  private readonly API = `${environment.apiUrl}/notes`;

  constructor(private http: HttpClient) {}

  // ── Categorías ────────────────────────────────────────────────────────────
  getCategories(): Observable<NoteCategory[]> {
    return this.http.get<NoteCategory[]>(`${this.API}/categories/`);
  }

  createCategory(data: Partial<NoteCategory>): Observable<NoteCategory> {
    return this.http.post<NoteCategory>(`${this.API}/categories/`, data);
  }

  deleteCategory(id: number): Observable<void> {
    return this.http.delete<void>(`${this.API}/categories/${id}/`);
  }

  // ── Notas ────────────────────────────────────────────────────────────────
  getNotes(filters?: NoteFilters): Observable<Note[]> {
    let params = new HttpParams();
    if (filters?.search) params = params.set('search', filters.search);
    if (filters?.type)   params = params.set('type', filters.type);
    if (filters?.category != null) params = params.set('category', String(filters.category));
    if (filters?.pinned) params = params.set('pinned', 'true');
    return this.http.get<Note[]>(`${this.API}/`, { params });
  }

  getNote(id: number): Observable<Note> {
    return this.http.get<Note>(`${this.API}/${id}/`);
  }

  createNote(data: Partial<Note>): Observable<Note> {
    return this.http.post<Note>(`${this.API}/`, data);
  }

  updateNote(id: number, data: Partial<Note>): Observable<Note> {
    return this.http.patch<Note>(`${this.API}/${id}/`, data);
  }

  deleteNote(id: number): Observable<unknown> {
    return this.http.delete(`${this.API}/${id}/`);
  }

  togglePin(id: number): Observable<{ is_pinned: boolean }> {
    return this.http.post<{ is_pinned: boolean }>(`${this.API}/${id}/pin/`, {});
  }

  // ── Historial ─────────────────────────────────────────────────────────────
  getHistory(noteId: number): Observable<NoteHistory[]> {
    return this.http.get<NoteHistory[]>(`${this.API}/${noteId}/history/`);
  }

  restoreHistory(noteId: number, historyId: number): Observable<Note> {
    return this.http.post<Note>(`${this.API}/${noteId}/history/${historyId}/restore/`, {});
  }

  // ── IA Empresarial ────────────────────────────────────────────────────────
  processWithAI(noteId: number, action: string): Observable<NoteAIResult> {
    return this.http.post<NoteAIResult>(`${this.API}/${noteId}/ai/process/`, { action });
  }

  getAIHistory(noteId: number): Observable<NoteAIResult[]> {
    return this.http.get<NoteAIResult[]>(`${this.API}/${noteId}/ai/`);
  }

  // ── Papelera ──────────────────────────────────────────────────────────────
  getTrash(): Observable<Note[]> {
    return this.http.get<Note[]>(`${this.API}/trash/`);
  }

  restoreNote(id: number): Observable<unknown> {
    return this.http.post(`${this.API}/${id}/restore/`, {});
  }
}
