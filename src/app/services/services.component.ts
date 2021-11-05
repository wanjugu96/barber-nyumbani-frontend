import { Component, OnInit } from '@angular/core';
import { AppointmentService } from '../appointment.service';

@Component({
  selector: 'app-services',
  templateUrl: './services.component.html',
  styleUrls: ['./services.component.css']
})
export class ServicesComponent implements OnInit {
  services: any;

  constructor(public AppointmentService:AppointmentService) { }

  ngOnInit(): void {
    this.services=this.AppointmentService.getservices().subscribe((data: any)=>{this.services=data

    });
    
    
  }

}
