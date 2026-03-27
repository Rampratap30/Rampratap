import { Component } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { NgxSpinnerService } from 'ngx-spinner';
import { ToastrService } from 'ngx-toastr';
import { ngxCsv } from 'ngx-csv';
import { CoreService } from 'src/app/service/core.service';

@Component({
  selector: 'app-reports',
  templateUrl: './reports.component.html',
  styleUrls: ['./reports.component.css'],
})
export class ReportsComponent {
  frm!: FormGroup;
  get f() {
    return this.frm.controls;
  }

  isARDisabled = true;

  constructor(
    private cs: CoreService,
    private fb: FormBuilder,
    private spinner: NgxSpinnerService,
    private toastr: ToastrService
  ) { }
  ngOnInit(): void {
    this.spinner.show();
    this.frm = this.fb.group({
      employeeStatus: ['All'],
    });
    this.spinner.hide();
  }
  employeeStatus = [
    {
      id: 'All',
      value: 'All',
    },
    {
      id: 'Active',
      value: 'Active',
    },
  ];
  downloadCSV() {
    this.spinner.show();
    let types: any;
    if (this.frm.value.employeeStatus) {
      types = this.frm.value.employeeStatus;
    }
    let url = '/api/home/bulk_export?type=Report_Screen';
    let obj = {
      msg: 'Report Screen',
      type: 'report',
      attribute1: types
    };
    this.cs.requestHttp('post', url, obj).subscribe({
      next: (response: any) => {
        this.toastr.success(
          'Request ID : ' +
          response['data'].records[0].log_id +
          ' Message: ' +
          response['data'].message
        );
      },
      error: (err) => {
        this.cs.handleError(err);
        this.spinner.hide();
      },
      complete: () => {
        this.spinner.hide();
      },
    });
  }

  onSearchSubmit() { }
  clearData() {
    this.frm.reset();
  }
}
