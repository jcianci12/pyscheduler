import { Pipe, PipeTransform } from '@angular/core';
import { Event } from './app/api/api';

@Pipe({
  name: 'filtereventsbydate'
})
export class FiltereventsbydatePipe implements PipeTransform {

  transform(value: Event[], startDate: Date, endDate: Date): Event[] {
    startDate = new Date(startDate)
    endDate =  new Date(endDate)
    value = value
      .filter(i => {

        return (startDate&& new Date(i.event_date!) >= startDate ) &&

          ( new Date(i.event_date!) <= new Date(endDate))
      }

      );
    return value
  }

}
