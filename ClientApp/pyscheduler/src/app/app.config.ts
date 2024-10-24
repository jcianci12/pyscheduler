import { ApplicationConfig, provideZoneChangeDetection } from '@angular/core';
import { provideRouter } from '@angular/router';

import { routes } from './app.routes';
import { API_BASE_URL, Client } from './api/api';
import { provideHttpClient, withFetch } from '@angular/common/http';
import { environment } from './environments/environment';

export const appConfig: ApplicationConfig = {
  providers: [provideZoneChangeDetection({ eventCoalescing: true }), provideRouter(routes),
provideHttpClient(withFetch()),
{ provide: API_BASE_URL, useValue: environment.baseUrl },




  ]
};
