import { AsyncPipe, JsonPipe } from '@angular/common';
import { Component } from '@angular/core';
import { OAuthService } from 'angular-oauth2-oidc';

@Component({
  selector: 'app-silent-refresh',
  standalone: true,
  imports: [AsyncPipe,JsonPipe],
  templateUrl: './silent-refresh.component.html',
  styleUrl: './silent-refresh.component.css'
})
export class SilentRefreshComponent {
  constructor(public oauthService: OAuthService) { }
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
