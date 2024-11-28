import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { Assignment, Client, Event, Event2, Person, Task } from '../api/api';
import { CommonModule } from '@angular/common';
import { FormControl, FormGroup, Validators, FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { AssignmentrowComponent } from "../assignmentrow/assignmentrow.component";
import { FilterassignmentsbytaskPipe } from '../pipes/filterassignmentsbytask.pipe';
import { CreateassignmentplaceholdersPipe } from '../pipes/createassignmentplaceholders.pipe';
import { GeneratescheduleComponent } from "../generateschedule/generateschedule.component";
import { FilterpeoplebytasksPipe } from '../pipes/filterpeoplebytasks.pipe';
import { PersonbookedpreviousweekPipe } from '../pipes/personbookedpreviousweek.pipe';
import { PeopleComponent } from '../people/people.component';
import { last } from 'rxjs';

@Component({
  selector: 'app-events',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule, FilterassignmentsbytaskPipe,
    FilterpeoplebytasksPipe,
    CreateassignmentplaceholdersPipe,
    PersonbookedpreviousweekPipe
  ],
  templateUrl: './events.component.html',
  styleUrl: './events.component.css'
})
export class EventsComponent implements OnInit {
  events: Event[] | undefined;
  selectedEvents: Event[] = [];
  draftEvents: Event[] = [];
  repeatValue = 1;
  repeatUnit = '604800';
  repeatCount = 5;
  eventForm: FormGroup = new FormGroup({
    id: new FormControl(''),
    event_date: new FormControl('', Validators.required),
    event_name: new FormControl('', Validators.required)
  });
  tasks: Task[] | undefined;
  people: Person[] | undefined;

  constructor(private client: Client, private cdr: ChangeDetectorRef) { }
  async ngOnInit() {
    this.tasks = await this.client.tasksAll().toPromise();
    this.events = await this.client.eventswithassignments().toPromise();
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

  async repeatEvents() {
    const draftEvents: Event2[] = [];
    for (let i = 1; i <= this.repeatCount; i++)
      for (const event of this.selectedEvents) {

        {
          let millisecondstoadd = i * parseInt(this.repeatUnit) * 1000;
          let eventdate = new Date(event.event_date!);
          eventdate.setTime(eventdate.getTime() + millisecondstoadd);
          //generate the date in yyyy-mm-dd

          const newEvent = new Event2({ event_date: eventdate.toISOString().slice(0, 10), event_name: event.event_name });
          draftEvents.push(newEvent);
        }
      }
    this.draftEvents = draftEvents;
  }
  async createEvents() {
    for (const event of this.draftEvents) {
      await this.client.eventsPOST(event).toPromise();
    }
    this.events = await this.client.eventsAll().toPromise();
    this.draftEvents = [];
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
  async assignTasks(event: Event) {
    this.client.allocate(event).subscribe(e => {
      this.events = [...this.events!]; // Create a new array reference
      const index = this.events.findIndex(e => e.id == event.id);
      this.events.find(i => i.id == event.id)!.assignments = e.assignments;
    });
  }

  async deleteEvent(eventId: number) {
    await this.client.eventsDELETE(eventId).toPromise();
    this.events = (this.events ?? []).filter(p => p.id !== eventId);
  }
  async clearEvent(eventId: number) {
    this.events!.find(i => i.id == eventId)!.assignments = [];
    this.events = [...this.events!]
  }

  selectEvent(event: Event) {
    if (this.selectedEvents.includes(event)) {
      this.selectedEvents = this.selectedEvents.filter(e => e.id !== event.id);
    } else {
      this.selectedEvents.push(event);
    }

  }
  isSelected(event: Event) {
    return this.selectedEvents.filter(i => i.id == event.id).length > 0;
  }


  autoassign(event: Event, events: Event[], index: number, suitablePeople: Person[], tasks: Task[]) {
    
    suitablePeople = this.removePeopleBookedLastEvent(events, index, suitablePeople);
  
    // Order the assignments so that the assignment with the fewest people that can do it comes first.
    event.assignments = event.assignments?.sort((a, b) => {
      let acount = suitablePeople.filter(i => i.tasks?.some(t => t.id == a.task_id)).length;
      let bcount = suitablePeople.filter(i => i.tasks?.some(t => t.id == b.task_id)).length;
      return acount - bcount;
    });
    for (const assignment of event.assignments!) {

      if (assignment.person_id == null) {
  
        // Remove people who are already assigned to a task in the current event
        // suitablePeople = suitablePeople.filter(i => !event.assignments!.some(a => a.person_id == i.id));
  
        if (suitablePeople.length > 0) {
          let availablepeople = this.removePeopleThatCantDoTheTask(suitablePeople, assignment.task_id!);

          const randomIndex = Math.floor(Math.random() * availablepeople.length);
          const selectedPerson = availablepeople[randomIndex];
  
          console.log(selectedPerson);
          assignment.person_id = selectedPerson.id;
  
          // Remove the selected person from suitablePeople
          suitablePeople = suitablePeople.filter(i => i.id != selectedPerson.id);
        }
      }
    }
  }

  removePeopleBookedLastEvent(events: Event[], index: number, people: Person[]): Person[] {
    console.log(`Received people:`, people)
    let lastevent = events[index - 1]
    if (lastevent == undefined) {
      console.log(`No previous event to check against, returning all people`)
      return people
    }
    else {
      const removedPeople = people.filter(i => lastevent.assignments!.some(a => a.person_id == i.id))
      console.log(`Removed people who were booked last event:`, removedPeople)
      people = people.filter(i => !removedPeople.includes(i))
      console.log(`Remaining people:`, people)
      return people
    }

  }
  removePeopleBookedThisEvent(assignments: Assignment[], people: Person[]): Person[] {
    people = people.filter(i => assignments.some(a => {
    
      if(a!=null && a.person_id == i.id) {
        return false
      } 
      else{return true}

    }

      
    ))
    return people
  }
  removePeopleThatCantDoTheTask(people: Person[], taskid: number): Person[] {
    people = people.filter(i => i.tasks?.some(t => t.id == taskid))


    return people
  }

}


