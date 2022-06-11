import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { NavController, AlertController } from '@ionic/angular';
import { LoginPacientesService } from '../../services/login-pacientes.service';

@Component({
  selector: 'app-login-pacientes',
  templateUrl: './login-pacientes.page.html',
  styleUrls: ['./login-pacientes.page.scss'],
})
export class LoginPacientesPage implements OnInit {
  tok: any;
  token: any;
  usuario: any;
  paciente: any;
  username: string;
  password: string;
  medicos: any;
  medicoSalesin: any[] = [];
  pacienteConfirmed: any;
  datosPaciente: any;

  user = new FormGroup({
    username: new FormControl('', [Validators.required]),
    password: new FormControl('', [Validators.required, Validators.minLength(8)]),
  });

  constructor(private apiService: LoginPacientesService, private navCtrl: NavController,
    private alertCtrl: AlertController) { }

  ngOnInit() {
    console.log('Página de login de pacientes');
    this.login();
  }

  async login() {
    if (this.user.valid) {
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
    }
  }

  async getMedicos() {
    // Obtenemos los médicos para el select
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
}
