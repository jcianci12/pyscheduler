import { Component, OnInit } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { Client } from './api/api';
import { NavbarComponent } from "./navbar/navbar.component";
import { CommonModule } from '@angular/common';
import { OAuthLogger, OAuthModule, OAuthService, UrlHelperService } from 'angular-oauth2-oidc';
import { HomeComponent } from './home/home.component';
import { PeopleComponent } from './people/people.component';
import { LoginComponent } from './login/login.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, NavbarComponent, CommonModule, LoginComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css',
  providers: [Client, OAuthModule, OAuthService, OAuthService, UrlHelperService]
})
export class AppComponent implements OnInit {
  constructor(public authService: OAuthService) { }

  title = 'pyscheduler';
  ngOnInit(): void {
    this.authService.events.subscribe((event) => console.log(event));
  }
}
