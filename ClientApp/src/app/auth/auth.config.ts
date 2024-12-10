import { AuthConfig } from 'angular-oauth2-oidc';

export const authConfig: AuthConfig = {
  issuer: 'https://authentik.tekonline.com.au/application/o/pyscheduler/',
  tokenEndpoint: 'https://authentik.tekonline.com.au/application/o/token/',
  logoutUrl: 'https://authentik.tekonline.com.au/application/o/pyscheduler/end-session/',
  userinfoEndpoint: 'https://authentik.tekonline.com.au/application/o/userinfo/',

  redirectUri: window.location.origin,
  clientId: 'yJwnySrODx2x1uNDKzszWiTV3ivrLPBdvvDkz1sN',
  dummyClientSecret:'test',

  // responseType: 'code',
  scope: 'email offline_access openid profile ',
  showDebugInformation: true,
  strictDiscoveryDocumentValidation: false,
  silentRefreshRedirectUri: window.location.origin + '/silent-refresh',
  useSilentRefresh:true,
  timeoutFactor: 0.75,
  requestAccessToken:true,
  requireHttps: false
};
