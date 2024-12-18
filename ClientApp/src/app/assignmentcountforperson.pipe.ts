import { Pipe, PipeTransform } from '@angular/core';
import { Assignment, Person } from './api/api';

@Pipe({
  name: 'assignmentcountforperson'
})
export class AssignmentcountforpersonPipe implements PipeTransform {

  transform(person: Person, assignments: Assignment[]): number {
    return assignments.filter(a => a.person_id == person.id).length;
  }

}
