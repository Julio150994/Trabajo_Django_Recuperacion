import { TestBed } from '@angular/core/testing';

import { CitasPacienteService } from './citas-paciente.service';

describe('CitasPacienteService', () => {
  let service: CitasPacienteService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(CitasPacienteService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
