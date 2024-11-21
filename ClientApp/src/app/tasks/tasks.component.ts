import { Component, OnInit } from '@angular/core';
import { Client, Task } from '../api/api';
import { CommonModule } from '@angular/common';
import { FormControl, FormGroup,FormsModule } from '@angular/forms';

@Component({
  selector: 'app-tasks',
  standalone: true,
  imports: [CommonModule,FormsModule],
  templateUrl: './tasks.component.html',
  styleUrl: './tasks.component.css'
})
export class TasksComponent implements OnInit {
  tasks: Task[] | undefined;
  taskForm: FormGroup= new FormGroup({
    id: new FormControl(''),
    task_name: new FormControl(''),
  });

  constructor(private client: Client) { }

  async ngOnInit() {
    this.tasks = await this.client.tasksAll().toPromise();
    this.taskForm 
  }

  async createTask(task: Task) {
    await this.client.tasksPOST(task).toPromise();
    this.tasks = await this.client.tasksAll().toPromise();
  }

  async updateTask(task: Task) {
    console.log(task)
    await this.client.tasksPUT(task.id as number,task).toPromise();
    this.tasks = await this.client.tasksAll().toPromise();
  }

  async deleteTask(taskId: number) {
    await this.client.tasksDELETE(taskId).toPromise();
    this.tasks = (this.tasks ?? []).filter(t => t.id !== taskId);  }
}

