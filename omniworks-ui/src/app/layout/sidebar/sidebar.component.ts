import { Component, OnInit } from '@angular/core';
import { Router, NavigationEnd } from '@angular/router';
import { filter } from 'rxjs/operators';
import { AuthService } from '../../core/services/auth.service';
import { ModulesService } from '../../core/services/modules.service';
import { Module, User } from '../../core/models/user.model';

interface NavItem {
  label: string;
  route: string;
  icon: string;
  adminOnly?: boolean;
}

@Component({
  selector: 'app-sidebar',
  standalone: false,
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.scss'],
})
export class SidebarComponent implements OnInit {
  currentUser: User | null = null;
  modules: Module[] = [];
  currentRoute = '';
  collapsed = false;

  readonly staticNav: NavItem[] = [
    { label: 'Inicio', route: '/home', icon: 'home' },
    { label: 'Usuarios', route: '/admin/users', icon: 'users', adminOnly: true },
  ];

  constructor(
    public auth: AuthService,
    private modulesService: ModulesService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.currentUser = this.auth.currentUser;
    this.router.events.pipe(filter(e => e instanceof NavigationEnd)).subscribe((e: any) => {
      this.currentRoute = e.urlAfterRedirects;
    });
    this.currentRoute = this.router.url;
    this.loadModules();
  }

  loadModules(): void {
    this.modulesService.getMyModules().subscribe({
      next: (modules) => (this.modules = modules),
    });
  }

  get visibleNav(): NavItem[] {
    return this.staticNav.filter(item => !item.adminOnly || this.auth.isAdmin);
  }

  isActive(route: string): boolean {
    return this.currentRoute.startsWith(route);
  }

  navigate(route: string): void {
    this.router.navigate([route]);
  }

  logout(): void {
    this.auth.logout();
  }

  getModuleIcon(key: string): string {
    const icons: Record<string, string> = {
      email_campaigns: 'mail',
      notes: 'file-text',
      doc_generator: 'layers',
    };
    return icons[key] || 'box';
  }

  getSidebarIcon(key: string): string { return this.getModuleIcon(key); }
}
