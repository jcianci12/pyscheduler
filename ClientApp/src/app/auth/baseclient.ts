import { Injectable, Inject, Optional } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { OAuthService } from 'angular-oauth2-oidc';
import { API_BASE_URL } from '../api/api';

@Injectable()
export class BaseClient {
  constructor(
    private http: HttpClient,
    private oAuthService: OAuthService,
    @Optional() @Inject(API_BASE_URL) private baseUrl?: string
  ) {}

  transformOptions(options: { headers?: HttpHeaders }): { headers: HttpHeaders } {
    let headers = options.headers || new HttpHeaders();

    const token = this.oAuthService.getAccessToken();
    if (token) {
      headers = headers.set('Authorization', `Bearer ${token}`);
    }

    return { headers };
  }
}
