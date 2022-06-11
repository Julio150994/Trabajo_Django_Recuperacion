import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { CitasPacientePage } from './citas-paciente.page';

const routes: Routes = [
  {
    path: '',
    component: CitasPacientePage
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class CitasPacientePageRoutingModule {}
