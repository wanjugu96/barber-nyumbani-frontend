import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { AppointmentService } from './appointment.service';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  barbers: any;
  services: any;

  constructor(public AppointmentService:AppointmentService) { }
  title = 'barber-Nyumbani';
  onSubmit(data: any){
  const formdata={name: data.name,phone :data.phone,barber :data.barber,service :data.service};

  this.AppointmentService.createappointment(formdata).subscribe(data=>{
    
    console.log(formdata)
    //this.msgtrue=true;
    });
  }

  ngOnInit(): void {
 this.barbers=this.AppointmentService.getbarber().subscribe(data=>{this.barbers=data
 });

 

this.services=this.AppointmentService.getservices().subscribe(data=>{this.services=data

});

  

}
}
