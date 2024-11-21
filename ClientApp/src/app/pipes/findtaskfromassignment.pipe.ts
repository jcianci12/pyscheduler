import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'findtaskfromassignment',
  standalone: true
})
export class FindtaskfromassignmentPipe implements PipeTransform {

  transform(value: unknown, ...args: unknown[]): unknown {
    return null;
  }

}
