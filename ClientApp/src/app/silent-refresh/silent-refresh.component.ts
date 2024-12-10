import { Component } from '@angular/core';
import { OAuthService } from 'angular-oauth2-oidc';

@Component({
  selector: 'app-silent-refresh',
  standalone: true,
  imports: [],
  templateUrl: './silent-refresh.component.html',
  styleUrl: './silent-refresh.component.css'
})
export class SilentRefreshComponent {
  constructor(private oauthService: OAuthService) { }
silentrefresh(){
  this
    .oauthService
    .silentRefresh()
    .then(info => console.debug('refresh ok', info))
    .catch(err => {
      if (err.error === 'consent_required') {
        this.oauthService.initImplicitFlow();
        this.oauthService.loadDiscoveryDocumentAndTryLogin();
      } else {
        console.error('refresh error', err);
      }
    });
}
}
