import { NgForm } from '@angular/forms';
import { Component, OnInit } from '@angular/core';
import { AppointmentService } from '../appointment.service';
@Component({
  selector: 'app-admin',
  templateUrl: './admin.component.html',
  styleUrls: ['./admin.component.css'],
})
export class AdminComponent implements OnInit {
  appointments: any;
  phone: any;
  constructor(public AppointmentService: AppointmentService) {}
  ngOnInit(): void {
    this.appointments = this.AppointmentService.getappointment().subscribe(
      (data: any): void => {
        this.appointments = data;
      }
    );
  }
  // approve appointment
  onApprove(id:any) {
    id = parseInt(id);
    console.log(id);
    this.AppointmentService.approveappointment(id).subscribe((data: any) => {
      console.log(data);
      this.ngOnInit();
    });
  }
}