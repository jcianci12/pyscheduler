import { Pipe, PipeTransform } from '@angular/core';
import { Assignment } from '../api/api';

@Pipe({
  name: 'filterassignmentsbytask',
  standalone: true
})
export class FilterassignmentsbytaskPipe implements PipeTransform {

  transform(assignments: Assignment[], taskid: number): Assignment[] {
    return assignments.filter(a => a.task_id === taskid);
  }

}

