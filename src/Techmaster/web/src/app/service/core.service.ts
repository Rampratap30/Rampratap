import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { __extends } from 'tslib';
import { environment } from './../../environments/environment';
import { ToastrService } from 'ngx-toastr';
import { Router } from '@angular/router';
import * as CryptoJS from 'crypto-js';
import { Observable, Subject, throwError } from 'rxjs';
import { FormGroup } from '@angular/forms';

@Injectable({
  providedIn: 'root',
})
export class CoreService {
  httpObj: any = {
    type: '',
    url: '',
    options: Object,
  };
  encrypt_endPoint: CryptoJS.lib.CipherParams | undefined;
  aesKey: CryptoJS.lib.WordArray | undefined;
  getRole: String | undefined;
  userName: String | undefined;
  user_id: String | undefined;

  selectItems = [
    {
      id: 'Y',
      value: 'Yes',
    },
    {
      id: 'N',
      value: 'No',
    },
  ];
  selectActive = [
    {
      id: 'Active',
      value: 'Active',
    },
    {
      id: 'Inactive',
      value: 'Inactive',
    },
  ];
  workShiftDropDown = [
    {
      id: '1st',
      value: '1st',
    },
    {
      id: '2nd',
      value: '2nd',
    },
    {
      id: '3rd',
      value: '3rd',
    },
  ];
  onSiteDropDown = [
    {
      id: 'Y',
      value: 'Yes',
    },
    {
      id: 'N',
      value: 'No',
    },
  ];
  fsStatus = [
    {
      id: 'Active',
      value: 'Active',
    },
    {
      id: 'Inactive',
      value: 'Inactive',
    },
    {
      id: 'LOA',
      value: 'LOA',
    },
  ];
  businessOrgDropDown = [
    {
      id: 'TS',
      value: 'TS',
    },
    {
      id: 'MS',
      value: 'MS',
    },
    {
      id: 'RPPS',
      value: 'RPPS',
    },
  ];

  obsGetUserInfo: Observable<any> | undefined;
  private subGetUserInfo = new Subject<any>();
  constructor(
    public http: HttpClient,
    private ts: ToastrService,
    private router: Router
  ) {
    this.obsGetUserInfo = this.subGetUserInfo.asObservable();
  }
  setUserInfo(data: any) {
    this.subGetUserInfo.next(data);
    this.getRole = data?.data?.userRole;
    this.userName = data?.data?.userName;
    this.user_id = data?.data?.user_id;

  }

  clearHttp() {
    this.httpObj.type = '';
    this.httpObj.url = '';
    this.httpObj.options = {};
  }

  requestHttp(type: string, endPoint: string, body?: any, params?: any) {
    this.clearHttp();
    this.httpObj.type = type;

    if (type == 'post' || type == 'put') {
      let header = new HttpHeaders();
      header.append('Content-Type', 'application/json');
      header.append('Accept', 'application/json');
      this.httpObj.options.headers = header;
    }
    const q = endPoint.split('?');
    this.obsGetUserInfo?.subscribe((data) => {
      this.aesKey = CryptoJS.enc.Base64.parse(data?.data?.aesKey);
    });
    if (q[1] != undefined && this.aesKey != null) {
      this.encrypt_endPoint = CryptoJS.AES.encrypt(
        JSON.stringify(q[1]),
        this.aesKey,
        {
          keySize: 16,
          iv: this.aesKey,
          mode: CryptoJS.mode.CBC,
          padding: CryptoJS.pad.Pkcs7,
        }
      );
      this.httpObj.url =
        environment.apiURL + q[0] + '?' + this.encrypt_endPoint?.toString();
    } else {
      this.httpObj.url = environment.apiURL + q[0];
    }

    if (body !== false) {
      this.httpObj.options.body = body;
    }
    if (params !== false) {
      this.httpObj.options.params = params;
    }
    return this.http.request(
      this.httpObj.type,
      this.httpObj.url,
      this.httpObj.options
    );
  }
  handleError(
    error: any,
    type?: string,
    endPoint?: string,
    body?: any,
    params?: any
  ) {
    try {
      console.log(error.status);
      console.log(error);
      if (error.status == 502) {
        this.ts.error('Server Busy : Kindly re-try');
      }
      if (
        error.status == 401 &&
        error.error.message == 'The incoming token has expired'
      ) {
        this.ts.error('Time Out - Relogin required..');
      } else {
        if (error?.error?.errors[0]?.message) {
          this.ts.error(error?.error?.errors[0]?.message, 'Error in API', {

          });
        } else if (error.errors instanceof ErrorEvent) {
          this.ts.error(error?.errors?.message, 'Error in API', {

          });
        } else {
          this.ts.error(error?.message, 'Error in API', {

          });
        }
      }
    } catch (error) {
      console.log(error);
    }

  }


}
