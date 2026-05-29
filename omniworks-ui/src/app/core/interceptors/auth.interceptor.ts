import { Injectable } from '@angular/core';
import {
  HttpInterceptor, HttpRequest, HttpHandler,
  HttpEvent, HttpErrorResponse
} from '@angular/common/http';
import { Observable, throwError, BehaviorSubject, TimeoutError } from 'rxjs';
import { catchError, filter, switchMap, take, timeout } from 'rxjs/operators';
import { Router } from '@angular/router';
import { AuthService } from '../services/auth.service';

const REQUEST_TIMEOUT_MS = 8000; // 8 segundos máximo por petición

// null = esperando refresh, false = refresh falló, string = token nuevo
type RefreshState = string | null | false;

@Injectable()
export class AuthInterceptor implements HttpInterceptor {
  private isRefreshing = false;
  private refreshTokenSubject = new BehaviorSubject<RefreshState>(null);

  constructor(private authService: AuthService, private router: Router) {}

  intercept(req: HttpRequest<unknown>, next: HttpHandler): Observable<HttpEvent<unknown>> {
    const token = this.authService.accessToken;
    const authReq = token ? req.clone({ setHeaders: { Authorization: `Bearer ${token}` } }) : req;

    return next.handle(authReq).pipe(
      timeout(REQUEST_TIMEOUT_MS),
      catchError((error) => {
        // Timeout: convierte en HttpErrorResponse con status 0
        if (error instanceof TimeoutError) {
          return throwError(() => new HttpErrorResponse({
            error: { detail: 'La solicitud tardó demasiado. Verifica que el backend esté corriendo en el puerto 8001.' },
            status: 0,
            statusText: 'Timeout',
          }));
        }

        if (error instanceof HttpErrorResponse) {
          if (error.status === 402) {
            const body = error.error;
            if (body?.expiration_date) {
              sessionStorage.setItem('license_expiration', body.expiration_date);
            }
            this.router.navigate(['/license-expired']);
            return throwError(() => error);
          }
          if (error.status === 401 && !req.url.includes('/auth/login/') && !req.url.includes('/auth/refresh/')) {
            return this.handle401(authReq, next);
          }
        }

        return throwError(() => error);
      })
    );
  }

  private handle401(req: HttpRequest<unknown>, next: HttpHandler): Observable<HttpEvent<unknown>> {
    if (!this.isRefreshing) {
      this.isRefreshing = true;
      this.refreshTokenSubject.next(null);

      return this.authService.refreshToken().pipe(
        switchMap((res) => {
          this.isRefreshing = false;
          this.refreshTokenSubject.next(res.access);
          return next.handle(req.clone({ setHeaders: { Authorization: `Bearer ${res.access}` } }));
        }),
        catchError((err) => {
          this.isRefreshing = false;
          // Desbloquea las peticiones en cola señalando fallo (false), evitando deadlock
          this.refreshTokenSubject.next(false);
          this.authService.logout();
          return throwError(() => err);
        })
      );
    }

    return this.refreshTokenSubject.pipe(
      filter((state) => state !== null),
      take(1),
      switchMap((state) => {
        if (state === false) {
          return throwError(() => new HttpErrorResponse({ status: 401, statusText: 'Unauthorized' }));
        }
        return next.handle(req.clone({ setHeaders: { Authorization: `Bearer ${state}` } }));
      })
    );
  }
}
