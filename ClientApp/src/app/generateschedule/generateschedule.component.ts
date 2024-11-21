import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FormsModule, FormArray, FormControl, FormGroup, ReactiveFormsModule } from '@angular/forms';

@Component({
  selector: 'app-generateschedule',
  standalone: true,
  imports: [FormsModule, ReactiveFormsModule, CommonModule],
  templateUrl: './generateschedule.component.html',
  styleUrls: ['./generateschedule.component.css']
})
export class GeneratescheduleComponent {
  form = new FormGroup({
    num: new FormControl(1),
    event: new FormControl(''),
    events: new FormArray([
      new FormGroup({
        name: new FormControl('Default Event'),
        interval: new FormControl(1),
        intervalType: new FormControl('weeks')

      })
    ]),
    start: new FormControl(''),
    intervalType: new FormControl('weeks')
  });

  get eventsArray(): FormArray {
    return this.form.get('events') as FormArray;
  }

  addEvent() {
    this.eventsArray.push(new FormGroup({
      name: new FormControl(''),
      interval: new FormControl(1)
    }));
  }

  removeEvent(index: number) {
    this.eventsArray.removeAt(index);
  }

  onSubmit() {
    console.log(this.form.value);
  }

}



