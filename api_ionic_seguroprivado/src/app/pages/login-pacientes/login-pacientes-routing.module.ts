import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { LoginPacientesPage } from './login-pacientes.page';

const routes: Routes = [
  {
    path: '',
    component: LoginPacientesPage
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class LoginPacientesPageRoutingModule {}
