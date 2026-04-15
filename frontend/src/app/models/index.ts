export interface User {
  id: number;
  username: string;
  email: string;
  date_joined: string;
}

export interface Category {
  id: number;
  name: string;
  slug: string;
  description: string;
  icon: string;
  listing_count: number;
}

export interface Listing {
  id: number;
  title: string;
  description: string;
  price: string;
  condition: 'new' | 'like_new' | 'good' | 'fair' | 'poor';
  location: string;
  image_url: string;
  is_sold: boolean;
  is_active: boolean;
  views_count: number;
  created_at: string;
  updated_at: string;
  seller: User;
  category: Category;
  is_favorited: boolean;
}

export interface Message {
  id: number;
  listing: number;
  listing_title: string;
  sender: User;
  recipient: User;
  body: string;
  is_read: boolean;
  created_at: string;
}

export interface Favorite {
  id: number;
  listing: Listing;
  created_at: string;
}

export interface AuthResponse {
  token: string;
  user: User;
}

export interface ListingSearchParams {
  q?: string;
  category?: string;
  min_price?: number;
  max_price?: number;
  condition?: string;
  ordering?: string;
}

export interface ApiError {
  detail?: string;
  [key: string]: any;
}
