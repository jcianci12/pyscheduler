import { bootstrapApplication } from '@angular/platform-browser';
import { HTTP_INTERCEPTORS, provideHttpClient } from '@angular/common/http';
import { RouterModule, provideRouter } from '@angular/router';
import { AppComponent } from './app/app.component';
import { provideOAuthClient, AuthConfig, OAuthModuleConfig } from 'angular-oauth2-oidc';
import { AuthInterceptor } from './app/auth/auth.interceptor';
import { routes } from './app/app.routes';

bootstrapApplication(AppComponent, {
  providers: [
    provideHttpClient(),
    provideRouter(routes), // Provide routes
    provideOAuthClient(),
    { provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor, multi: true }
  ]
  
})
.catch(err => console.error(err));
