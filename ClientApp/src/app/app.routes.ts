import { Routes } from '@angular/router';
import { PeopleComponent } from './people/people.component';
import { TasksComponent } from './tasks/tasks.component';
import { EventsComponent } from './events/events.component';
import { AssignmentsComponent } from './assignment/assignments.component';
import { UnavailabilityComponent } from './unavailability/unavailability.component';
import { HomeComponent } from './home/home.component';
import { AuthGuard } from './auth/auth.guard';
import { LoginComponent } from './login/login.component';
import { SilentRefreshComponent } from './silent-refresh/silent-refresh.component';

export const routes: Routes = [
     { path: '', redirectTo: 'home', pathMatch: 'full' },
     { path: 'home', component: HomeComponent },
    { path: 'login', component: LoginComponent },

    { path: 'people', component: PeopleComponent,canActivate:[AuthGuard] },
    { path: 'tasks', component: TasksComponent,canActivate:[AuthGuard] },
    { path: 'events', component: EventsComponent ,canActivate:[AuthGuard]},
    { path: 'assignments', component: AssignmentsComponent,canActivate:[AuthGuard] },
    { path: 'silent-refresh', component: SilentRefreshComponent },


    {
        path: 'assignments/:id',
        component: AssignmentsComponent,canActivate:[AuthGuard]
    },
    { path: 'unavailability', component: UnavailabilityComponent,canActivate:[AuthGuard] }


];

