import { Injectable, signal } from '@angular/core';
import { Router } from '@angular/router';
import { Observable, tap } from 'rxjs';
import { ApiService } from './api.service';
import { User, AuthResponse } from '../models';

const TOKEN_KEY = 'auth_token';
const USER_KEY = 'auth_user';

@Injectable({ providedIn: 'root' })
export class AuthService {
  currentUser = signal<User | null>(this.loadUser());

  constructor(private api: ApiService, private router: Router) {}

  get token(): string | null {
    return localStorage.getItem(TOKEN_KEY);
  }

  get isLoggedIn(): boolean {
    return !!this.token;
  }

  private loadUser(): User | null {
    const raw = localStorage.getItem(USER_KEY);
    return raw ? JSON.parse(raw) : null;
  }

  private saveSession(res: AuthResponse): void {
    localStorage.setItem(TOKEN_KEY, res.token);
    localStorage.setItem(USER_KEY, JSON.stringify(res.user));
    this.currentUser.set(res.user);
  }

  login(username: string, password: string): Observable<AuthResponse> {
    return this.api.login(username, password).pipe(
      tap(res => this.saveSession(res))
    );
  }

  register(username: string, email: string, password: string, passwordConfirm: string): Observable<AuthResponse> {
    return this.api.register(username, email, password, passwordConfirm).pipe(
      tap(res => this.saveSession(res))
    );
  }

  logout(): void {
    this.api.logout().subscribe({
      complete: () => this.clearSession(),
      error: () => this.clearSession(),
    });
  }

  private clearSession(): void {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
    this.currentUser.set(null);
    this.router.navigate(['/login']);
  }
}
