import { Component, OnInit } from '@angular/core';
import { LoadingController, AlertController, NavController } from '@ionic/angular';
import { environment } from '../../../environments/environment.prod';
import { CitasPacienteService } from '../../services/citas-paciente.service';


@Component({
  selector: 'app-citas-paciente',
  templateUrl: './citas-paciente.page.html',
  styleUrls: ['./citas-paciente.page.scss'],
})
export class CitasPacientePage implements OnInit {
  url = environment.api;
  usuario: any;
  idUsuario: any;
  citasPaciente: any;
  citas: any;
  encabezadoCitas: any;
  idMedico: any;
  medicos: any;
  tok: any;
  token: any;
  username: any;
  tokenEliminado: any;
  paciente: any;
  medicoSalesin: any[] = [];
  medicoSeleccionado: any;


  constructor(private loadingCtrl: LoadingController, private alertCtrl: AlertController,
    private navCtrl: NavController, private apiCitasService: CitasPacienteService) {}


  async ngOnInit() {
    console.log('Página de las citas del paciente');

    // Establecemos el token de sesión actual para obtener los médicos
    this.token = localStorage.getItem('token');
    this.getMedicos(this.token);
  }

  /** Obtenemos y seleccionamos uno de los médicos obtenidos después de iniciar sesión*/
  async getMedicos(tok: any) {
    this.apiCitasService.obtenerMedicos(tok)
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
    this.idMedico = this.medicoSeleccionado;
    await this.toCitasPaciente(this.medicoSeleccionado, this.token);
  }

  /** Para las citas del paciente con el médico seleccionado */
  async toCitasPaciente(idMedico: number, token: any) {
    // Para obtener las citas con el médico seleccionado
    await this.apiCitasService.obtenerCitasRealizadasPaciente(idMedico, token)
    .then(async data => {
      this.citas = data;// mostramos las citas del paciente con el médico seleccionado sin repetir
    });

    this.navCtrl.navigateForward('/citas-paciente');
  }

  logout() {
    // Para cerrar la sesión del paciente eliminando el token
    this.loadPaciente('Cerrando sesión...');
  }

  async loadPaciente(message: string) {
    const loading = await this.loadingCtrl.create({
      message,
      duration: 3,
    });

    await loading.present();

    const { role, data } = await loading.onDidDismiss();

    // Cerramos la sesión del paciente durante la eliminación del token
    await this.apiCitasService.logoutPacientes(localStorage.getItem('token'));
    this.navCtrl.navigateForward('/login-pacientes');
    this.alertLogoutPaciente();
  }

  async alertLogoutPaciente() {
    const logout = await this.alertCtrl.create({
      header: 'Logout',
      cssClass: 'logoutCss',
      message: '<strong>El paciente ha cerrado sesión correctamente</strong>',
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
}
