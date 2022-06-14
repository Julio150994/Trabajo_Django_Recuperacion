import { Component, Input, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { NavController, AlertController, LoadingController } from '@ionic/angular';
import { LoginPacientesService } from '../../services/login-pacientes.service';

@Component({
  selector: 'app-login-pacientes',
  templateUrl: './login-pacientes.page.html',
  styleUrls: ['./login-pacientes.page.scss'],
})
export class LoginPacientesPage implements OnInit {
  tok: any;
  token: any;
  paciente: any;
  pacientes: any;
  username: string;
  password: string;
  idUsuario: any;
  pacientesEncontrados: any[] = [];

  user = new FormGroup({
    username: new FormControl('', [Validators.required]),
    password: new FormControl('', [Validators.required, Validators.minLength(6)]),
  });

  constructor(private apiLoginService: LoginPacientesService, private navCtrl: NavController,
    private loadingCtrl: LoadingController, private alertCtrl: AlertController) {}

  ngOnInit() {
    console.log('Página de login de pacientes');
  }

  /** Mensaje para cuando hemos iniciado sesión con el paciente correctamente */
  async cargarUsuario(message: string) {
    const loading = await this.loadingCtrl.create({
      message,
      duration: 3,
    });

    await loading.present();

    const { role, data } = await loading.onDidDismiss();
  }

  async errorCredenciales() {
    const credenciales = await this.alertCtrl.create({
      header: 'ERROR',
      cssClass: 'errorCss',
      message: '<strong>Error en las credenciales de usuario</strong>',
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
    await credenciales.present();
  }

  async usuarioNoEncontrado(username: string) {
    const mensajeError = await this.alertCtrl.create({
      header: 'Message',
      cssClass: 'messageCss',
      message: '<strong>Usuario '+username+' no encontrado en la base de datos</strong>',
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
    await mensajeError.present();
  }

  async usuarioNoValido(username: string) {
    const mensajeError = await this.alertCtrl.create({
      header: 'Message',
      cssClass: 'messageCss',
      message: '<strong>'+username+' debe ser un usuario paciente</strong>',
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
    await mensajeError.present();
  }

  async pacienteLogueado(username: string) {
    const login = await this.alertCtrl.create({
      header: 'Login',
      cssClass: 'loginCss',
      message: '<strong>'+username+' ha iniciado sesión correctamente</strong>',
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
    await login.present();
  }

  async login() {
    if (this.user.valid) {
      this.paciente = this.user.value;
      this.username = this.paciente.username;
      this.password = this.paciente.password;

      await this.apiLoginService.loginPaciente(this.username, this.password)
      .then(async data => {
        this.tok = data;
        this.token = this.tok.token;
        localStorage.setItem('token',this.token);
        // Mostramos mensaje de login de usuario
        await this.cargarUsuario('Cargando aplicación...');

        // Redirigimos a la otra página y mostramos mensaje en la otra página
        this.navCtrl.navigateForward('/citas-paciente');
        this.pacienteLogueado(this.username);
      });
    }
  }
}
