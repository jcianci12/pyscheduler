import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { Client } from './api/api';
import { NavbarComponent } from "./navbar/navbar.component";
import { AuthService } from './auth/auth.service';
import { CommonModule } from '@angular/common';
import {  OAuthLogger, OAuthModule, OAuthService, UrlHelperService } from 'angular-oauth2-oidc';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, NavbarComponent,CommonModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css', providers: [Client,OAuthModule,AuthService,OAuthService,UrlHelperService]
})
export class AppComponent {
  constructor(private authService: AuthService) { } login() { this.authService.login(); } isAuthenticated(): boolean { return this.authService.isAuthenticated(); }
  get userName(): string | null { 
    return this.authService.userName; 
  }
  title = 'pyscheduler';

}
