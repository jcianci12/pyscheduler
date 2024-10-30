import { Component, OnInit } from '@angular/core';
import { Assignment, Client, Event, EventWithAssignments } from '../api/api';
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
  events: EventWithAssignments[] | undefined;
  eventForm: FormGroup = new FormGroup({
    id: new FormControl(''),
    event_date: new FormControl('', Validators.required),
    event_name: new FormControl('', Validators.required)
  });
  tasks: import("c:/Users/jcianci12.DESKTOP-2CKPSCV/Desktop/IT/pyscheduler/ClientApp/pyscheduler/src/app/api/api").Task[] | undefined;
  people: import("c:/Users/jcianci12.DESKTOP-2CKPSCV/Desktop/IT/pyscheduler/ClientApp/pyscheduler/src/app/api/api").Person[] | undefined;

  constructor(private client: Client) { }
  async ngOnInit() {
    this.events = await this.client.eventswithassignments().toPromise();
  }

  async ngAfterViewInit() {
    this.tasks = await this.client.tasksAll().toPromise();
    this.people = await this.client.getpeople().toPromise();

  }
  onPersonSelect(selectedpersonevent?: any, taskid?: number, eventid?: number) {
    let selectedpersonid = Number(selectedpersonevent.target.value);
    //check if there is an assignment for the event
    let event = this.events!.find(e => e.id == eventid);
    let eventassignment = event?.assignments?.find(a => event?.id == taskid);
    if (eventassignment) {
      eventassignment.personid = selectedpersonid;
    }
    else {
      eventassignment = new Assignment({ event_id: eventid, task_id: taskid, person_id: selectedpersonid });
      event!.assignments?.push(eventassignment);
    }
    this.events![eventid!] = event!;

     
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


