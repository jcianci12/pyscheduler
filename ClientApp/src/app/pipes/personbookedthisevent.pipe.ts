import { Pipe, PipeTransform } from '@angular/core';
import { Assignment, Event } from '../api/api';

@Pipe({
  name: 'personbookedthisevent',
  standalone: true,
  pure:false
})
export class PersonbookedthiseventPipe implements PipeTransform {

  transform(assignment: Assignment, thisevent: Event): Boolean {

    if(!thisevent) return false
    let thiseventpersonids = thisevent.assignments!.map(e => e.person_id);
    let thisassignmentpersonid = assignment.person_id;
    // return true
    return thiseventpersonids.filter(p=>p==thisassignmentpersonid).length>1;
  }
}
