import { NgModule } from '@angular/core';
import { PreloadAllModules, RouterModule, Routes } from '@angular/router';

const routes: Routes = [
  {
    path: 'login-pacientes',
    loadChildren: () => import('./pages/login-pacientes/login-pacientes.module').then( m => m.LoginPacientesPageModule)
  },
  {
    path: 'citas-paciente',
    loadChildren: () => import('./pages/citas-paciente/citas-paciente.module').then( m => m.CitasPacientePageModule)
  },
  {
    path: '',
    redirectTo: 'login-pacientes',
    pathMatch: 'full'
  },
];

@NgModule({
  imports: [
    RouterModule.forRoot(routes, { preloadingStrategy: PreloadAllModules })
  ],
  exports: [RouterModule]
})
export class AppRoutingModule { }
