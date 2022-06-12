import { Component, Input, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { NavController, AlertController, LoadingController } from '@ionic/angular';
import { LoginPacientesService } from '../../services/login-pacientes.service';
import { CitasPacienteService } from '../../services/citas-paciente.service';

@Component({
  selector: 'app-login-pacientes',
  templateUrl: './login-pacientes.page.html',
  styleUrls: ['./login-pacientes.page.scss'],
})
export class LoginPacientesPage implements OnInit {
  @Input() paciente: string;

  tok: any;
  token: any;
  request: any;
  usuario: any;
  idUsuario: any;
  datosPaciente: any;
  username: string;
  password: string;
  medicos: any;
  medico: any;
  medicoSalesin: any[] = [];
  medicoSeleccionado: any;

  user = new FormGroup({
    username: new FormControl('', [Validators.required]),
    password: new FormControl('', [Validators.required, Validators.minLength(8)]),
  });

  constructor(private pacientesService: LoginPacientesService, private citasService: CitasPacienteService,
    private navCtrl: NavController, private loadingCtrl: LoadingController,
    private alertCtrl: AlertController) {}


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
    this.pacienteLogueado();
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

  async pacienteLogueado() {
    const login = await this.alertCtrl.create({
      header: 'Login',
      cssClass: 'loginCss',
      message: '<strong>Ha iniciado sesión correctamente</strong>',
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
      this.datosPaciente = this.user.value;
      this.username = this.datosPaciente.username;
      this.password = this.datosPaciente.password;

      await this.pacientesService.loginPaciente(this.username, this.password)
      .then(async data => {
        this.tok = data;
        this.token = this.tok.token;

        // Mostramos mensaje de login de usuario
        await this.cargarUsuario('Cargando aplicación...');

        // Obtenemos los médicos del sistema con el token de sesión
        await this.getMedicos(this.token);

        /*let usuarios: any;
        usuarios = await this.pacientesService.obtenerUsuarios();
        usuarios = usuarios.data;
        console.log('Usuarios encontrados: '+usuarios+'\n');

        for (let i = 0; i < usuarios?.length; i++) {
          if (usuarios[i].username === this.username) {
            this.username = usuarios[i].username;
            console.log('Usernames: '+this.username);
            this.idUsuario = usuarios[i].idUsuario;
            console.log('Ids usuarios: '+this.idUsuario);
            break;
          }
        }*/
      });
    }
  }

  /** Obtenemos y seleccionamos uno de los médicos obtenidos después de iniciar sesión*/
  async getMedicos(tok: any) {
    this.pacientesService.obtenerMedicos(tok)
    .then(medicos => {
      this.medicos = medicos;
      if (this.medicos == null) {
        console.error('No se han encontrado médicos en el sistema.');
      }
      else {
        for (let i = 0; i < this.medicos?.length; i++) {
          this.medicoSalesin.push(this.medicos[i]);
        }
      }
    });
  }

  async seleccionarMedico() {
    this.medico = this.medicoSeleccionado;
    await this.toCitasPaciente(this.medicoSeleccionado);
  }

  /** Para las citas del paciente con el médico seleccionado*/
  async toCitasPaciente(medico: string) {
    console.log('Citas realizadas del paciente con el médico '+medico);
    this.navCtrl.navigateForward('/citas-paciente');
  }
}
