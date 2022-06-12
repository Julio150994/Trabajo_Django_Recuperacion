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
  citasPaciente: any;
  citasRealizadas: any[] = [];
  citas: any;
  encabezadoCitas: any;
  id: any;
  medicos: any;// funciona al pulsar el botón de logout (ocultando el select de médicos)
  tok: any;
  token: any;
  username: any;
  tokenEliminado: any;
  usuarioPaciente: string;

  constructor(private loadingCtrl: LoadingController, private alertCtrl: AlertController,
    private navCtrl: NavController, private apiService: CitasPacienteService) { }

  ngOnInit() {
    console.log('Citas realizadas del paciente con médico');
    this.getCitasPaciente();
  }

  /** Métodos para cerrar sesión del paciente */
  logout() {
    localStorage.removeItem('token');
    this.loadPaciente('Cerrando sesión...');
  }

  async loadPaciente(message: string) {
    const loading = await this.loadingCtrl.create({
      message,
      duration: 3,
    });

    await loading.present();

    const { role, data } = await loading.onDidDismiss();

    this.navCtrl.navigateForward('/login-pacientes');
    this.alertLogoutPaciente(this.username);
  }

  async alertLogoutPaciente(username: string) {
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

  /** Para obtener las citas realizadas del paciente */
  async getCitasPaciente() {
    this.token = localStorage.getItem('token');

    // Validaciones de las citas
    /*this.apiService.getEncabezadoCitasPaciente()
    .then(async data => {
      this.encabezadoCitas = data;
      this.encabezadoCitas = this.encabezadoCitas.data;
    });*/

    // Obtenemos los datos de las citas del paciente
    this.apiService.obtenerCitasRealizadasPaciente(this.token).then(data => {
      this.citasPaciente = data;
      this.citasPaciente = this.citasPaciente.data;
      this.citas = this.citasPaciente;

      for (let cita = 0; cita < this.citas?.length; cita++) {
        if (this.citas[cita].idMedico.username === localStorage.getItem('medico_id')) {
          this.citasRealizadas.push(this.citas[cita]);
        }
      }
    });
  }
}
