import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { AlertController, LoadingController } from '@ionic/angular';
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
  mensajeLogin: string;
  usuario: any;
  id: number;

  constructor(private httpLogin: HttpClient, private alertCtrl: AlertController,
    private loadingCtrl: LoadingController) {}

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
        this.mensajeLogin = 'Error al iniciar sesión con '+username;
        this.cargarLogin(this.mensajeLogin);
      });
    });
  }

  async cargarLogin(message: string) {
    const loading = await this.loadingCtrl.create({
      message,
      duration: 3,
    });

    await loading.present();

    const { role, data } = await loading.onDidDismiss();
    console.error(message);
    this.alertErrorLogin(message);
  }

  // Mensaje para indicar que ya has iniciado sesión con ese paciente
  async alertErrorLogin(mensajeError: string) {
    const error = await this.alertCtrl.create({
      header: 'MENSAJE DE AVISO',
      cssClass: 'warningCss',
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
