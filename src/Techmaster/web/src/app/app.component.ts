import { Component, OnInit } from '@angular/core';
import { CoreService } from './service/core.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
})
export class AppComponent implements OnInit {
  constructor(public apiService: CoreService) { }
  title = 'Tech Master';
  ngOnInit() {
    this.apiService.requestHttp('get', '/user-info').subscribe(
      (Response) => {
       // this.apiService.obsGetUserInfo?.forEach((subscription) => subscription?.unsubscribe());
        this.apiService.setUserInfo(Response);
      },
      (error) => {
        console.log(error);
        this.apiService.handleError(error);
      }
    );
  }
}
