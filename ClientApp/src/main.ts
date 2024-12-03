import { bootstrapApplication } from '@angular/platform-browser';
import { HTTP_INTERCEPTORS, provideHttpClient } from '@angular/common/http';
import { AppComponent } from './app/app.component';
import { provideOAuthClient, AuthConfig, OAuthModuleConfig } from 'angular-oauth2-oidc';
import { AuthInterceptor } from './app/auth/auth.interceptor';





bootstrapApplication(AppComponent, {
  providers: [
    provideHttpClient(),
    provideOAuthClient(),
    // { provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor, multi: true }
  ]
})
.catch(err => console.error(err));
