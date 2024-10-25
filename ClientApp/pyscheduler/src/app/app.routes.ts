import { Routes } from '@angular/router';
import { PeopleComponent } from './people/people.component';
import { TasksComponent } from './tasks/tasks.component';

export const routes: Routes = [
    { path: 'people', component: PeopleComponent },
    { path: 'tasks', component: TasksComponent }

];

