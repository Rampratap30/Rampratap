import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { AppComponent } from 'src/app/app.component';
import { AppModule } from 'src/app/app.module';
import { CoreService } from 'src/app/services/core.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css'],
})
export class HomeComponent implements OnInit {
  constructor(
    public cs: CoreService,
    private router: Router,
    private route: ActivatedRoute,
    private app: AppComponent
  ) {}
  responseData: any;
  q_param: string | undefined;
  isLoading = false;

  ngOnInit() {
    this.route.queryParams.subscribe({
      next: (params: any) => {
        this.q_param = params['param'];        
        if (this.q_param) {
          this.isLoading = true;
          this.getData();
        } else {
          this.router.navigate(['PageNotFoundComponent'], {
            skipLocationChange: true,
          });
        }
      },
    });
  }

  getData() {
    //let url = '/assets/json/new-order-ship.json';
    let url = '/api/home/getdata?param=' + this.q_param;
    this.cs.requestHttp('get', url).subscribe({
      next: (response: any) => {
        this.responseData = response;
      },
      error: (err: any) => {
        this.isLoading = false;
        this.router.navigate(['PageNotFoundComponent'], {
          skipLocationChange: true,
        });
        console.log(err.status);
        console.log(err);
      },
      complete: () => {
        this.isLoading = false;
        if (this.responseData['data']?.display_page) {
          switch (this.responseData['data']?.display_page) {
            case '1':
              this.router.navigate(['multipleShipto'], {
                skipLocationChange: true,
                queryParams: { filter: JSON.stringify(this.responseData) },
              });
              break;
            case '2':
              this.router.navigate(['cdnMultipleShipto'], {
                skipLocationChange: true,
                queryParams: { filter: JSON.stringify(this.responseData) },
              });
              break;
            case '3':
              this.router.navigate(['cdnSingleShipto'], {
                skipLocationChange: true,
                queryParams: { filter: JSON.stringify(this.responseData) },
              });
              break;
            default:
              this.router.navigate(['PageNotFoundComponent'], {
                skipLocationChange: true,
              });
              break;
          }
        } else {
          this.router.navigate(['PageNotFoundComponent'], {
            skipLocationChange: true,
          });
        }
      },
    });
  }
}
