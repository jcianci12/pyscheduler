import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { Client } from './api/api';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css',providers:[Client]
})
export class AppComponent {
  title = 'pyscheduler';
}
