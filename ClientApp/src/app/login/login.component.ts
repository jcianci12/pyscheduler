import { Component } from '@angular/core';
import { OAuthModule, OAuthService, UrlHelperService } from 'angular-oauth2-oidc';
import { Client } from '../api/api';
import { AuthService } from '../auth/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css',
  providers: [Client, OAuthModule, AuthService, OAuthService, UrlHelperService]

})
export class LoginComponent {
  constructor(private authService: AuthService) { }

  login() {
    this.authService.login();
  }
  logout(){
    this.authService.logout();
  }
  isAuthenticated(): boolean {
    return this.authService.isAuthenticated();

  }
  get userName(): string | null {
    return this.authService.userName;
  }
}
