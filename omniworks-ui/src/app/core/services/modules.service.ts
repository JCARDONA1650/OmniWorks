import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { Module } from '../models/user.model';

@Injectable({ providedIn: 'root' })
export class ModulesService {
  private readonly API = environment.apiUrl;

  constructor(private http: HttpClient) {}

  getMyModules(): Observable<Module[]> {
    return this.http.get<Module[]>(`${this.API}/modules/`);
  }
}
