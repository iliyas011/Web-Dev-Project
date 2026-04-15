import { Component } from '@angular/core';
import { RouterOutlet, RouterLink, RouterLinkActive } from '@angular/router';
import { AuthService } from './services/auth.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, RouterLink, RouterLinkActive],
  template: `
    <nav class="navbar">
      <a class="nav-brand" routerLink="/home">
        <span class="brand-icon"><img src="frontend/src/app/kbtu.png" alt="KBTU Logo" /></span> KBTU
      </a>
      <div class="nav-links">
        <a routerLink="/home" routerLinkActive="active">Browse</a>
        @if (auth.isLoggedIn) {
          <a routerLink="/create" routerLinkActive="active">+ Sell</a>
          <a routerLink="/my-listings" routerLinkActive="active">My Ads</a>
          <a routerLink="/favorites" routerLinkActive="active">Saved</a>
          <a routerLink="/messages" routerLinkActive="active">Messages</a>
          <span class="nav-user">{{ auth.currentUser()?.username }}</span>
          <button class="btn-logout" (click)="logout()">Logout</button>
        } @else {
          <a routerLink="/login" routerLinkActive="active">Login</a>
          <a routerLink="/register" class="btn-register" routerLinkActive="active">Sign Up</a>
        }
      </div>
    </nav>
    <main class="main-content">
      <router-outlet />
    </main>
  `,
  styles: [`
    .navbar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 2rem;
      height: 64px;
      background: #070e14;
      border-bottom: 1px solid #2a2a2a;
      position: sticky;
      top: 0;
      z-index: 100;
    }
    .nav-brand {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      font-size: 1.3rem;
      font-weight: 700;
      color: #f0c040;
      text-decoration: none;
      letter-spacing: -0.5px;
    }
    .brand-icon { font-size: 1.5rem; }
    .nav-links {
      display: flex;
      align-items: center;
      gap: 1.5rem;
    }
    .nav-links a {
      color: #aaa;
      text-decoration: none;
      font-size: 0.9rem;
      font-weight: 500;
      transition: color 0.2s;
    }
    .nav-links a:hover, .nav-links a.active { color: #fff; }
    .nav-user {
      color: #f0c040;
      font-size: 0.85rem;
      font-weight: 600;
    }
    .btn-logout {
      background: none;
      border: 1px solid #444;
      color: #aaa;
      padding: 0.3rem 0.8rem;
      border-radius: 4px;
      cursor: pointer;
      font-size: 0.85rem;
      transition: all 0.2s;
    }
    .btn-logout:hover { border-color: #e55; color: #e55; }
    .btn-register {
      background: #f0c040 !important;
      color: #0f0f0f !important;
      padding: 0.3rem 1rem;
      border-radius: 4px;
      font-weight: 600 !important;
    }
    .main-content { min-height: calc(100vh - 64px); }
    
    img { display: block; 
      width: 32px; height: 32px; border-radius: 50%; object-fit: cover; 
      }
  `]
})
export class AppComponent {
  constructor(public auth: AuthService) {}
  logout() { this.auth.logout(); }
}
