import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { User } from '../models/user.model';
import { Module } from '../models/user.model';

export interface CreateUserPayload {
  email: string;
  username: string;
  first_name: string;
  last_name: string;
  role: 'admin' | 'user';
  password: string;
  confirm_password: string;
}

export interface UpdateUserPayload {
  first_name?: string;
  last_name?: string;
  username?: string;
  role?: 'admin' | 'user';
  is_active?: boolean;
}

export interface ModulePermission {
  id: number;
  module: Module;
  is_enabled: boolean;
}

@Injectable({ providedIn: 'root' })
export class UsersAdminService {
  private readonly API = environment.apiUrl;

  constructor(private http: HttpClient) {}

  getUsers(): Observable<User[]> {
    return this.http.get<User[]>(`${this.API}/users/`);
  }

  getUser(id: number): Observable<User> {
    return this.http.get<User>(`${this.API}/users/${id}/`);
  }

  createUser(data: CreateUserPayload): Observable<User> {
    return this.http.post<User>(`${this.API}/users/`, data);
  }

  updateUser(id: number, data: UpdateUserPayload): Observable<User> {
    return this.http.patch<User>(`${this.API}/users/${id}/`, data);
  }

  deactivateUser(id: number): Observable<{ detail: string }> {
    return this.http.delete<{ detail: string }>(`${this.API}/users/${id}/`);
  }

  changePassword(id: number, newPassword: string): Observable<{ detail: string }> {
    return this.http.post<{ detail: string }>(`${this.API}/users/${id}/change-password/`, {
      new_password: newPassword,
      confirm_password: newPassword,
    });
  }

  getUserModules(userId: number): Observable<ModulePermission[]> {
    return this.http.get<ModulePermission[]>(`${this.API}/admin/users/${userId}/modules/`);
  }

  setModulePermission(userId: number, moduleId: number, isEnabled: boolean): Observable<ModulePermission> {
    return this.http.post<ModulePermission>(`${this.API}/admin/users/${userId}/modules/`, {
      module_id: moduleId,
      is_enabled: isEnabled,
    });
  }

  getAllModules(): Observable<Module[]> {
    return this.http.get<Module[]>(`${this.API}/modules/`);
  }
}
