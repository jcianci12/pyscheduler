import { Injectable } from '@angular/core';
import { OAuthService } from 'angular-oauth2-oidc';
import { authConfig } from './auth.config';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  constructor(private oauthService: OAuthService) {
    this.configure();
  }

  private configure() {
    this.oauthService.configure(authConfig);
    this.oauthService.loadDiscoveryDocumentAndTryLogin();
    this.oauthService.setupAutomaticSilentRefresh();
  }

  login() {
    
        this.oauthService.initLoginFlow();
      

  }
  logout() { this.oauthService.logOut(); }

  isAuthenticated(): boolean {
    return this.oauthService.hasValidAccessToken();
  }



  get userName(): string | null {
    const claims = this.oauthService.getIdentityClaims();
    return claims ? claims['name'] : null;
  }

  getAccessToken(): string | null {
    return this.oauthService.getAccessToken();
  }

  getIdToken(): string | null {
    return this.oauthService.getIdToken();
  }
}
