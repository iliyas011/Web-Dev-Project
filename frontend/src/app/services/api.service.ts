import { Injectable } from '@angular/core';
import { HttpClient, HttpParams, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import {
  User, Category, Listing, Message, Favorite,
  AuthResponse, ListingSearchParams
} from '../models';

@Injectable({ providedIn: 'root' })
export class ApiService {
  private base = 'http://localhost:8000/api';

  constructor(private http: HttpClient) {}

  private handleError(err: HttpErrorResponse): Observable<never> {
    let message = 'An unexpected error occurred.';
    if (err.error) {
      if (typeof err.error === 'string') message = err.error;
      else if (err.error.detail) message = err.error.detail;
      else {
        const msgs: string[] = [];
        for (const key of Object.keys(err.error)) {
          const val = err.error[key];
          msgs.push(`${key}: ${Array.isArray(val) ? val.join(', ') : val}`);
        }
        if (msgs.length) message = msgs.join(' | ');
      }
    }
    return throwError(() => new Error(message));
  }

  

  login(username: string, password: string): Observable<AuthResponse> {
    return this.http.post<AuthResponse>(`${this.base}/auth/login/`, { username, password })
      .pipe(catchError(this.handleError));
  }

  register(username: string, email: string, password: string, password_confirm: string): Observable<AuthResponse> {
    return this.http.post<AuthResponse>(`${this.base}/auth/register/`, { username, email, password, password_confirm })
      .pipe(catchError(this.handleError));
  }

  logout(): Observable<any> {
    return this.http.post(`${this.base}/auth/logout/`, {})
      .pipe(catchError(this.handleError));
  }

  me(): Observable<User> {
    return this.http.get<User>(`${this.base}/auth/me/`)
      .pipe(catchError(this.handleError));
  }



  getCategories(): Observable<Category[]> {
    return this.http.get<Category[]>(`${this.base}/categories/`)
      .pipe(catchError(this.handleError));
  }


  getListings(): Observable<Listing[]> {
    return this.http.get<Listing[]>(`${this.base}/listings/`)
      .pipe(catchError(this.handleError));
  }

  searchListings(params: ListingSearchParams): Observable<Listing[]> {
    let httpParams = new HttpParams();
    if (params.q) httpParams = httpParams.set('q', params.q);
    if (params.category) httpParams = httpParams.set('category', params.category);
    if (params.min_price != null) httpParams = httpParams.set('min_price', params.min_price.toString());
    if (params.max_price != null) httpParams = httpParams.set('max_price', params.max_price.toString());
    if (params.condition) httpParams = httpParams.set('condition', params.condition);
    if (params.ordering) httpParams = httpParams.set('ordering', params.ordering);
    return this.http.get<Listing[]>(`${this.base}/listings/search/`, { params: httpParams })
      .pipe(catchError(this.handleError));
  }

  getListing(id: number): Observable<Listing> {
    return this.http.get<Listing>(`${this.base}/listings/${id}/`)
      .pipe(catchError(this.handleError));
  }

  createListing(data: Partial<Listing> & { category_id: number }): Observable<Listing> {
    return this.http.post<Listing>(`${this.base}/listings/`, data)
      .pipe(catchError(this.handleError));
  }

  updateListing(id: number, data: Partial<Listing>): Observable<Listing> {
    return this.http.put<Listing>(`${this.base}/listings/${id}/`, data)
      .pipe(catchError(this.handleError));
  }

  deleteListing(id: number): Observable<void> {
    return this.http.delete<void>(`${this.base}/listings/${id}/`)
      .pipe(catchError(this.handleError));
  }

  markSold(id: number): Observable<any> {
    return this.http.patch(`${this.base}/listings/${id}/sold/`, {})
      .pipe(catchError(this.handleError));
  }

  getMyListings(): Observable<Listing[]> {
    return this.http.get<Listing[]>(`${this.base}/listings/my/`)
      .pipe(catchError(this.handleError));
  }



  getMessages(): Observable<Message[]> {
    return this.http.get<Message[]>(`${this.base}/messages/`)
      .pipe(catchError(this.handleError));
  }

  sendMessage(listing_id: number, body: string): Observable<Message> {
    return this.http.post<Message>(`${this.base}/messages/`, { listing_id, body })
      .pipe(catchError(this.handleError));
  }



  getFavorites(): Observable<Favorite[]> {
    return this.http.get<Favorite[]>(`${this.base}/favorites/`)
      .pipe(catchError(this.handleError));
  }

  toggleFavorite(listing_id: number): Observable<{ detail: string; favorited: boolean }> {
    return this.http.post<any>(`${this.base}/favorites/`, { listing_id })
      .pipe(catchError(this.handleError));
  }
}
