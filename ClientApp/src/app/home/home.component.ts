import { Component } from '@angular/core';
import { Client } from '../api/api';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent {
constructor(private client:Client){
  this.client.xyz().subscribe(res => console.log(res));
  
}
}
