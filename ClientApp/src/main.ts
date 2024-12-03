import { bootstrapApplication } from '@angular/platform-browser';
import { HTTP_INTERCEPTORS, provideHttpClient } from '@angular/common/http';
import { RouterModule, provideRouter } from '@angular/router';
import { AppComponent } from './app/app.component';
import { provideOAuthClient, AuthConfig, OAuthModuleConfig } from 'angular-oauth2-oidc';
import { AuthInterceptor } from './app/auth/auth.interceptor';
import { routes } from './app/app.routes';
import { environment } from './app/environments/environment';
import { API_BASE_URL } from './app/api/api';

bootstrapApplication(AppComponent, {
  providers: [
    provideHttpClient(),
    provideRouter(routes), // Provide routes
    provideOAuthClient(),
    // { provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor, multi: true }
    { provide: API_BASE_URL, useValue: environment.baseUrl } // Provide base URL from environment
  ]
  
})
.catch(err => console.error(err));
