import { Pipe, PipeTransform } from '@angular/core';
import { Event } from './app/api/api';

@Pipe({
  name: 'filtereventsbydate'
})
export class FiltereventsbydatePipe implements PipeTransform {

  transform(value: Event[], startDate:Date,endDate:Date): Event[] {
    value =  value
    .filter(i =>new Date(i.event_date!) >= startDate && 
     new Date(i.event_date!) <= endDate);
    return value
  }

}
