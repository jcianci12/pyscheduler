import { Routes } from '@angular/router';
import { PeopleComponent } from './people/people.component';
import { TasksComponent } from './tasks/tasks.component';
import { EventsComponent } from './events/events.component';
import { AssignmentsComponent } from './assignment/assignments.component';
import { UnavailabilityComponent } from './unavailability/unavailability.component';

export const routes: Routes = [
    { path: 'people', component: PeopleComponent },
    { path: 'tasks', component: TasksComponent },
    { path: 'events', component: EventsComponent },
    { path: 'assignments', component: AssignmentsComponent },
    
    
    {
        path: 'assignments/:id',
        component: AssignmentsComponent
    },
    { path: 'unavailability', component: UnavailabilityComponent }


];

