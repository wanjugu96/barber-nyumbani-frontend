import { Component, OnInit } from '@angular/core';
import { AppointmentService } from '../appointment.service';


@Component({
  selector: 'app-admin',
  templateUrl: './admin.component.html',
  styleUrls: ['./admin.component.css']
})
export class AdminComponent implements OnInit {
appointments: any
id: any
phone: any
  constructor(public AppointmentService:AppointmentService) { }

  ngOnInit(): void {
    this.appointments=this.AppointmentService.getappointment().subscribe((data: any): void=>{this.appointments=data
    });
  }
  onApprove(data: any){
    const phone={phone :data.phone};
    const id=data.statusid

    this.AppointmentService.approveappointment(id,phone).subscribe(data=>{
    
      //console.log(phone)
      //this.msgtrue=true;
      });

  }
  

}
