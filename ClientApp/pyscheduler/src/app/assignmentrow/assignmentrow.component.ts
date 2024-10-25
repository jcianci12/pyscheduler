import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Assignment, Client } from '../api/api';
import { Person } from '../api/api';
import { Task } from '../api/api';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-assignmentrow',
  standalone: true,
  imports: [CommonModule,FormsModule],
  templateUrl: './assignmentrow.component.html',
  styleUrls: ['./assignmentrow.component.css']
})
export class AssignmentrowComponent {
  @Input() eventid?: number;
  @Input() taskid?: number;
  @Input() model?: number;
  @Output() modelChange = new EventEmitter<number>();

  people: Person[] = [];
  task!: Task;
  selectedpersonid: number|undefined;
  _eventAssignment: Assignment | undefined;

  constructor(private client: Client) { }

  async ngOnInit(): Promise<void> {
    this.client.getpeople().subscribe(people => this.people = people);
    this.client.tasksGET(this.taskid??0).subscribe(tasks => this.task = tasks);
      this._eventAssignment = await this.client.assignmentsGET(this.eventid??0).toPromise();
      if(this._eventAssignment?.task_id == this.taskid){
            this.selectedpersonid = this._eventAssignment?.person_id;
      }
     
  }
  
  onPersonSelect(event: any) {
//update the db. if there is no existing assignmnet, add one
let assignment: Assignment =new Assignment({event_id:this.eventid,task_id:this.taskid,person_id: event.target.value}) ;
console.log(assignment)

    if(!this.selectedpersonid){
      this.client.assignmentsPUT(assignment.id??0,assignment).subscribe();
    }
    else{
      this.client.assignmentsPOST(assignment).subscribe();
    }
  }

}

