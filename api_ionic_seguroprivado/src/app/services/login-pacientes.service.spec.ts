import { TestBed } from '@angular/core/testing';

import { LoginPacientesService } from './login-pacientes.service';

describe('LoginPacientesService', () => {
  let service: LoginPacientesService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(LoginPacientesService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
