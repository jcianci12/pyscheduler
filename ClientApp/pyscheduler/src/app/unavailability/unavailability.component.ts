import { Component, OnInit } from '@angular/core';
import { Client, Person, Unavailability, Unavailability2 } from '../api/api';
import { FormControl, FormGroup, FormsModule } from '@angular/forms';
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
    start_date: new FormControl<Date | null>(null),
    end_date: new FormControl<Date | null>(null)
  });
  async ngOnInit() {
    this.unavailability = await this.client.unavailabilityAll().toPromise();
    console.log(this.unavailability)
    this.people = await this.client.getpeople().toPromise();
  }
async createUnavailability(unavailability: Unavailability) {
  const startDate = this.unavailabilityForm.get('start_date')?.value;
  const endDate = this.unavailabilityForm.get('end_date')?.value;

  unavailability.start_date = startDate ? new Date(startDate) : undefined;
  unavailability.end_date = endDate ? new Date(endDate) : undefined;

  console.log(unavailability);
  this.client.unavailabilityPOST(unavailability).toPromise();
  this.ngOnInit()
}
async updateUnavailability(unavailability: Unavailability) {


  console.log(unavailability);
  await this.client.unavailabilityPUT(unavailability.id ?? 0, unavailability).toPromise();
  this.ngOnInit()
}
async deleteUnavailability(unavailability_id: number) {
  await this.client.unavailabilityDELETE(unavailability_id).toPromise();
  this.ngOnInit()
}
}
