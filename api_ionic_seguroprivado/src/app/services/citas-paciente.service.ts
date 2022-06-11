import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { AlertController } from '@ionic/angular';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class CitasPacienteService {
  apiSeguroPrivado = environment.api;// poner el enlace de la api en los entornos
  tok: any;
  token: any;
  cita: any;
  citas: any;
  id: number;

  constructor(private http: HttpClient, private alertCitasCtrl: AlertController) { }

  /** Para mostrar las citas del paciente */
  async obtenerCitasRealizadasPaciente() {
    return new Promise<any>(res => {
      this.http.get(this.apiSeguroPrivado+'/citas/').subscribe(data => {
        this.citas = data;
        this.citas = this.citas.data;
        res(data);
      }, error => {
        console.log('Este paciente no tiene citas realizadas');
      });
    });
  }
}
