import { Component, OnInit } from '@angular/core';
import { Client, Event } from '../api/api';
import { CommonModule } from '@angular/common';
import { FormControl, FormGroup, Validators, FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { AssignmentrowComponent } from "../assignmentrow/assignmentrow.component";

@Component({
  selector: 'app-events',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule, AssignmentrowComponent],
  templateUrl: './events.component.html',
  styleUrl: './events.component.css'
})
export class EventsComponent implements OnInit {
  events: Event[] | undefined;
  eventForm: FormGroup = new FormGroup({
    id: new FormControl(''),
    event_date: new FormControl('', Validators.required),
    event_name: new FormControl('', Validators.required)
  });
  tasks: import("c:/Users/jcianci12.DESKTOP-2CKPSCV/Desktop/IT/pyscheduler/ClientApp/pyscheduler/src/app/api/api").Task[] | undefined;
  people: import("c:/Users/jcianci12.DESKTOP-2CKPSCV/Desktop/IT/pyscheduler/ClientApp/pyscheduler/src/app/api/api").Person[] | undefined;

  constructor(private client: Client) { }
  async ngOnInit() {
    this.events = await this.client.eventsAll().toPromise();
    this.eventForm
  }

  async ngAfterViewInit() {
    this.tasks = await this.client.tasksAll().toPromise();
    this.people = await this.client.getpeople().toPromise();

  }
  onPersonSelect(event: any,taskid?:number) {
  }

  
  async createEvent(event: Event) {
    await this.client.eventsPOST(event).toPromise();
    this.events = await this.client.eventsAll().toPromise();
  }

  async updateEvent(event: Event) {
    console.log(event)
    await this.client.eventsPUT(event.id as number, event).toPromise();
    this.events = await this.client.eventsAll().toPromise();
  }

  async deleteEvent(eventId: number) {
    await this.client.eventsDELETE(eventId).toPromise();
    this.events = (this.events ?? []).filter(p => p.id !== eventId);
  }
}


