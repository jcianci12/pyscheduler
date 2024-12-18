import { Component, OnInit } from '@angular/core';
import { Router, RouterLink, RouterOutlet } from '@angular/router';
import { Client } from './api/api';
import { NavbarComponent } from "./navbar/navbar.component";
import { CommonModule } from '@angular/common';
import { OAuthLogger, OAuthModule, OAuthService, UrlHelperService } from 'angular-oauth2-oidc';
import { HomeComponent } from './home/home.component';
import { PeopleComponent } from './people/people.component';
import { LoginComponent } from './login/login.component';
import {MatMenuModule} from '@angular/material/menu';
import {MatButtonModule} from '@angular/material/button';
import {MatCardModule} from '@angular/material/card';
@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, NavbarComponent, CommonModule, 
     MatButtonModule, MatMenuModule,
    MatCardModule, LoginComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css',
  providers: [Client, OAuthModule, OAuthService, OAuthService, UrlHelperService]
})
export class AppComponent implements OnInit {
  constructor(public authService: OAuthService, private router: Router) { }

  title = 'pyscheduler';
  ngOnInit(): void {
    this.authService.events.subscribe((event) => 
    {
            console.log(event)
if(event.type =='token_expires'){
  
  this.authService.logOut();
  this.router.navigate(['/home']);
}
    }
  );
  }
}
