import { AuthConfig } from 'angular-oauth2-oidc';

export const authConfig: AuthConfig = {
  issuer: 'https://authentik.tekonline.com.au/application/o/pyscheduler/',
  // tokenEndpoint: 'https://authentik.tekonline.com.au/application/o/token/',
  logoutUrl: 'https://authentik.tekonline.com.au/application/o/pyscheduler/end-session/',
  redirectUri: window.location.origin,
  clientId: 'yJwnySrODx2x1uNDKzszWiTV3ivrLPBdvvDkz1sN',
  responseType: 'code',
  scope: 'openid profile email',
  showDebugInformation: true,
  strictDiscoveryDocumentValidation: false
};
