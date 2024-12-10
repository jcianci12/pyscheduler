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

    { path: 'people', component: PeopleComponent },
    { path: 'tasks', component: TasksComponent },
    { path: 'events', component: EventsComponent },
    { path: 'assignments', component: AssignmentsComponent },
    { path: 'silent-refresh1', component: SilentRefreshComponent },


    {
        path: 'assignments/:id',
        component: AssignmentsComponent
    },
    { path: 'unavailability', component: UnavailabilityComponent }


];

