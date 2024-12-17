import { Pipe, PipeTransform } from '@angular/core';
import { Person } from '../api/api';

@Pipe({
  name: 'filterpeoplebyname',
  standalone: true
})
export class FilterpeoplebynamePipe implements PipeTransform {

  transform(value: Person[]|undefined, term: string): Person[] {
    if(!value) return [];
    if(term=='' ) return value
    return value.filter(p=>(p.first_name!.toLowerCase()+p.last_name!.toLowerCase()).includes(term.toLowerCase()));
  }

}
