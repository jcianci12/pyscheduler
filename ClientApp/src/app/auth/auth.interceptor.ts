import { HttpInterceptorFn } from "@angular/common/http";
import { OAuthService } from 'angular-oauth2-oidc';
import { inject } from '@angular/core';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  // Use Angular's inject() function to get the OAuthService
  const oAuthService = inject(OAuthService);
  const token = oAuthService.getAccessToken();
  console.log("Inside authInterceptor");
  console.log("AccessToken:", token); // Log the token to ensure it's retrieved
  
  if (token) {
    const cloned = req.clone({
      headers: req.headers.set('Authorization', `Bearer ${token}`)
    });
    return next(cloned);
  }
  return next(req);
};
