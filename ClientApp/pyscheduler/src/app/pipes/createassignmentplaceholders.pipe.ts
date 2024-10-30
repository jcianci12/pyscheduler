import { Pipe, PipeTransform } from '@angular/core';
import { Assignment, Event, Task } from '../api/api';




@Pipe({
  name: 'createassignmentplaceholders',
  standalone: true
})
export class CreateassignmentplaceholdersPipe implements PipeTransform {
  transform(events: Event[], tasks: Task[]): Event[] {
    if (!events) return []

    // return events.map(event => {

    //   if (event.assignments!.length === 0) {
    //     event.assignments = tasks.map(task => new Assignment({
    //       id: undefined,event_id: event.id, person_id: undefined, task_id: task.id
    //     }));
    //   }


    //   return event;
    // });


    return events.map(event => {
      return new Event({
        event_date: event.event_date, event_name: event.event_name, id: event.id,
        assignments: 
          tasks.map(task => new Assignment({
            id: undefined, event_id: event.id, person_id: event.assignments?.find(a => a.event_id == event.id && a.task_id == task.id)?.person_id, task_id: task.id
          })
        )
      })


        ;
    })
  }

}

