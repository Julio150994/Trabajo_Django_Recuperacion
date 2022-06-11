import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

import { IonicModule } from '@ionic/angular';

import { LoginPacientesPageRoutingModule } from './login-pacientes-routing.module';

import { LoginPacientesPage } from './login-pacientes.page';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    IonicModule,
    LoginPacientesPageRoutingModule
  ],
  declarations: [LoginPacientesPage]
})
export class LoginPacientesPageModule {}
