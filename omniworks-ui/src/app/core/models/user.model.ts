export interface User {
  id: number;
  email: string;
  username: string;
  first_name: string;
  last_name: string;
  full_name: string;
  role: 'admin' | 'user';
  is_admin: boolean;
  is_active: boolean;
  avatar: string | null;
  avatar_url: string | null;
  created_at: string;
}

export interface AuthTokens {
  access: string;
  refresh: string;
  user: User;
}

export interface Module {
  id: number;
  key: string;
  name: string;
  description: string;
  icon: string;
  route: string;
  is_active: boolean;
  order: number;
}
