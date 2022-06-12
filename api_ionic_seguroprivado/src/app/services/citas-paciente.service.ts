import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { AlertController } from '@ionic/angular';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class CitasPacienteService {
  apiUrl = environment.api;// poner el enlace de la api en los entornos
  tok: any;
  token: any;
  cita: any;
  citas: any;
  id: number;

  constructor(private httpCitas: HttpClient, private alertCitasCtrl: AlertController) { }

  /** Funciones patra gestionar las citas del paciente */
  getEncabezadoCitasPaciente() {
    return new Promise(res => {
      this.httpCitas.post(this.apiUrl+'/citas_paciente/?id='+localStorage.getItem('medico_id'),{
        //headers: new HttpHeaders().set('Authorization', 'Token '+localStorage.getItem('token'))
        headers: new HttpHeaders().append('Content-Type','application/json')
      }).subscribe(data => {
        this.cita = data;
        this.cita = this.cita.data;
        res(data);
      }, error => {
        console.log('Error al mostrar el contador de artículos '+error);
      });
    });
  }

  async obtenerCitasRealizadasPaciente() {
    return new Promise<any>(res => {
      this.httpCitas.get(this.apiUrl+'/citas_paciente/', {
        headers: new HttpHeaders().append('Content-Type','application/json')
      }).subscribe(data => {
        this.citas = data;
        this.citas = this.citas.data;
        res(data);
      }, (error) => {
        console.log(error);
        console.log('Este paciente no tiene citas realizadas');
      });
    });
  }
}
