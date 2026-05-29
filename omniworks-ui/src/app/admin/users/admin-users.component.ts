import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { AuthService } from '../../core/services/auth.service';
import { UsersAdminService, ModulePermission } from '../../core/services/users-admin.service';
import { User } from '../../core/models/user.model';
import { Module } from '../../core/models/user.model';

type Modal = 'none' | 'create' | 'edit' | 'password' | 'modules';

@Component({
  selector: 'app-admin-users',
  standalone: false,
  templateUrl: './admin-users.component.html',
  styleUrls: ['./admin-users.component.scss'],
})
export class AdminUsersComponent implements OnInit {
  users: User[] = [];
  filteredUsers: User[] = [];
  loading = false;
  saving = false;

  searchQuery = '';
  filterRole: 'all' | 'admin' | 'user' = 'all';
  filterStatus: 'all' | 'active' | 'inactive' = 'all';

  modal: Modal = 'none';
  selectedUser: User | null = null;
  modalError = '';
  modalSuccess = '';

  // Módulos
  allModules: Module[] = [];
  userModulePerms: ModulePermission[] = [];
  loadingModules = false;

  createForm: FormGroup;
  editForm: FormGroup;
  passwordForm: FormGroup;

  constructor(
    private fb: FormBuilder,
    public auth: AuthService,
    private svc: UsersAdminService
  ) {
    this.createForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      username: ['', Validators.required],
      first_name: ['', Validators.required],
      last_name: ['', Validators.required],
      role: ['user', Validators.required],
      password: ['', [Validators.required, Validators.minLength(8)]],
      confirm_password: ['', Validators.required],
    });

    this.editForm = this.fb.group({
      first_name: ['', Validators.required],
      last_name: ['', Validators.required],
      username: ['', Validators.required],
      role: ['user', Validators.required],
      is_active: [true],
    });

    this.passwordForm = this.fb.group({
      new_password: ['', [Validators.required, Validators.minLength(8)]],
      confirm_password: ['', Validators.required],
    });
  }

  ngOnInit(): void {
    this.loadUsers();
    this.svc.getAllModules().subscribe(m => (this.allModules = m));
  }

  loadUsers(): void {
    this.loading = true;
    this.svc.getUsers().subscribe({
      next: (users) => {
        this.users = users;
        this.applyFilters();
        this.loading = false;
      },
      error: () => (this.loading = false),
    });
  }

  applyFilters(): void {
    let list = [...this.users];

    if (this.searchQuery.trim()) {
      const q = this.searchQuery.toLowerCase();
      list = list.filter(u =>
        u.full_name.toLowerCase().includes(q) ||
        u.email.toLowerCase().includes(q) ||
        u.username.toLowerCase().includes(q)
      );
    }

    if (this.filterRole !== 'all') {
      list = list.filter(u => u.role === this.filterRole);
    }

    if (this.filterStatus === 'active') {
      list = list.filter(u => u.is_active);
    } else if (this.filterStatus === 'inactive') {
      list = list.filter(u => !u.is_active);
    }

    this.filteredUsers = list;
  }

  // ── Crear usuario ─────────────────────────────────────────────────────
  openCreate(): void {
    this.createForm.reset({ role: 'user' });
    this.modalError = '';
    this.modal = 'create';
  }

  submitCreate(): void {
    if (this.createForm.invalid) { this.createForm.markAllAsTouched(); return; }
    const v = this.createForm.value;
    if (v.password !== v.confirm_password) {
      this.modalError = 'Las contraseñas no coinciden.';
      return;
    }
    this.saving = true;
    this.modalError = '';
    this.svc.createUser(v).subscribe({
      next: (u) => {
        this.users.unshift(u);
        this.applyFilters();
        this.saving = false;
        this.closeModal();
      },
      error: (err) => {
        this.saving = false;
        this.modalError = this.parseError(err);
      },
    });
  }

  // ── Editar usuario ────────────────────────────────────────────────────
  openEdit(user: User): void {
    this.selectedUser = user;
    this.editForm.patchValue({
      first_name: user.first_name,
      last_name: user.last_name,
      username: user.username,
      role: user.role,
      is_active: user.is_active,
    });
    this.modalError = '';
    this.modal = 'edit';
  }

  submitEdit(): void {
    if (this.editForm.invalid || !this.selectedUser) { this.editForm.markAllAsTouched(); return; }
    this.saving = true;
    this.modalError = '';
    this.svc.updateUser(this.selectedUser.id, this.editForm.value).subscribe({
      next: (u) => {
        const idx = this.users.findIndex(x => x.id === u.id);
        if (idx >= 0) this.users[idx] = u;
        this.applyFilters();
        this.saving = false;
        this.closeModal();
      },
      error: (err) => { this.saving = false; this.modalError = this.parseError(err); },
    });
  }

  // ── Cambiar contraseña ────────────────────────────────────────────────
  openChangePassword(user: User): void {
    this.selectedUser = user;
    this.passwordForm.reset();
    this.modalError = '';
    this.modalSuccess = '';
    this.modal = 'password';
  }

  submitChangePassword(): void {
    if (this.passwordForm.invalid || !this.selectedUser) { this.passwordForm.markAllAsTouched(); return; }
    const v = this.passwordForm.value;
    if (v.new_password !== v.confirm_password) {
      this.modalError = 'Las contraseñas no coinciden.';
      return;
    }
    this.saving = true;
    this.modalError = '';
    this.svc.changePassword(this.selectedUser.id, v.new_password).subscribe({
      next: () => {
        this.saving = false;
        this.modalSuccess = 'Contraseña actualizada correctamente.';
        setTimeout(() => this.closeModal(), 1800);
      },
      error: (err) => { this.saving = false; this.modalError = this.parseError(err); },
    });
  }

  // ── Permisos de módulos ───────────────────────────────────────────────
  openModules(user: User): void {
    this.selectedUser = user;
    this.userModulePerms = [];
    this.loadingModules = true;
    this.modal = 'modules';
    this.svc.getUserModules(user.id).subscribe({
      next: (perms) => { this.userModulePerms = perms; this.loadingModules = false; },
      error: () => (this.loadingModules = false),
    });
  }

  isModuleEnabled(moduleId: number): boolean {
    const perm = this.userModulePerms.find(p => p.module.id === moduleId);
    return perm ? perm.is_enabled : false;
  }

  toggleModule(moduleId: number, isEnabled: boolean): void {
    if (!this.selectedUser) return;
    this.svc.setModulePermission(this.selectedUser.id, moduleId, isEnabled).subscribe({
      next: (perm) => {
        const idx = this.userModulePerms.findIndex(p => p.module.id === moduleId);
        if (idx >= 0) this.userModulePerms[idx] = perm;
        else this.userModulePerms.push(perm);
      },
    });
  }

  // ── Activar/desactivar rápido ─────────────────────────────────────────
  toggleActive(user: User): void {
    if (user.id === this.auth.currentUser?.id) return;
    this.svc.updateUser(user.id, { is_active: !user.is_active }).subscribe({
      next: (u) => {
        const idx = this.users.findIndex(x => x.id === u.id);
        if (idx >= 0) this.users[idx] = u;
        this.applyFilters();
      },
    });
  }

  // ── Utilidades ────────────────────────────────────────────────────────
  closeModal(): void {
    this.modal = 'none';
    this.selectedUser = null;
    this.modalError = '';
    this.modalSuccess = '';
  }

  isCurrentUser(user: User): boolean {
    return user.id === this.auth.currentUser?.id;
  }

  parseError(err: any): string {
    if (!err.error) return 'Error desconocido.';
    if (typeof err.error === 'string') return err.error;
    const msgs = Object.values(err.error).flat();
    return (msgs[0] as string) || 'Error desconocido.';
  }

  formatDate(d: string): string {
    return new Date(d).toLocaleDateString('es-CO', { day: '2-digit', month: 'short', year: 'numeric' });
  }

  get activeCount(): number { return this.users.filter(u => u.is_active).length; }
  get adminCount(): number { return this.users.filter(u => u.is_admin).length; }
}
