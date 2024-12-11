import { Component, OnInit } from '@angular/core';
import { Anonymous3, Client } from '../api/api';
import { CommonModule } from '@angular/common';
import { AuthService } from '../auth/auth.service';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent implements OnInit {
  data: Anonymous3 = new Anonymous3();
  constructor(private client: Client,public authService:AuthService) {


  }
  ngOnInit(): void {
    this.client.xyz().subscribe(res => this.data = res);

  }
}
