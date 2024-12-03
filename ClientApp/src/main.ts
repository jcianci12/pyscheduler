import { bootstrapApplication } from '@angular/platform-browser';
import { appConfig } from './app/app.config';
import { AppComponent } from './app/app.component';
import { AuthService } from './app/auth/auth.service';

bootstrapApplication(AppComponent, appConfig)
  .then((moduleRef) => {
    const authService = moduleRef.injector.get(AuthService);
    authService.configure();
  })
  .catch((err) => console.error(err));

