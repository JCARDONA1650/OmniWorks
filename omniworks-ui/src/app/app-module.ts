import { NgModule, provideBrowserGlobalErrorListeners } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { ReactiveFormsModule, FormsModule } from '@angular/forms';
import { HTTP_INTERCEPTORS, provideHttpClient, withInterceptorsFromDi } from '@angular/common/http';
import { CommonModule } from '@angular/common';

import { AppRoutingModule } from './app-routing-module';
import { App } from './app';
import { AuthInterceptor } from './core/interceptors/auth.interceptor';

// Layout
import { ShellComponent } from './layout/shell/shell.component';
import { SidebarComponent } from './layout/sidebar/sidebar.component';
import { TopbarComponent } from './layout/topbar/topbar.component';

// Auth
import { LoginComponent } from './auth/login/login.component';

// Dashboard
import { DashboardComponent } from './dashboard/dashboard.component';

// Voice Notes
import { VoiceNotesComponent } from './notes/voice-notes/voice-notes.component';

// Doc Generator
import { DocGeneratorComponent } from './doc-generator/generator/doc-generator.component';

// Email Campaigns
import { CampaignsMainComponent } from './email-campaigns/list/campaigns-main.component';

// Admin
import { AdminUsersComponent } from './admin/users/admin-users.component';


@NgModule({
  declarations: [
    App,
    ShellComponent,
    SidebarComponent,
    TopbarComponent,
    LoginComponent,
    DashboardComponent,
    VoiceNotesComponent,
    DocGeneratorComponent,
    CampaignsMainComponent,
    AdminUsersComponent,
  ],
  imports: [
    BrowserModule,
    CommonModule,
    ReactiveFormsModule,
    FormsModule,
    AppRoutingModule,
  ],
  providers: [
    provideBrowserGlobalErrorListeners(),
    provideHttpClient(withInterceptorsFromDi()),
    {
      provide: HTTP_INTERCEPTORS,
      useClass: AuthInterceptor,
      multi: true,
    },
  ],
  bootstrap: [App],
})
export class AppModule {}
