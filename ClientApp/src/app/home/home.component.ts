import { Component } from '@angular/core';
import { Anonymous3, Client } from '../api/api';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent {
  data:Anonymous3 = new Anonymous3();
constructor(private client:Client){
  this.client.xyz().subscribe(res => this.data = res);

}
}
