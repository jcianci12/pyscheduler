import { Pipe, PipeTransform } from '@angular/core';
import { Person } from './api/api';
import { PersonAssignment } from './assignmentcountforperson.pipe';

@Pipe({
  name: 'findpersonwithid'
})
export class FindpersonwithidPipe implements PipeTransform {

  transform(people: PersonAssignment[], personid: number): PersonAssignment|null {
    return people.find(p => p.id == personid)?? null;
  }

}
