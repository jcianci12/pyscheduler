import { bootstrapApplication } from '@angular/platform-browser';
import { importProvidersFrom } from '@angular/core';
import { appConfig } from './app/app.config';
import { AppComponent } from './app/app.component';
import { AuthModule } from '@auth0/auth0-angular';

bootstrapApplication(AppComponent, {
  ...appConfig,
  providers: [
    ...appConfig.providers,
    importProvidersFrom(
      AuthModule.forRoot({
        domain: 'your-auth0-domain',
        clientId: 'your-auth0-client-id',
      })
    )
  ]
})
.catch((err) => console.error(err));
