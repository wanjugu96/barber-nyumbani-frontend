import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
​
@Injectable({
  providedIn: 'root',
})
export class AppointmentService {
  constructor(private http: HttpClient) {}
  token = 'dd67b380e5428280381fe02d5e1659b13a43fe0d';
​
  createappointment(createBody: any) {
    return this.http.post(
      'https://barber-nyumbani.herokuapp.com/api/appointments/',
      createBody,
      {
        headers: {
          Authorization: 'Token ' + this.token,
        },
      }
    );
  }
​
  getappointment() {
    return this.http.get(
      'https://barber-nyumbani.herokuapp.com/api/appointments/'
    );
  }
  getbarber() {
    return this.http.get('https://barber-nyumbani.herokuapp.com/api/barbers/');
  }
  getservices() {
    return this.http.get('https://barber-nyumbani.herokuapp.com/api/services/');
  }
​
  // approve appointment
  approveappointment(id:any) {
    return this.http.put(
      'https://barber-nyumbani.herokuapp.com/api/appointments/' +
        id +
        '/approve/',
      {},
      {
        headers: {
          Authorization: 'Token ' + this.token,
        },
      }
    );
  }
}