import { bootstrapApplication } from '@angular/platform-browser';
import { provideHttpClient, withFetch, withInterceptors } from '@angular/common/http';
import { RouterModule, provideRouter } from '@angular/router';
import { AppComponent } from './app/app.component';
import { provideOAuthClient } from 'angular-oauth2-oidc';
import { routes } from './app/app.routes';
import { environment } from './app/environments/environment';
import { API_BASE_URL } from './app/api/api';
import { authInterceptor } from './app/auth/auth.interceptor';

bootstrapApplication(AppComponent, {
  providers: [
    provideRouter(routes),
    provideOAuthClient(),
     provideHttpClient(withFetch()
     , withInterceptors([authInterceptor])),


    { provide: API_BASE_URL, useValue: environment.baseUrl }
  ]
})
.catch(err => console.error(err));
