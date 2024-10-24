import { Component, OnInit } from '@angular/core';
import { Client, Person } from '../api/api';
@Component({
  selector: 'app-people',
  standalone: true,
  imports: [],
  templateUrl: './people.component.html',
  styleUrl: './people.component.css'
})
export class PeopleComponent implements OnInit {
  people:Person[] = [];
  constructor(private client: Client) { }
  ngOnInit() { this.client.peopleAll().subscribe(people => this.people = people); }
}
