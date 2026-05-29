import { Component } from '@angular/core';

@Component({
  selector: 'app-license-expired',
  standalone: false,
  templateUrl: './license-expired.component.html',
  styleUrls: ['./license-expired.component.scss'],
})
export class LicenseExpiredComponent {
  readonly whatsappUrl = 'https://wa.me/573202828836?text=Hola%2C%20necesito%20renovar%20mi%20plan%20de%20OmniWorks';
  readonly websiteUrl  = 'https://www.onmiteksolutions.com';
  readonly email       = 'info@onmiteksolutions.com';

  expirationDate: string | null = null;
  readonly year = new Date().getFullYear();

  constructor() {
    const raw = sessionStorage.getItem('license_expiration');
    if (raw) {
      try {
        const d = new Date(raw + 'T00:00:00');
        this.expirationDate = d.toLocaleDateString('es-CO', {
          day: '2-digit', month: 'long', year: 'numeric',
        });
      } catch { /* ignore */ }
    }
  }
}
