import { Component, OnInit } from '@angular/core';
import { Client, Person, Unavailability, Unavailability2, Unavailability3 } from '../api/api';
import { FormControl, FormGroup, FormsModule, Validators } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-unavailability',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './unavailability.component.html',
  styleUrl: './unavailability.component.css'
})
export class UnavailabilityComponent implements OnInit {
unavailability: Unavailability[]|undefined = [];
people: Person[]|undefined = [];
  constructor(private client:Client) { }
  unavailabilityForm: FormGroup = new FormGroup({
    person_id: new FormControl(''),
    start_date: new FormControl('', Validators.required),
    end_date: new FormControl('', Validators.required)
  });
  async ngOnInit() {
    this.unavailability = await this.client.unavailabilityAll().toPromise();
    console.log(this.unavailability)
    this.people = await this.client.getpeople().toPromise();
  }
async createUnavailability(unavailability: Unavailability2) {
  

  console.log(unavailability);
  this.client.unavailabilityPOST(unavailability).toPromise();
  this.ngOnInit()
}
async updateUnavailability(unavailability: Unavailability) {


  console.log(unavailability);
  await this.client.unavailabilityPUT(unavailability.id!, unavailability as Unavailability3).toPromise();
  this.ngOnInit()
}
async deleteUnavailability(unavailability_id: number) {
  await this.client.unavailabilityDELETE(unavailability_id).toPromise();
  this.ngOnInit()
}
}
