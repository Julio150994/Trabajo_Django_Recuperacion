import { Component, OnInit, ViewChild } from '@angular/core';
import { LoadingController, AlertController, NavController, IonList } from '@ionic/angular';
import { environment } from '../../../environments/environment.prod';
import { CitasPacienteService } from '../../services/citas-paciente.service';

@Component({
  selector: 'app-citas-paciente',
  templateUrl: './citas-paciente.page.html',
  styleUrls: ['./citas-paciente.page.scss'],
})
export class CitasPacientePage implements OnInit {
  @ViewChild('listaCitasPaciente', {static: true}) listaCitasPaciente: IonList;

  url = environment.api;
  citasPaciente: any;
  citasRealizadas: any[] = [];
  citas: any;
  encabezadoCitas: any;
  id: any;
  token: any;
  tokenEliminado: any;


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
      duration: 2,
    });

    await loading.present();

    const { role, data } = await loading.onDidDismiss();

    this.navCtrl.navigateForward('/login-pacientes');
    this.alertLogoutPaciente();
  }

  async alertLogoutPaciente() {
    const logout = await this.alertCtrl.create({
      header: 'Logout',
      cssClass: 'logoutCss',
      message: '<strong>El paciente ha cerrado sesión</strong>',
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
  }

  /** Para obtener las citas realizadas del paciente */
  async getCitasPaciente() {
    this.apiService.obtenerCitasRealizadasPaciente().then(data => {
      this.citasPaciente = data;
      this.citasPaciente = this.citasPaciente.data;
      this.citas = this.citasPaciente;

      for (let cita = 0; cita < this.citas?.length; cita++) {
        if (this.citas[cita].idMedico.username === localStorage.getItem('nombre_medico')) {
          this.citasRealizadas.push(this.citas[cita]);
        }
      }
    });
  }
}
