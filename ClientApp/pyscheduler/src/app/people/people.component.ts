import { Component, OnInit } from '@angular/core';
import { Client, Person } from '../api/api';
import { CommonModule } from '@angular/common';
import { FormControl, FormGroup,FormsModule } from '@angular/forms';

@Component({
  selector: 'app-people',
  standalone: true,
  imports: [CommonModule,FormsModule],
  templateUrl: './people.component.html',
  styleUrl: './people.component.css'
})
export class PeopleComponent implements OnInit {
  people: Person[] | undefined;
  personForm: FormGroup= new FormGroup({
    first_name: new FormControl(''),
    last_name: new FormControl('')
  });

  constructor(private client: Client) { }
  async ngOnInit() {
    this.people = await this.client.peopleAll().toPromise();
    this.personForm 
  }

  async createPerson(person: Person) {
    await this.client.peoplePOST(person).toPromise();
    this.people = await this.client.peopleAll().toPromise();
  }

  async updatePerson(person: Person) {
    await this.client.peoplePUT(person.id as number, person).toPromise();
    this.people = await this.client.peopleAll().toPromise();
  }

  async deletePerson(personId: number) {
    await this.client.peopleDELETE(personId).toPromise();
    this.people = (this.people ?? []).filter(p => p.id !== personId);  }
}