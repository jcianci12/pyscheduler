import { AuthConfig } from 'angular-oauth2-oidc';

export const authConfig: AuthConfig = {
  issuer: 'https://authentik.tekonline.com.au/application/o/pyscheduler/',
  redirectUri: window.location.origin,
  clientId: 'yJwnySrODx2x1uNDKzszWiTV3ivrLPBdvvDkz1sN',
  responseType: 'code',
  scope: 'openid profile email',
  showDebugInformation: true
};
