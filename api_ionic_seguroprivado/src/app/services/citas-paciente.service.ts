import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { AlertController } from '@ionic/angular';
import { environment } from '../../environments/environment';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class CitasPacienteService {
  apiUrl = environment.api;// poner el enlace de la api en los entornos
  cita: any;
  citas: any;
  mensajeLogout: string;
  token: any;
  refresh: any;
  authPaciente: BehaviorSubject<boolean> = new BehaviorSubject<boolean>(null);

  constructor(private httpCitas: HttpClient, private alertCtrl: AlertController) { }


  async obtenerCitasRealizadasPaciente(token: any) {
    return new Promise(res => {
      this.httpCitas.get<any>(this.apiUrl+'/citas_paciente/', {
        headers: new HttpHeaders().set('Authorization', 'Token '+token)
      }).subscribe(data => {
        this.citas = data;
        this.citas = this.citas.data;
        res(data);
      }, error => {
        console.log(error);
        console.error('Este paciente no tiene citas realizadas');
      });
    });
  }

  /** Para cerrar sesión de los usuarios pacientes */
  async logoutPacientes(token: any) {
    return new Promise(res => {
      this.httpCitas.post(this.apiUrl+'/logout/', {
        headers: new HttpHeaders().set('Authorization', 'Token '+token)
      }).subscribe(data => {
        console.log(data);
        res(data);
      }, error => {
        this.mensajeLogout = 'No se ha podido cerrar sesión';
        console.error(this.mensajeLogout+' '+error);
        this.alertErrorLogout(this.mensajeLogout);
      });
    });
  }

  async alertErrorLogout(mensajeError: string) {
    const error = await this.alertCtrl.create({
      header: 'ERROR',
      cssClass: 'sessionCss',
      message: '<strong>'+mensajeError+'</strong>',
      buttons: [
        {
          text: 'Aceptar',
          role: 'cancel',
          cssClass: 'secondary',
          handler: (deactived) => {
          }
        }
      ]
    });
    await error.present();
  }
}
