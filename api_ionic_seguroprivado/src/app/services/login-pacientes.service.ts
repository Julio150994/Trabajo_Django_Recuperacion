import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { AlertController } from '@ionic/angular';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class LoginPacientesService {
  apiUrl = environment.api;// poner el enlace de la api en los entornos
  username: string;
  password: string;
  tok: any;
  token: any;
  paciente: any;
  id: number;

  constructor(private login: HttpClient, private alertPaciente: AlertController) {}

  /* Para el inicio de sesión con los pacientes */
  loginPaciente(user, pwd) {
    return new Promise(res => {
      this.login.post<any>(this.apiUrl+'/token/',{
        username: user,
        password: pwd
      }).subscribe(data => {
        console.log(data);
        this.paciente = data;
        this.paciente = this.paciente.data;
        localStorage.setItem('token',this.paciente);
        res(data);
      }, error => {
        this.pacienteNoValido();// imprimimos un mensaje de alerta
        console.error('Error producido al iniciar sesión');
      });
    });
  }

  async pacienteNoValido() {
    const errorPaciente = await this.alertPaciente.create({
      header: 'ERROR',
      cssClass: 'loginCss',
      message: '<strong>Error al iniciar sesión con paciente</strong>',
      buttons: [
        {
          text: 'Aceptar',
          role: 'cancel',
          cssClass: 'secondary',
          handler: (valid) => {
          }
        }
      ]
    });
    await errorPaciente.present();
  }

  /** Para obtener todos los médicos */
  obtenerMedicos() {
    return new Promise(resolve => {
      this.login.get(this.apiUrl+'/medicos/', {
        headers: new HttpHeaders().append('Content-Type','application/json')
      }).subscribe(res => {
        resolve(res);
      }, (error) => {
        console.log(error);
      });
    });
  }
}
