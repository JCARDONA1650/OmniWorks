import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../../core/services/auth.service';
import { User } from '../../core/models/user.model';

@Component({
  selector: 'app-topbar',
  standalone: false,
  templateUrl: './topbar.component.html',
  styleUrls: ['./topbar.component.scss'],
})
export class TopbarComponent implements OnInit {
  currentUser: User | null = null;
  pageTitle = '';

  private readonly routeTitles: Record<string, string> = {
    '/home': 'Dashboard',
    '/admin/users': 'Gestión de Usuarios',
    '/email-campaigns': 'Envíos Corporativos',
    '/notes': 'Notas',
  };

  constructor(public auth: AuthService, private router: Router) {}

  ngOnInit(): void {
    this.currentUser = this.auth.currentUser;
    this.updateTitle(this.router.url);
    this.router.events.subscribe(() => this.updateTitle(this.router.url));
  }

  private updateTitle(url: string): void {
    const key = Object.keys(this.routeTitles).find(k => url.startsWith(k));
    this.pageTitle = key ? this.routeTitles[key] : 'OmniWorks';
  }

  logout(): void {
    this.auth.logout();
  }
}
