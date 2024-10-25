import { Component } from '@angular/core';
import { Client, Assignment } from '../api/api';
import { FormControl, FormGroup,Validators,FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-schedules',
  standalone: true,
  imports: [CommonModule,FormsModule],
  templateUrl: './assignments.component.html',
  styleUrl: './assignments.component.css'
})



export class AssignmentsComponent {
// schedule:Schedule=   event_id?: number | undefined;
// id?: number | undefined;
// person_id?: number | undefined;
// task_id?: number | undefined;
  schedules: Assignment[] = [];
  persons: any[] = [];
  tasks: any[] = [];
  events: any[] = [];

  ngOnInit(): void {
    this.client.assignmentsAll().subscribe(schedules => {
      this.schedules = schedules;
    });

    this.client.getpeople().subscribe(persons => {
      this.persons = persons;
    });

    this.client.tasksAll().subscribe(tasks => {
      this.tasks = tasks;
    });

    this.client.eventsAll().subscribe(events => {
      this.events = events;
    });
  }
  scheduleForm: FormGroup= new FormGroup({
    id: new FormControl(''),
    event_id: new FormControl('', Validators.required),
    person_id: new FormControl('', Validators.required),
    task_id: new FormControl('', Validators.required)
  });
  constructor(private client: Client) { }

  


  createSchedule(schedule: Assignment): void {
    this.client.assignmentsPOST(schedule).subscribe(() => {
      this.ngOnInit();
    });
  }

  deleteSchedule(schedule_id: number): void {
    this.client.assignmentsDELETE(schedule_id).subscribe(() => {
      this.ngOnInit();
    });
  }

  updateSchedule(schedule: Assignment): void {
    this.client.assignmentsPUT(schedule.id!, schedule).subscribe(() => {
      this.ngOnInit();
    });
  }


}
