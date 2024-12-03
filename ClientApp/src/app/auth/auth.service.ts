import { Injectable } from '@angular/core';
import { AuthConfig, OAuthService } from 'angular-oauth2-oidc';
import { authConfig } from './auth.config';

@Injectable({
  providedIn: 'root',

})
export class AuthService {
  constructor(private oauthService: OAuthService) {
    this.configure();
  }

  public configure() {
    this.oauthService.configure(authConfig);
    this.oauthService.loadDiscoveryDocumentAndTryLogin().then((_) => {
      this.oauthService.tryLoginImplicitFlow().then((_) => { 
        if(!this.oauthService.hasValidAccessToken()) {
          this.oauthService.initLoginFlow();
        }
        else{
          this.oauthService.loadUserProfile().then((userProfile) => {
            console.log(userProfile);
          });
        }
      });
    });
  }

  login() {
    this.oauthService.initCodeFlow();
  }
  logout() {
    this.oauthService.logOut();
  }

  isAuthenticated(): boolean {
    return this.oauthService.hasValidAccessToken();
  }
  getAccessToken(): string | null {
    return this.oauthService.getAccessToken();
  }


  get userName(): string | null {
    const claims = this.oauthService.getIdentityClaims();
    return claims ? claims['name'] : null;
  }
}
