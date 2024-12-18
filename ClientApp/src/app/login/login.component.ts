import { Component } from '@angular/core';
import { OAuthModule, OAuthService, UrlHelperService } from 'angular-oauth2-oidc';
import { Client } from '../api/api';
import { AuthService } from '../auth/auth.service';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule,MatButtonModule],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css',
  providers: [Client,  AuthService,
     OAuthService, UrlHelperService]

})
export class LoginComponent {
  constructor(private authService: AuthService,private oath:OAuthService) { }
currenturl: string = window.location.href;
  login() {
    this.oath.redirectUri = this.currenturl;
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
