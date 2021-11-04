import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class AppointmentService {

  constructor(private http: HttpClient) { }
  token = '87d3b5cbbc0f7a5d651f257020b18bd47be765c5'


  createappointment(createBody: any) {


    return this.http.post('https://barber-nyumbani.herokuapp.com/api/appointments/', createBody,
      {
        headers: {
          Authorization: 'Token ' + this.token,
        }
      }

    );

  }




  getappointment(){
    return this.http.get('https://barber-nyumbani.herokuapp.com/api/appointments/')
       
     }
  getbarber(){
      return this.http.get('https://barber-nyumbani.herokuapp.com/api/barbers/')
         
       }
  getservices(){
  return this.http.get('https://barber-nyumbani.herokuapp.com/api/services/')
      
    }

approveappointment(id: any,phone:any){

  return this.http.put('https://barber-nyumbani.herokuapp.com/api/appointments/' + id + '/approve/',phone,
  {
    headers: {
      Authorization: 'Token ' + this.token,
    }
  } 
  );
       
     }

}
