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
  usuario: any;
  id: number;

  constructor(private httpLogin: HttpClient, private alertCtrl: AlertController) {}

  /* Para el inicio de sesión con los pacientes */
  loginPaciente(username, pwd) {
    return new Promise(res => {
      this.httpLogin.post<any>(this.apiUrl+'/token/',{
        user: username,
        password: pwd
      }).subscribe(data => {
        console.log(data);
        this.paciente = data;
        this.paciente = this.paciente.data;
        localStorage.setItem('token',this.paciente);
        res(data);
      }, error => {
        console.error('Ya has iniciado sesión con '+username);

      });
    });
  }

  /** Obtenemos los usuarios pacientes de la base de datos */
  obtenerUsuariosPacientes() {
    return new Promise(res => {
      this.httpLogin.get(this.apiUrl+'/pacientes/',{
      }).subscribe(data => {
        this.token = data;
        this.token = this.token.data;
        res(data);
      }, error => {
        console.error('Error al obtener los usuarios pacientes '+error);
      });
    });
  }

  // Mensaje para indicar que ya has iniciado sesión con ese paciente
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
}
