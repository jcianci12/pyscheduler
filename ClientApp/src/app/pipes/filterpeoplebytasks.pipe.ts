import { Pipe, PipeTransform } from '@angular/core';
import { Assignment, Person, Task } from '../api/api';

@Pipe({
  name: 'filterpeoplebytasks',
  standalone: true,
})
export class FilterpeoplebytasksPipe implements PipeTransform {

  transform(people: Person[],task: Task ): Person[] {
    if(people==null){
      return people
    }
    let filteredpeople: Person[] = people.filter(p => p.tasks?.some(t => t.id === task.id));
   

    return filteredpeople
  }

}
