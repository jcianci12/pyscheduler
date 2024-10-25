import { Component, OnInit } from '@angular/core';
import { Client, Assignment } from '../api/api';
import { FormControl, FormGroup,Validators,FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-schedules',
  standalone: true,
  imports: [CommonModule,FormsModule],
  templateUrl: './assignments.component.html',
  styleUrl: './assignments.component.css'
})


export class AssignmentsComponent implements OnInit{
// schedule:Schedule=   event_id?: number | undefined;
// id?: number | undefined;
// person_id?: number | undefined;
// task_id?: number | undefined;
  assignments: Assignment[] = [];
  persons: any[] = [];
  tasks: any[] = [];
  events: any[] = [];
  event:Event|null=null;
  currentAssignment!:Assignment|null;
  eventIdFromRoute:number|null = null;
  ngOnInit(): void {
    const routeParams = this.route.snapshot.paramMap;
    this.eventIdFromRoute = Number(routeParams.get('id'));
    if (this.eventIdFromRoute) {

      this.client.get_assignments_by_event(this.eventIdFromRoute).subscribe(assignments => {
        this.assignments = assignments;
      });
    } else {
      this.client.assignmentsAll().subscribe(assignments => {
        this.assignments = assignments;
      });
    }

    this.client.getpeople().subscribe(persons => {
      this.persons = persons;
    });

    this.client.tasksAll().subscribe(tasks => {
      this.tasks = tasks;
    });

    this.client.eventsAll().subscribe(events => {
      this.events = events;
      if(this.eventIdFromRoute){
              this.event = this.events[this.eventIdFromRoute];

      }
    });
  }
  assignmentForm: FormGroup= new FormGroup({
    id: new FormControl(''),
    event_id: new FormControl('', Validators.required),
    person_id: new FormControl('', Validators.required),
    task_id: new FormControl('', Validators.required)
  });
  constructor(private client: Client, private route: ActivatedRoute) { }

  


  createAssignment(schedule: Assignment): void {
    this.client.assignmentsPOST(schedule).subscribe(() => {
      this.ngOnInit();
    });
  }

  deleteAssigment(schedule_id: number): void {
    this.client.assignmentsDELETE(schedule_id).subscribe(() => {
      this.ngOnInit();
    });
  }

  updateAssigment(schedule: Assignment): void {
    this.client.assignmentsPUT(schedule.id!, schedule).subscribe(() => {
      this.ngOnInit();
    });
  }


}

