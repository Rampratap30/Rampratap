import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root',
})
export class CoreService {
  httpObj: any = {
    type: '',
    url: '',
    options: Object,
  };

  constructor(public http: HttpClient) {}

  clearHttp() {
    this.httpObj.type = '';
    this.httpObj.url = '';
    this.httpObj.options = {};
  }

  requestHttp(type: string, endPoint: string, body?: any, params?: any) {
    this.clearHttp();
   // console.log(environment.apiURL )
    this.httpObj.type = type;
    const q = endPoint.split('?');
    this.httpObj.url = environment.apiURL + q[0] + '?' + q[1];
  //  console.log(this.httpObj.url  )
    if (params !== false) {
      this.httpObj.options.params = params;
    }
    return this.http.request(
      this.httpObj.type,
      this.httpObj.url,
      this.httpObj.options
    );
  }
}
