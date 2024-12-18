import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { Assignment, Client, Event, Event2, Person, Task, Unavailability } from '../api/api';
import { CommonModule } from '@angular/common';
import { FormControl, FormGroup, Validators, FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { FilterassignmentsbytaskPipe } from '../pipes/filterassignmentsbytask.pipe';
import { CreateassignmentplaceholdersPipe } from '../pipes/createassignmentplaceholders.pipe';
import { FilterpeoplebytasksPipe } from '../pipes/filterpeoplebytasks.pipe';
import { PersonbookedpreviousweekPipe } from '../pipes/personbookedpreviousweek.pipe';
import { PersonbookedthiseventPipe } from '../pipes/personbookedthisevent.pipe';
import { MatCardModule } from '@angular/material/card';
import { FiltereventsbydatePipe } from '../../filtereventsbydate.pipe';

@Component({
  selector: 'app-events',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule, FilterassignmentsbytaskPipe,
    FilterpeoplebytasksPipe,
    CreateassignmentplaceholdersPipe,
    PersonbookedpreviousweekPipe, PersonbookedthiseventPipe,
    MatCardModule,FiltereventsbydatePipe
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

  dateFilter: FormGroup = new FormGroup({
    startDate: new FormControl(new Date().toISOString().slice(0, 10)),
    endDate: new FormControl(new Date(new Date().setDate(new Date().getDate() + 7)).toISOString().slice(0, 10))
  });
  tasks: Task[] | undefined;
  people: Person[] | undefined;
  unavailability: Unavailability[] | undefined;

  constructor(private client: Client, private cdr: ChangeDetectorRef) { }
  async ngOnInit() {
    this.tasks = await this.client.tasksAll().toPromise();
    this.events = await this.client.eventswithassignments().toPromise();
    this.people = await this.client.getpeople().toPromise();
    this.unavailability = await this.client.unavailabilityAll().toPromise();
  }


  forceUpdate(event: Event) {

    this.events![event.id!] = event;
    // this.events = [...this.events!];

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


  autoassignbyweek(thisevent: Event, index: number, suitablePeople: Person[], tasks: Task[]) {
    //start with the people that can do the task
    let allevents = this.events!
    suitablePeople = this.removepeopleThatAreUnavailable(suitablePeople, thisevent)
    suitablePeople = this.removePeopleBookedLastEvent(allevents, index, suitablePeople);
    suitablePeople = this.removePeopleBookedThisEvent(thisevent.assignments!, suitablePeople);

    // Order the assignments so that the assignment with the fewest people that can do it comes first.
    thisevent.assignments = thisevent.assignments?.sort((a, b) => {
      let acount = suitablePeople.filter(i => i.tasks?.some(t => t.id == a.task_id)).length;
      let bcount = suitablePeople.filter(i => i.tasks?.some(t => t.id == b.task_id)).length;
      return acount - bcount;
    });
    //loop through the assignments
    for (const assignment of thisevent.assignments!) {

      //if no one is booked the person id will be null
      if (assignment.person_id == null||assignment.person_id==undefined||assignment.person_id as any  as string =='') {

        // Remove people who are already assigned to a task in the current event
        // suitablePeople = suitablePeople.filter(i => !event.assignments!.some(a => a.person_id == i.id));

        if (suitablePeople.length > 0) {
          let availablepeople = this.removePeopleThatCantDoTheTask(suitablePeople, assignment.task_id!);

          const randomIndex = Math.floor(Math.random() * availablepeople.length);
          const selectedPerson = availablepeople[randomIndex];

          console.log(selectedPerson);
          assignment.person_id = selectedPerson.id;

          // We have assigned the person, we can now remove them from the pool of people.
          suitablePeople = suitablePeople.filter(i => i.id != selectedPerson.id);
        }
      }
    }
    

  }
  autoassigntaskforallevents(ev: Event[]) {
    let events = [...ev]
  
    //a list of unnassigned tasks. tasks with fewer people that can do it are at the top
    let unassignedtasks = this.tasks?.sort((a, b) => {
      let acount = this.people!.filter(i => i.tasks?.some(t => t.id == a.id)).length;
      let bcount = this.people!.filter(i => i.tasks?.some(t => t.id == b.id)).length;
      return acount - bcount;
    });
  
    for (let i = 0; i < unassignedtasks!.length; i++) {
      let t = unassignedtasks![i];
      let peoplethatcandothetasks = this.removePeopleThatCantDoTheTask(this.people!, t.id!)
  
      for (let j = 0; j < events.length; j++) {
        let e = events[j];
  
        peoplethatcandothetasks = this.removepeopleThatAreUnavailable(peoplethatcandothetasks!, e)
        // peoplethatcandothetasks = this.removePeopleBookedLastEvent(events, j, peoplethatcandothetasks);
        // peoplethatcandothetasks = this.removepeoplethatarealreadybookedthisevent(e, peoplethatcandothetasks);
        //create empty placeholders for the assignments
        //check if there is an assignment for this task on the current event
        let assignmentfoundindex = e.assignments!.findIndex(ft => ft.task_id == t.id)
        let assignmentfound = e.assignments![assignmentfoundindex]
  
        if (!assignmentfound) {
          let newassignment = new Assignment({ task_id: t.id, event_id: e.id })
          e.assignments?.push(newassignment)
          assignmentfound = newassignment
        }
        let selectedpersonindex = 0
  
        let maxTries = 10;
        while (assignmentfound.person_id == undefined && maxTries > 0) {
          //define a random offset
          let p = this.moduloselectperson(peoplethatcandothetasks!, selectedpersonindex)
          //checks
          let evass = events.map(i=>i.assignments)
          //person booked last event
          let personbookedlastevent = j > 0 ? events[j - 1]?.assignments?.some(a => a.person_id == p.id) : false
          //person booked this event
          let personbookedthisevent = e.assignments?.some(a => a.person_id == p.id)
  
          if (personbookedlastevent || personbookedthisevent) {
            selectedpersonindex++
            maxTries--;
          } else {
            let selectedperson = this.moduloselectperson(peoplethatcandothetasks!, selectedpersonindex)
            assignmentfound.person_id = selectedperson.id
            console.log("Person assigned:", selectedperson.first_name, selectedperson.last_name, e.event_name, e.event_date, t.task_name, j > 0 ? events[j - 1]?.assignments?.map(i => i.person_id) : [])
            selectedpersonindex++
            break
          }
        }
  
      }
    }
    this.events = [...events]
  }
  randomselectperson(people: Person[]):number {
    const randomIndex = Math.floor(Math.random() * people.length);
    return randomIndex;
  }
  moduloselectperson(people:Person[],number:number):Person{
    return people[number % people.length]
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
  removepeopleThatAreUnavailable(people: Person[], event: Event): Person[] {
    let unavailability = this.unavailability?.filter(i => i.end_date! >= event.event_date! && i.start_date! <= event.event_date!)

    people = people.filter(i => !unavailability?.some(u => u.person_id == i.id))

    return people
  }
  removePeopleBookedThisEvent(assignments: Assignment[], people: Person[]): Person[] {
    people = people.filter(i => assignments.some(a => {
      if (a != null && a.person_id == i.id) {
        return false
      }
      else { return true }
    }
    ))
    return people
  }
  removePeopleThatCantDoTheTask(people: Person[], taskid: number): Person[] {
    people = people.filter(i => i.tasks?.some(t => t.id == taskid))
    return people
  }
  

}


