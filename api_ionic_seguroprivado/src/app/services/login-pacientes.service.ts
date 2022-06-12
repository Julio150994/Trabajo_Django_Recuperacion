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

  constructor(private httpLogin: HttpClient, private alertPaciente: AlertController) {}

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

  /** Obtenemos los usuarios de la base de datos */
  obtenerUsuarios() {
    return new Promise(res => {
      this.httpLogin.get(this.apiUrl+'/usuarios/',{
        headers: new HttpHeaders().append('Content-Type','application/json')
      }).subscribe(data => {
        this.token = data;
        this.token = this.token.data;
        res(data);
      }, error => {
        console.log('Error al obtener los usuarios '+error);
      });
    });
  }

  /** Para obtener todos los médicos */
  obtenerMedicos(tok: any) {
    return new Promise(resolve => {
      this.httpLogin.get(this.apiUrl+'/medicos/', {
        headers: new HttpHeaders().set('Authorization', 'Token '+tok)
      }).subscribe(res => {
        resolve(res);
      }, (error) => {
        console.log(error);
      });
    });
  }
}
