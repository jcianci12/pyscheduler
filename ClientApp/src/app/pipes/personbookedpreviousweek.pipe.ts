import { Pipe, PipeTransform } from '@angular/core';
import {  Assignment, Client, Event, Event2, Person, Task } from '../api/api';


@Pipe({
  name: 'personbookedpreviousweek',
  standalone: true,
  pure:false
})
export class PersonbookedpreviousweekPipe implements PipeTransform {

  transform(assignment: Assignment, previousevent: Event): Boolean {

    if(!previousevent) return false
    let previousassignmentspersonids = previousevent.assignments!.map(e => e.person_id);
    let thisassignmentpersonid = assignment.person_id;
    // return true
    return previousassignmentspersonids.some(p=>p==thisassignmentpersonid);
  }

}
