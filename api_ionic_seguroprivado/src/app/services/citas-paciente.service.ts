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
  mensajeCitasRealizadas: string;
  token: any;
  paciente: any;
  user: string;
  refresh: any;
  authPaciente: BehaviorSubject<boolean> = new BehaviorSubject<boolean>(null);

  constructor(private httpCitas: HttpClient, private alertCtrl: AlertController) { }

  /** Para obtener todos los médicos */
  obtenerMedicos(tok: any) {
    return new Promise(resolve => {
      this.httpCitas.get(this.apiUrl+'/medicos/', {
        headers: new HttpHeaders().set('Authorization', 'Token '+tok)
      }).subscribe(res => {
        resolve(res);
      }, (error) => {
        console.error('No se han podido obtener los médicos '+error);
      });
    });
  }

  async obtenerCitasRealizadasPaciente(idMedico: number, token: any) {
    return new Promise(res => {
      this.httpCitas.get<any>(this.apiUrl+'/citas_paciente/?id='+idMedico, {
        headers: new HttpHeaders().set('Authorization', 'Token '+token)
      }).subscribe(data => {
        if (data == null) {
          this.mensajeCitasRealizadas = 'No tiene citas realizadas con este médico';
          console.warn(this.mensajeCitasRealizadas);
          this.alertCitasRealizadas(this.mensajeCitasRealizadas);
        }
        else {
          this.citas = data;
        }
        res(data);
      }, error => {
        console.log(error);
      });
    });
  }


  // Mensaje de alerta para cuando el paciente no tiene citas realizadas con el médico seleccionado
  async alertCitasRealizadas(mensajeCitas: string) {
    const error = await this.alertCtrl.create({
      header: 'MENSAJE DE AVISO',
      cssClass: 'warningCss',
      message: '<strong>'+mensajeCitas+'</strong>',
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

  /** Para cerrar sesión de los usuarios pacientes */
  logoutPacientes(tok: any) {
    return new Promise(res => {
      this.httpCitas.post<any>(this.apiUrl+'/logout/', {
        headers: new HttpHeaders().set('Authorization', 'Token '+tok)
      }).subscribe(data => {
        res(data);
        this.mensajeLogout = 'Ha cerrado sesión correctamente';
        console.log(this.mensajeLogout);
        this.alertLogoutPaciente(this.mensajeLogout);
      }, error => {
        console.log(error);

        this.mensajeLogout = 'No se ha podido cerrar sesión';
        console.error(this.mensajeLogout+' '+error);
        this.alertErrorLogout(this.mensajeLogout);
      });
    });
  }

  /** Mensajes para cerrar sesión */
  async alertLogoutPaciente(mensaje: string) {
    const logout = await this.alertCtrl.create({
      header: 'Logout',
      cssClass: 'logoutCss',
      message: '<strong>'+mensaje+'</strong>',
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
    // Mostramos la alerta en el inicio
    await logout.present();
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
