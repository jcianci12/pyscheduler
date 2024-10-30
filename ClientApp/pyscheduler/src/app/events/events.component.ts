import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { Assignment, Client, Event, Event2, Task } from '../api/api';
import { CommonModule } from '@angular/common';
import { FormControl, FormGroup, Validators, FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { AssignmentrowComponent } from "../assignmentrow/assignmentrow.component";
import { FilterassignmentsbytaskPipe } from '../pipes/filterassignmentsbytask.pipe';
import { CreateassignmentplaceholdersPipe } from '../pipes/createassignmentplaceholders.pipe';
import { GeneratescheduleComponent } from "../generateschedule/generateschedule.component";

@Component({
  selector: 'app-events',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule, AssignmentrowComponent, FilterassignmentsbytaskPipe, CreateassignmentplaceholdersPipe, GeneratescheduleComponent],
  templateUrl: './events.component.html',
  styleUrl: './events.component.css'
})
export class EventsComponent implements OnInit {
  events: Event[] | undefined;
  selectedEvents: Event[] = [];
  repeatValue = 1;
  repeatUnit = 'days';
  eventForm: FormGroup = new FormGroup({
    id: new FormControl(''),
    event_date: new FormControl('', Validators.required),
    event_name: new FormControl('', Validators.required)
  });
  tasks: import("c:/Users/jcianci12.DESKTOP-2CKPSCV/Desktop/IT/pyscheduler/ClientApp/pyscheduler/src/app/api/api").Task[] | undefined;
  people: import("c:/Users/jcianci12.DESKTOP-2CKPSCV/Desktop/IT/pyscheduler/ClientApp/pyscheduler/src/app/api/api").Person[] | undefined;

  constructor(private client: Client,private cdr:ChangeDetectorRef) { }
 async ngOnInit() {
   this.tasks = await this.client.tasksAll().toPromise();
   this.events = await this.client.eventswithassignments().toPromise();
 }

  async ngAfterViewInit() {
    this.tasks = await this.client.tasksAll().toPromise();
    this.people = await this.client.getpeople().toPromise();
  }
  forceUpdate(event: Event) {
  
    this.events![event.id!] = event;
    this.cdr.detectChanges(); 
  }
selectAll: boolean = false;

selectAllEvents() {
  if (this.selectAll) {
    this.selectedEvents = [...this.events!];
  } else {
    this.selectedEvents = [];
  }
}

repeatEvents(){

}


  async createEvent(event: Event) {
    await this.client.eventsPOST(event).toPromise();
    this.events = await this.client.eventsAll().toPromise();
  }

  async updateEvent(event: Event) {
    event.assignments = event.assignments?.filter(a => a.person_id != null);
    await this.client.eventsPUT(event.id as number, event).toPromise();
    this.events = await this.client.eventsAll().toPromise();
  }

  async deleteEvent(eventId: number) {
    await this.client.eventsDELETE(eventId).toPromise();
    this.events = (this.events ?? []).filter(p => p.id !== eventId);
  }

  selectEvent(event: Event) {
    if (this.selectedEvents.includes(event)) {
      this.selectedEvents = this.selectedEvents.filter(e => e.id !== event.id);
    } else {
      this.selectedEvents.push(event);
    }
  
  }
  isSelected(event: Event) {
    return this.selectedEvents.filter(i=>i.id==event.id).length > 0;
  }
}


