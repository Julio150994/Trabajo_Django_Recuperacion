import { Injectable } from '@angular/core';
import { HttpInterceptor, HttpRequest, HttpHandler, HttpEvent, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { Router } from '@angular/router';

@Injectable({
  providedIn: 'root'
})
export class AuthInterceptorService {

  constructor(private router: Router) { }

  // Para el inicio de sesión de los pacientes
  intercept(httpRequest: HttpRequest<any>, httpHandler: HttpHandler): Observable<HttpEvent<any>> {
    const token: string = localStorage.getItem('token');

    let request = httpRequest;

    if (token) {
      request = httpRequest.clone({
        setHeaders: {
          authorization: `Token ${ token }`
        }
      });
    }

    return httpHandler.handle(request).pipe(
      catchError((error: HttpErrorResponse) => {

        if (error.status === 401) {
          this.router.navigateByUrl('/login-pacientes');
        }

        return throwError(error);
      })
    );
  }
}
