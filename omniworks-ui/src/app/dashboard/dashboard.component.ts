import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../core/services/auth.service';
import { ModulesService } from '../core/services/modules.service';
import { Module, User } from '../core/models/user.model';

@Component({
  selector: 'app-dashboard',
  standalone: false,
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss'],
})
export class DashboardComponent implements OnInit {
  currentUser: User | null = null;
  modules: Module[] = [];
  loading = true;
  currentHour = new Date().getHours();

  constructor(
    public auth: AuthService,
    private modulesService: ModulesService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.currentUser = this.auth.currentUser;
    this.modulesService.getMyModules().subscribe({
      next: (modules) => {
        this.modules = modules;
        this.loading = false;
      },
      error: () => (this.loading = false),
    });
  }

  get greeting(): string {
    if (this.currentHour < 12) return 'Buenos días';
    if (this.currentHour < 18) return 'Buenas tardes';
    return 'Buenas noches';
  }

  getModuleIcon(key: string): string {
    const icons: Record<string, string> = {
      email_campaigns: 'mail',
      notes: 'file-text',
    };
    return icons[key] || 'box';
  }

  getModuleGradient(index: number): string {
    const gradients = [
      'linear-gradient(135deg, #1e6fff 0%, #38bdf8 100%)',
      'linear-gradient(135deg, #6366f1 0%, #38bdf8 100%)',
      'linear-gradient(135deg, #0ea5e9 0%, #22c55e 100%)',
      'linear-gradient(135deg, #8b5cf6 0%, #1e6fff 100%)',
    ];
    return gradients[index % gradients.length];
  }

  navigate(route: string): void {
    this.router.navigate([route]);
  }
}
