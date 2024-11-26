import { Component, OnInit } from '@angular/core';
import { Client,   Person,   Person2,   Person3,   Task } from '../api/api';
import { CommonModule } from '@angular/common';
import { FormControl, FormGroup, FormsModule } from '@angular/forms';
import { DuplicatepersonPipe } from '../pipes/duplicateperson.pipe';

@Component({
  selector: 'app-people',
  standalone: true,
  imports: [CommonModule, FormsModule,DuplicatepersonPipe],
  templateUrl: './people.component.html',
  styleUrl: './people.component.css'
})
export class PeopleComponent implements OnInit {
  people: Person[] | undefined;
  tasks: Task[] | undefined;
  personForm: FormGroup = new FormGroup({
    first_name: new FormControl(''),
    last_name: new FormControl('')
  });

  constructor(private client: Client) { }

  async ngOnInit() {
    this.people = await this.client.getpeople().toPromise();
    this.tasks = await this.client.tasksAll().toPromise();
    this.personForm;
  }

  async createPerson(person: Person2) {
    await this.client.createperson(person).toPromise();
    this.people = await this.client.getpeople().toPromise();
  }

  async updatePerson(person: Person) {
    console.log(person);
    await this.client.updateperson(person.id as number, person as Person3 ).toPromise();
    this.people = await this.client.getpeople().toPromise();
  }
  async updateAllPeople() {
    for (const person of this.people ?? []) {
      await this.client.updateperson(person.id as number, person as Person3).toPromise();
    }
    this.people = await this.client.getpeople().toPromise();
  }
onTaskChange(event: Event, person: Person, task: Task) {
  const target = event.target as HTMLInputElement;
  const isChecked = target.checked;
  const tasks = person.tasks ?? [];
  if (isChecked) {
    if (!tasks.includes(task)) {
      person.tasks = [...tasks, task];
    }
  } else {
    person.tasks = tasks.filter(t => t.id !== task.id);
  }
  this.updatePerson(person);
}


  async deletePerson(personId: number) {
    await this.client.deleteperson(personId).toPromise();
    this.people = (this.people ?? []).filter(p => p.id !== personId);
  }
  hasTask(person: Person, task: Task): boolean {
    return person.tasks?.some(t => t.id === task.id) ?? false;
  }
}
