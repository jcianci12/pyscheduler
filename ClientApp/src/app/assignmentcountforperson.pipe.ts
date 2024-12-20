import { Pipe, PipeTransform } from '@angular/core';
import { Assignment, Event, IPerson, Person } from './api/api';
import { flatMap } from 'rxjs';
@Pipe({
  name: 'assignmentcountforperson'
})
export class AssignmentcountforpersonPipe implements PipeTransform {

  transform(people: Person[], events: Event[]): PersonAssignment[] {

    let assignmentsarray: Assignment[] = []
    for (var i = 0; i < events.length; i++) {
      let assarray = events[i].assignments!.flat()
      assignmentsarray.push(...assarray)
    }
if (!people){
  return []
}
    let data = people.map(p => ({ ...p, colour: "",
      assignmentCount: assignmentsarray.filter(a => a.person_id == p.id).length })
    );
    let min = Math.min(...data.map(d => d.assignmentCount))
    let max = Math.max(...data.map(d => d.assignmentCount))
    data = data.map(d => ({...d, colour: `rgb(255,${Math.floor((d.assignmentCount-min) / (max-min) * 255)},0)`}))
    data = data.sort((a, b) => b.assignmentCount - a.assignmentCount);

    return data

  }

}

export interface PersonAssignment extends IPerson {

  assignmentCount: Number
  
  colour: string
}