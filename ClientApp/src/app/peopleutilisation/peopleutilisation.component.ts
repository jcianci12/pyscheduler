import { Component, OnInit } from '@angular/core';
import { Assignment, Client, Person } from '../api/api';
import { CommonModule, JsonPipe } from '@angular/common';
import { AssignmentcountforpersonPipe } from '../assignmentcountforperson.pipe';

@Component({
  selector: 'app-peopleutilisation',
  imports: [ CommonModule],
  templateUrl: './peopleutilisation.component.html',
  styleUrl: './peopleutilisation.component.css'
})
export class PeopleutilisationComponent implements OnInit {
  personAssignments: any;
  constructor(private client: Client) { }
  assignments: Assignment[] = [];
  people: Person[] = [];
  peopleassignments: peopleassignments[] = [];
  ngOnInit(): void {
    this.client.assignmentsAll().subscribe(ass => {
      this.assignments = ass
      this.client.getpeople().subscribe(people => {this.people = people

this.people.forEach(p => {
  this.peopleassignments.push({name: p.first_name + ' ' + p.last_name, value: this.assignments.filter(a => a.person_id == p.id).length});
});
this.peopleassignments.sort((a, b) => b.value - a.value);

      });

    }



    );
    //we need to use this data to get how many times the person is assigned.

  }
}
export interface peopleassignments {
  name: string;
  value: number;
}