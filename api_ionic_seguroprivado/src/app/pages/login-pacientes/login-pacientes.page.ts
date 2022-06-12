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
  @Input() usuarioPaciente: string;

  tok: any;
  token: any;
  usuario: any;
  paciente: any;
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

  constructor(private apiService: LoginPacientesService, private navCtrl: NavController,
    private loadingCtrl: LoadingController, private alertCtrl: AlertController) {}


  ngOnInit() {
    console.log('Página de login de pacientes');
  }

  async login() {
    // Mostramos médicos cuando pulsamos al botón de login
    await this.loadLogin('Cargando aplicación...');

    console.log('Médicos del seguro obtenidos');
    await this.getMedicos();

    /*if (this.user.valid) {
      this.datosPaciente = this.user.value;
      this.username = this.datosPaciente.username;
      this.password = this.datosPaciente.password;

      await this.apiService.loginPaciente(this.username,this.password)
        .then(async data => {
          this.tok = data;
          this.usuario=this.tok.data;
          this.token = this.usuario.token;
          localStorage.setItem('token',this.token);

          let usuario: any;
          usuario = await this.apiService.obtenerMedicos();
          usuario=usuario.data;
        });
    }*/
  }

  /** Mensaje paar cuando hemos iniciado sesión con el paciente correctamente */
  async loadLogin(message: string) {
    const loading = await this.loadingCtrl.create({
      message,
      duration: 1.5,
    });

    await loading.present();

    const { role, data } = await loading.onDidDismiss();

    console.log('Ha iniciado sesión correctamente');
    this.alertLogin();
  }

  async alertLogin() {
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

  /** Obtenemos y seleccionamos uno de los médicos obtenidos */
  async getMedicos() {
    this.apiService.obtenerMedicos()
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
    console.log('Médico seleccionado: '+this.medicoSeleccionado);
    this.medico = this.medicoSeleccionado;
    await this.toCitasPaciente(this.medicoSeleccionado);
  }

  /** Para las citas del paciente con el médico seleccionado*/
  async toCitasPaciente(medico: string) {
    console.log('Citas realizadas del paciente con el médico '+medico);
    this.navCtrl.navigateForward('/citas-paciente');
  }
}
