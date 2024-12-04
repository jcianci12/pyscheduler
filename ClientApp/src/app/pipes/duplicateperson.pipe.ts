import { Pipe, PipeTransform } from '@angular/core';
import { Person } from '../api/api';

@Pipe({
  name: 'duplicateperson',
  standalone: true,
  pure: false
})
export class DuplicatepersonPipe implements PipeTransform {

  transform(person: Person, people: Person[]): boolean {
    let d = people.filter(p => p.first_name?.trim() === person.first_name?.trim() && p.last_name?.trim() === person.last_name?.trim()).length > 1;
    // console.log(d)
    return d
  }

}
