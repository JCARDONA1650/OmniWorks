import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AuthGuard } from './core/guards/auth.guard';
import { GuestGuard } from './core/guards/guest.guard';
import { AdminGuard } from './core/guards/admin.guard';
import { ShellComponent } from './layout/shell/shell.component';
import { LoginComponent } from './auth/login/login.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { VoiceNotesComponent } from './notes/voice-notes/voice-notes.component';
import { DocGeneratorComponent } from './doc-generator/generator/doc-generator.component';
import { CampaignsMainComponent } from './email-campaigns/list/campaigns-main.component';
import { AdminUsersComponent } from './admin/users/admin-users.component';

const routes: Routes = [
  { path: 'login', component: LoginComponent, canActivate: [GuestGuard] },
  {
    path: '',
    component: ShellComponent,
    canActivate: [AuthGuard],
    children: [
      { path: 'home',            component: DashboardComponent },
      { path: 'notes',           component: VoiceNotesComponent },
      { path: 'doc-generator',   component: DocGeneratorComponent },
      { path: 'email-campaigns', component: CampaignsMainComponent },
      { path: 'admin/users',     component: AdminUsersComponent, canActivate: [AdminGuard] },
      { path: '',                redirectTo: 'home', pathMatch: 'full' },
    ],
  },
  { path: '**', redirectTo: 'home' },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
