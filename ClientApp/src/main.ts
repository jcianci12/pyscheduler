import { bootstrapApplication } from '@angular/platform-browser';
import { provideHttpClient } from '@angular/common/http';
import { AppComponent } from './app/app.component';
import { provideOAuthClient, AuthConfig, OAuthModuleConfig } from 'angular-oauth2-oidc';

const authConfig: AuthConfig = {
  issuer: 'https://authentik.tekonline.com.au/application/o/pyscheduler/',
  redirectUri: window.location.origin + '/index.html',
  clientId: 'spa-demo',
  scope: 'openid profile email voucher',
  strictDiscoveryDocumentValidation: false,
  skipIssuerCheck: true
};

const oAuthModuleConfig: OAuthModuleConfig = {
  ...authConfig,
  resourceServer: {
    allowedUrls: ['https://authentik.tekonline.com.au'],
    sendAccessToken: true
  }
};

bootstrapApplication(AppComponent, {
  providers: [
    provideHttpClient(),
    provideOAuthClient(oAuthModuleConfig)
  ]
})
.catch(err => console.error(err));
