import { Routes } from '@angular/router';
import { PeopleComponent } from './people/people.component';
import { TasksComponent } from './tasks/tasks.component';
import { EventsComponent } from './events/events.component';

export const routes: Routes = [
    { path: 'people', component: PeopleComponent },
    { path: 'tasks', component: TasksComponent },
    { path: 'events', component: EventsComponent }


];

