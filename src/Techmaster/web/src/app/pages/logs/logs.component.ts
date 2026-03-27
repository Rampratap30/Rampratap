
import { Component } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { NgbCalendar, NgbDate, NgbDateParserFormatter, NgbDatepickerConfig } from '@ng-bootstrap/ng-bootstrap';
import { GridOptions, IDatasource, IGetRowsParams } from 'ag-grid-community';
import { NgxSpinnerService } from 'ngx-spinner';
import { ToastrService } from 'ngx-toastr';
import { RequestWithFilterAndSort } from 'src/app/common/types';
import { CoreService } from 'src/app/service/core.service';
import { environment } from './../../../environments/environment';
import { ngxCsv } from 'ngx-csv';

@Component({
  selector: 'app-logs',
  templateUrl: './logs.component.html',
  styleUrls: ['./logs.component.css']
})
export class LogsComponent {
  private gridApi: any;
  private gridColumnApi: any;
  defaultPageSize = environment.defaultPageSize;
  frm!: FormGroup;
  get f() { return this.frm.controls };

  isARDisabled = true;
  hoveredDate: NgbDate | null = null;
  fromDate!: NgbDate | null;
  toDate!: NgbDate | null;
  rowData: any[] = [];
  activeTab = 1;
  empIdDisable: boolean = false;

  constructor(
    private toastr: ToastrService,
    private spinner: NgxSpinnerService,
    private cs: CoreService,
    private fb: FormBuilder,
    private calendar: NgbCalendar,
    public formatter: NgbDateParserFormatter,
    private config: NgbDatepickerConfig,
  ) {
    // this.fromDate = calendar.getToday();
    //this.toDate = calendar.getNext(calendar.getToday(), 'd', 10);
    const current = new Date();
    config.minDate = {
      month: current.getMonth() + 1,
      day: current.getDate(),
      year: current.getFullYear() - 5,
    };
  }

  ngOnInit(): void {
    this.frm = this.fb.group({
      from_date: [''],
      to_date: [''],
      logsFor: [''],
      search_emp_id: [''],
    })
  }

  logsFor = [
    {
      id: 'OFSC',
      value: 'OFSC'
    },
    {
      id: 'HRMS',
      value: 'HRMS'
    },
    // {
    //   id: 'CSA Notification',
    //   value: 'CSA Notification'
    // },
    {
      id: 'Bulk Import',
      value: 'Bulk Import'
    },
    {
      id: 'home',
      value: 'Bulk Export'
    },
    {
      id: 'LOG',
      value: 'LOG'
    }
  ]
  onDateSelection(date: NgbDate) {
    if (!this.fromDate && !this.toDate) {
      this.fromDate = date;
    } else if (this.fromDate && !this.toDate
      // && date && date.after(this.fromDate)
    ) {
      this.toDate = date;
    } else {
      this.toDate = null;
      this.fromDate = date;
    }
  }

  isHovered(date: NgbDate) {
    return (
      this.fromDate && !this.toDate && this.hoveredDate && date.after(this.fromDate) && date.before(this.hoveredDate)
    );
  }

  isInside(date: NgbDate) {
    return this.toDate && date.after(this.fromDate) && date.before(this.toDate);
  }

  isRange(date: NgbDate) {
    return (
      date.equals(this.fromDate) ||
      (this.toDate && date.equals(this.toDate)) ||
      this.isInside(date) ||
      this.isHovered(date)
    );
  }

  validateInput(currentValue: NgbDate | null, input: string): NgbDate | null {
    const parsed = this.formatter.parse(input);
    return parsed && this.calendar.isValid(NgbDate.from(parsed)) ? NgbDate.from(parsed) : currentValue;
  }

  clearData() {
    this.frm.reset();
    this.fromDate = null;
    this.toDate = null;
    this.empIdDisable = false;
    this.gridApi.setDatasource(this.dataSource);
  }
  columnDefs: any = [
    { headerName: 'Employee ID', field: 'employee_id' },
    { headerName: 'Resource Number', field: 'resource_number' },
    { headerName: 'Email ID', field: 'email_id' },
    { headerName: 'File Name', field: 'file_name' },
    { headerName: 'Lambda Status', field: 'lambda_status' },
    { headerName: 'Message', field: 'message' },
    { headerName: 'Type', field: 'type' },
    { headerName: 'Creation Date', field: 'created_date' },
    { headerName: 'Created By', field: 'created_by' }
  ];

  gridOptions: GridOptions = {
    defaultColDef: {
      sortable: false,
      //resizable: true,
      //filter:true,
    },
    rowModelType: 'infinite',
  }

  onGridReady(params: any) {
    this.gridApi = params.api;
    this.gridColumnApi = params.columnApi;
    //this.gridApi.setDatasource(this.dataSource);
  }
  autoSizeAll(skipHeader: boolean) {
    const allColumnIds: string[] = [];
    this.gridColumnApi.getColumns()!.forEach((column: any) => {
      allColumnIds.push(column.getId());
    });
    this.gridColumnApi.autoSizeColumns(allColumnIds, skipHeader);
  }

  //Dashboard
  dataSource: IDatasource = {
    getRows: (params: IGetRowsParams) => {
      let sort = undefined;
      let colId = undefined;
      if (params.sortModel[0]) {
        sort = params.sortModel[0].sort;
        colId = params.sortModel[0].colId;
      }
      this.spinner.show();
      let request: RequestWithFilterAndSort = {
        colId: colId,
        sort: sort,
        filterModel: params.filterModel,
        data: undefined,
      };
      this.get_dashboard_data(
        request,
        this.gridApi.paginationGetCurrentPage(),
        this.gridApi.paginationGetPageSize()
      ).subscribe({
        next: (response: any) => {
          this.spinner.hide();
          params.successCallback(
            response['data'].records,
            response['data'].total_items
          );
          this.autoSizeAll(false)
          this.gridApi.hideOverlay()
          if (response['data'].total_items <= 0) {
            this.gridApi.showNoRowsOverlay();
          }
        },
        error: (err: any) => {
          this.spinner.hide();
          this.cs.handleError(err);
        },
      });
    },
  };

  get_dashboard_data(
    requestWithSortAndFilter: RequestWithFilterAndSort,
    page: number,
    size: number
  ) {
    page++;
    let url = "api/logs/get?";
    let query = 'page=' + page + '&per_page=' + size
    if (requestWithSortAndFilter.colId) {
      query += '&order_by=' + requestWithSortAndFilter.colId + '&order=' + requestWithSortAndFilter.sort
    }

    if (this.frm.value.logsFor) {
      query += "&type=" + this.frm.value.logsFor;
    }

    if (this.frm.value.search_emp_id) {
      query += "&search_emp_id=" + this.frm.value.search_emp_id;
    }

    let _from_date = this.fromDate;
    let lv_from_date;
    if (_from_date) {
      const a_s_ra = new Date(
        _from_date.year +
        '-' +
        _from_date.month +
        '-' +
        _from_date.day
      );
      let a_s_month = ('0' + (a_s_ra.getMonth() + 1)).slice(-2);
      let a_s_day = ('0' + _from_date.day).slice(-2);
      lv_from_date =
        _from_date.year + '-' + a_s_month + '-' + a_s_day;
      query += "&from_date=" + lv_from_date;
    }

    let _to_date = this.toDate;
    let lv_to_date;
    if (_to_date) {
      const a_s_ra = new Date(
        _to_date.year +
        '-' +
        _to_date.month +
        '-' +
        _to_date.day
      );
      let a_s_month = ('0' + (a_s_ra.getMonth() + 1)).slice(-2);
      let a_s_day = ('0' + _to_date.day).slice(-2);
      lv_to_date =
        _to_date.year + '-' + a_s_month + '-' + a_s_day;
      query += "&to_date=" + lv_to_date;
    }

    // if (this.fromDate) {
    //   let date = this.fromDate;
    //   //const a = new Date(date.year + '-' + date.month + '-' + date.day);
    //   //let month = ('0' + (a.getMonth() + 1)).slice(-2);
    //   //let day = ('0' + a.getDate()).slice(-2);
    //   let month = ('0' + (new Date(date.year + '-' + date.month + '-' + date.day).getUTCMonth() + 1)).slice(-2);
    //   let day = ('0' + new Date(date.year + '-' + date.month + '-' + date.day).getUTCDate()).slice(-2);
    //   query += "&from_date=" + date.year + '-' + month + '-' + day;
    // }
    // if (this.toDate) {
    //   let date = this.toDate;
    //   //const a = new Date(date.year + '-' + date.month + '-' + date.day);
    //   //let month = ('0' + (a.getMonth() + 1)).slice(-2);
    //   //let day = ('0' + a.getDate()).slice(-2);
    //   let month = ('0' + (new Date(date.year + '-' + date.month + '-' + date.day).getUTCMonth() + 1)).slice(-2);
    //   let day = ('0' + new Date(date.year + '-' + date.month + '-' + date.day).getUTCDate()).slice(-2);
    //   query += "&to_date=" + date.year + '-' + month + '-' + day;
    // }

    let requestURL = url + query;
    console.log(requestURL)
    return this.cs.requestHttp('get', requestURL, false);
  }

  onSearchSubmit() {
    this.gridApi.setDatasource(this.dataSource);
  }
  onPageSizeChanged(event: any) {
    this.gridApi.paginationSetPageSize(Number(event.target.value));
  }

  logForSelectevent(event: any) {
    if (this.frm.value.logsFor == 'HRMS') {
      this.empIdDisable = true;
    }
    else {
      this.empIdDisable = false;
    }
  }

  logForRemoveevent(event: any) {
    this.empIdDisable = false;

  }

  onBtExportBulk() {
    this.spinner.show();
    let url = '/api/logs/bulk_export?type=Log_Screen';
    let obj = {
      msg: 'Log Screen',
      type: 'LOG',
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

}
