import { Routes } from '@angular/router';
import { authGuard } from './guards/auth.guard';

export const routes: Routes = [
  {
    path: '',
    redirectTo: 'home',
    pathMatch: 'full'
  },
  {
    path: 'home',
    loadComponent: () => import('./pages/home/home.component').then(m => m.HomeComponent)
  },
  {
    path: 'listings/:id',
    loadComponent: () => import('./pages/listing-detail/listing-detail.component').then(m => m.ListingDetailComponent)
  },
  {
    path: 'create',
    loadComponent: () => import('./pages/create-listing/create-listing.component').then(m => m.CreateListingComponent),
    canActivate: [authGuard]
  },
  {
    path: 'my-listings',
    loadComponent: () => import('./pages/my-listings/my-listings.component').then(m => m.MyListingsComponent),
    canActivate: [authGuard]
  },
  {
    path: 'messages',
    loadComponent: () => import('./pages/messages/messages.component').then(m => m.MessagesComponent),
    canActivate: [authGuard]
  },
  {
    path: 'favorites',
    loadComponent: () => import('./pages/favorites/favorites.component').then(m => m.FavoritesComponent),
    canActivate: [authGuard]
  },
  {
    path: 'login',
    loadComponent: () => import('./pages/login/login.component').then(m => m.LoginComponent)
  },
  {
    path: 'register',
    loadComponent: () => import('./pages/register/register.component').then(m => m.RegisterComponent)
  },
  {
    path: '**',
    redirectTo: 'home'
  }
];
