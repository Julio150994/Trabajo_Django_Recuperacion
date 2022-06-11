import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { IonicModule } from '@ionic/angular';

import { CitasPacientePageRoutingModule } from './citas-paciente-routing.module';

import { CitasPacientePage } from './citas-paciente.page';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    CitasPacientePageRoutingModule
  ],
  declarations: [CitasPacientePage]
})
export class CitasPacientePageModule {}
