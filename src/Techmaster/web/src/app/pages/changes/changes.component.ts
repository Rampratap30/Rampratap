import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { FormBuilder, FormControl, FormGroup } from '@angular/forms';
import {
  ModalDismissReasons,
  NgbCalendar,
  NgbDate,
  NgbDateParserFormatter,
  NgbDateStruct,
  NgbDatepickerConfig,
  NgbModal,
} from '@ng-bootstrap/ng-bootstrap';
import {
  CheckboxSelectionCallbackParams,
  ColDef,
  GridOptions,
  HeaderCheckboxSelectionCallbackParams,
  IDatasource,
  IGetRowsParams,
  SelectionChangedEvent,
} from 'ag-grid-community';
import { ToastrService } from 'ngx-toastr';
import { Observable, filter } from 'rxjs';
import { RequestWithFilterAndSort } from 'src/app/common/types';
import { NgxSpinnerService } from 'ngx-spinner';
import { environment } from './../../../environments/environment';
import { CoreService } from 'src/app/service/core.service';
import { map } from 'jquery';
import { Router } from '@angular/router';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Component({
  selector: 'app-changes',
  templateUrl: './changes.component.html',
  styleUrls: ['./changes.component.css'],
})
export class ChangesComponent {
  defaultPageSize = environment.defaultPageSize;
  defaultDialogSize = environment.defaultDialogSize;
  isARDisabled = true;
  hoveredDate: NgbDate | null = null;
  fromDate!: NgbDate | null;
  toDate!: NgbDate | null;
  currentManager: any;
  date: any;
  searchDialog: any;
  apiURL = environment.apiURL;
  selectedManager: any[] = [];
  selectedEmployee: any[] = [];
  //ag-grid
  gridApi: any;
  gridColumnApi: any;
  gridApiDialog: any;
  gridColumnApiDialog: any;
  gridApiDialogM: any;
  gridColumnApiDialogM: any;
  public getRole: String | undefined;
  public paginationPageSize: number | undefined;

  public rowSelection: 'single' | 'multiple' = 'multiple';
  public rowSelectionDialog: 'single' | 'multiple' = 'single';

  frm!: FormGroup;
  get f() {
    return this.frm.controls;
  }
  frmTran!: FormGroup;
  get ft() {
    return this.frmTran.controls;
  }

  rowData: any[] = [];
  managerData: any[] = [];
  employeeData: any[] = [];
  btnDisabled: boolean = true;
  retriveValues: boolean = false;

  selectedList: any[] = [];

  status = [
    {
      id: 'Pending',
      value: 'Pending',
    },
    {
      id: 'Approved',
      value: 'Approved',
    },
    {
      id: 'Processed',
      value: 'Processed',
    },
    {
      id: 'Rejected',
      value: 'Rejected',
    },
  ];
  requestType = [
    {
      id: 'My Pending',
      value: 'My Pending',
    },
    {
      id: 'All Pending',
      value: 'All Pending',
    },
  ];

  requestTypeManager = [
    {
      id: 'My Pending',
      value: 'My Pending',
    }
  ];

  constructor(
    private toastr: ToastrService,
    private spinner: NgxSpinnerService,
    private cs: CoreService,
    private modalService: NgbModal,
    private fb: FormBuilder,
    private calendar: NgbCalendar,
    public formatter: NgbDateParserFormatter,
    private router: Router,
    private http: HttpClient,
    private config: NgbDatepickerConfig,
  ) {
    //this.fromDate = calendar.getToday();
    //this.toDate = calendar.getNext(calendar.getToday(), 'd', 10);
    const current = new Date();
    config.minDate = {
      month: current.getMonth() + 1,
      day: current.getDate(),
      year: current.getFullYear() - 5,
    };
  }


  onDateSelection(date: NgbDate) {
    if (!this.fromDate && !this.toDate) {
      this.fromDate = date;
    } else if (
      this.fromDate && !this.toDate
      // &&
      // date &&
      // date.after(this.fromDate)
    ) {
      this.toDate = date;
    } else {
      this.toDate = null;
      this.fromDate = date;
    }
  }

  isHovered(date: NgbDate) {
    return (
      this.fromDate &&
      !this.toDate &&
      this.hoveredDate &&
      date.after(this.fromDate) &&
      date.before(this.hoveredDate)
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
    return parsed && this.calendar.isValid(NgbDate.from(parsed))
      ? NgbDate.from(parsed)
      : currentValue;
  }

  ngOnInit(): void {
    if (!this.cs.getRole) {
      this.cs.obsGetUserInfo?.subscribe((data) => {
        this.getRole = data?.data?.userRole;
      });
    } else {
      this.getRole = this.cs.getRole;
    }

    let response = (localStorage.getItem("retriveValues"));
    if (response == "false" || response == null) {
      this.frm = this.fb.group({
        managerName: '',
        empName: '',
        fromDate: '',
        toDate: '',
        status: '',
        requestType: 'My Pending',
        changeID: '',
        requestedBy: '',
      });
      if (this.getRole == 'ADMIN') {
        this.frm.patchValue({
          requestType: 'All Pending'
        });
      }
      const obj = {
        managerName: '',
        empName: '',
        fromDate: '',
        toDate: '',
        status: '',
        requestType: this.frm.value.requestType,
        changeID: '',
        requestedBy: ''
      }
      localStorage.setItem("filteredlist", JSON.stringify(obj));
    } else {
      const responses = JSON.parse(localStorage.getItem('filteredlist') || '{}');
      let lv_from_date = '';
      if (responses["fromDate"]) {
        let _from_date = responses["fromDate"].split('-');
        lv_from_date = _from_date[1] + '/' + _from_date[2] + '/' + _from_date[0];

      }
      let lv_to_date = '';
      if (responses["toDate"]) {
        let _to_date = responses["toDate"].split('-');
        lv_to_date = _to_date[1] + '/' + _to_date[2] + '/' + _to_date[0];

      }

      this.frm = this.fb.group({
        managerName: responses["managerName"],
        empName: responses["empName"],
        fromDate: lv_from_date,
        toDate: lv_to_date,
        status: responses["status"],
        requestType: responses["requestType"],
        changeID: responses["changeID"],
        requestedBy: responses["requestedBy"],
      });

    }
  }

  clearData() {
    this.frm.reset();
    this.fromDate = null
    this.toDate = null
    while (this.selectedManager.length) {
      this.selectedManager.pop();
    }
    localStorage.removeItem("filteredlist");
    localStorage.removeItem("retriveValues");
    if (
      localStorage.getItem("changeScreenSortList")
    ) {
      localStorage.removeItem("changeScreenSortList");
      localStorage.removeItem("changeScreenColList");
    }

    this.gridApi.setDatasource(this.dataSource);
  }
  openSearchDialogManager(val: any) {
    this.searchDialog = val;
    this.gridApiDialogM.setDatasource(this.dataSourceManager);
  }

  openSearchDialog(val: any) {
    this.searchDialog = val;
    this.gridApiDialog.setDatasource(this.dataSourceEmployee);
  }
  public defaultColDef: ColDef = {
    flex: 1,
    minWidth: 100,
  };

  columnDefs: any = [
    {
      headerName: 'Change ID',
      field: 'change_id',
      sortable: true,
      width: 150,
      pinned: 'left',
      lockPinned: true,
      cellClass: 'lock-pinned',
      headerCheckboxSelection: true,
      headerCheckboxSelectionFilteredOnly: true,
      checkboxSelection: true,
      cellRenderer: this.createHyperLink.bind(this),
    },
    {
      headerName: 'Employee ID',
      field: 'employee_id',
      sortable: true,
      width: 150,
    },
    {
      headerName: 'Employee Name',
      field: 'employee_name',
      sortable: true,
      width: 200,
    },
    {
      headerName: 'Manager Name',
      field: 'manager_name',
      sortable: true,
      width: 200,
    },
    {
      headerName: 'Change Note',
      field: 'change_note',
      sortable: true,
      width: 160,
    },
    {
      headerName: 'Effective Date',
      field: 'change_effective_date',
      sortable: true,
      width: 160,
    },
    {
      headerName: 'Requested By',
      field: 'requested_by',
      sortable: true,
      width: 165,
    },
    { headerName: 'Change Status', field: 'status', sortable: true, width: 150 },
    { headerName: 'Admin Notes', field: 'admin_notes', sortable: true, width: 150 },
    { headerName: 'HR Status', field: 'hr_status', sortable: true, width: 150 },
    { headerName: 'FS Status', field: 'fs_status', sortable: true, width: 150 },
    { headerName: 'Business Org', field: 'business_org', sortable: true, width: 150 },
  ];

  managercolumnDefs: any = [
    { headerName: 'Id', field: 'manager_id', width: 100, sortable: true },
    { headerName: 'Name', field: 'manager_name', width: 265, sortable: true },
  ];

  employeecolumnDefs: any = [
    { headerName: 'Name', field: 'employee_name', sortable: true },
    { headerName: 'Id', field: 'employee_id', width: 100, sortable: true },
    { headerName: 'Resource Number', field: 'resource_number', sortable: true },
  ];

  gridOptions: GridOptions = {
    defaultColDef: {
      sortable: true,
      unSortIcon: true,
      resizable: true,
      //filter:true,
    },
    noRowsOverlayComponent: '<div>no rows</div>',
    rowModelType: 'infinite',
  };

  createHyperLink(params: any): any {
    if (!params.data) {
      return;
    }
    let keyData = params.valueFormatted ? params.valueFormatted : params.value;
    let employee_id = params.data.employee_id;
    let syncup = params.data.syncup_type;
    let status = params.data.status;
    const spanElement = document.createElement('span');
    spanElement.innerHTML = `<a class="idUnderline" href="javascript:void(0);"> ${keyData}</a>`;
    if ((syncup == null || syncup == 'Manager_Transfer') && status == 'Pending') {
      spanElement.addEventListener('click', ($event) => {
        $event.preventDefault();
        this.router.navigate([
          '/viewChanges/' + btoa(keyData) + '/' + btoa(employee_id),
        ]);
      });

    }
    else {
      spanElement.addEventListener('click', ($event) => {
        $event.preventDefault();
        this.router.navigate([
          '/viewSyncup/' + btoa(keyData) + '/' + btoa(employee_id),
        ]);
      });
    }



    return spanElement;
  }
  onGridReadyDialogM(params: any) {
    this.gridApiDialogM = params.api;
    this.gridColumnApiDialogM = params.columnApi;
    //this.gridApiDialogM.setDatasource(this.dataSourceManager);
  }

  onGridReadyDialog(params: any) {
    this.gridApiDialog = params.api;
    this.gridColumnApiDialog = params.columnApi;
    //this.gridApiDialog.setDatasource(this.dataSourceEmployee);
  }

  onSearchSubmit() {
    if (
      localStorage.getItem("changeScreenSortList")
    ) {
      localStorage.removeItem("changeScreenSortList");
      localStorage.removeItem("changeScreenColList");
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
    }

    const obj = {
      managerName: this.frm.value.managerName,
      empName: this.frm.value.empName,
      fromDate: lv_from_date,
      toDate: lv_to_date,
      status: this.frm.value.status,
      requestType: this.frm.value.requestType,
      changeID: this.frm.value.changeID,
      requestedBy: this.frm.value.requestedBy
    }
    localStorage.setItem("filteredlist", JSON.stringify(obj));
    this.retriveValues = false;
    localStorage.setItem("retriveValues", `${this.retriveValues}`);
    this.gridApi.setDatasource(this.dataSource);

  }

  onGridReady(params: any) {
    this.gridApi = params.api;
    this.gridColumnApi = params.columnApi;
    this.gridApi.setDatasource(this.dataSource);
  }
  dataSourceManager: IDatasource = {
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
      this.getManagers(
        request,
        this.gridApiDialogM.paginationGetCurrentPage(),
        this.gridApiDialogM.paginationGetPageSize()
      ).subscribe({
        next: (response: any) => {
          this.spinner.hide();
          params.successCallback(
            response['data'].records,
            response['data'].total_items
          );
        },
        error: (err: any) => {
          this.spinner.hide();
          this.cs.handleError(err);
        },
      });
    },
  };

  getManagers(
    requestWithSortAndFilter: RequestWithFilterAndSort,
    page: number,
    size: number
  ) {
    page++;
    let url = 'api/home/get_manager_list?';
    let query = '';
    if (this.frm.value.managerName) {
      query += 'manager_name=' + this.frm.value.managerName + '&';
    }
    query += 'page=' + page + '&per_page=' + size;
    if (requestWithSortAndFilter.colId) {
      query +=
        '&order_by=' +
        requestWithSortAndFilter.colId +
        '&order=' +
        requestWithSortAndFilter.sort;
    }
    let requestURL = url + query;
    return this.cs.requestHttp('get', requestURL);

    //this.cs.req('get', this.cs.appUrl + 'home/home_manager.json');
    //return this.cs.getHttp();
  }

  dataSourceEmployee: IDatasource = {
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
      this.getEmployee(
        request,
        this.gridApiDialog.paginationGetCurrentPage(),
        this.gridApiDialog.paginationGetPageSize()
      ).subscribe({
        next: (response: any) => {
          this.spinner.hide();
          params.successCallback(
            response['data'].records,
            response['data'].total_items
          );
        },
        error: (err: any) => {
          this.spinner.hide();
          this.cs.handleError(err);
        },
      });
    },
  };

  getEmployee(
    requestWithSortAndFilter: RequestWithFilterAndSort,
    page: number,
    size: number
  ) {
    page++;
    let url = 'api/home/get_employee_list?';
    let query = '';
    query += 'page=' + page + '&per_page=' + size + '&change_screen=Y';
    if (requestWithSortAndFilter.colId) {
      query +=
        '&order_by=' +
        requestWithSortAndFilter.colId +
        '&order=' +
        requestWithSortAndFilter.sort;
    }
    if (this.selectedManager.length > 0) {
      query +=
        '&manager_id=' +
        this.selectedManager[0].manager_id +
        '&manager_name=' +
        this.selectedManager[0].manager_name +
        '&';
    }
    if (this.frm.value.empName) {
      query += '&q=' + this.frm.value.empName;
    }
    let requestURL = url + query;
    return this.cs.requestHttp('get', requestURL);
    // this.cs.setHttp('get', this.cs.appUrl + 'home/home_employee.json');
    // return this.cs.getHttp();
  }

  //Dashboard
  dataSource: IDatasource = {
    getRows: (params: IGetRowsParams) => {
      let sort = undefined;
      let colId = undefined;
      if (params.sortModel[0]) {
        sort = params.sortModel[0].sort;
        colId = params.sortModel[0].colId;
        localStorage.setItem("changeScreenSortList", sort);
        localStorage.setItem("changeScreenColList", colId);
      }
      else {
        let sortResponse = (localStorage.getItem("changeScreenSortList"));
        let colIdResponse = (localStorage.getItem("changeScreenColList"));
        if ((sortResponse != 'undefined' || sortResponse != null) && (colIdResponse != 'undefined' || colIdResponse != null)) {
          sort = sortResponse;
          colId = colIdResponse;
        }
      }
      console.log(colId);
      console.log(sort);
      this.spinner.show();
      let request: RequestWithFilterAndSort = {
        colId: colId,
        sort: sort,
        filterModel: undefined,//params.filterModel,
        data: undefined,
      };
      console.log(colId);
      console.log(sort);
      this.get_dashboard_data(
        request,
        this.gridApi.paginationGetCurrentPage(),
        this.gridApi.paginationGetPageSize()
      ).subscribe({
        next: (response: any) => {
          params.successCallback(
            response['data'].records,
            response['data'].total_items
          );
          this.gridApi.hideOverlay();
          if (response['data'].total_items <= 0) {
            this.gridApi.showNoRowsOverlay();
          }
        },
        error: (err: any) => {
          this.spinner.hide();
          this.cs.handleError(err);
        },
        complete: () => {
          this.spinner.hide();
          //localStorage.removeItem("retriveValues");
        }
      });
    },
  };

  get_dashboard_data(
    requestWithSortAndFilter: RequestWithFilterAndSort,
    page: number,
    size: number
  ) {
    let response = (localStorage.getItem("retriveValues"));
    let requestURL = 'api/changes/get';
    if (response == null || !response || response == 'false') {
      page++;
      let obj = {
        is_export_all: 'N',
        manager_name: '',
        q: '',
        status: '',
        change_type: '',
        order_by: 'change_id',
        order: 'desc',
        page: page,
        per_page: size,
        from_date: '',
        to_date: '',
        request_type: '',
        change_id: '',
        requested_by: '',
      };
      if (requestWithSortAndFilter.colId) {
        obj.order_by = requestWithSortAndFilter.colId;
        obj.order = requestWithSortAndFilter.sort;
        console.log(requestWithSortAndFilter.colId);
        console.log(requestWithSortAndFilter.sort);
      }
      if (this.selectedManager.length > 0) {
        obj.manager_name = this.selectedManager[0].manager_name;
      }
      if (this.frm.value.empName) {
        obj.q = this.frm.value.empName;
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
      }

      if (lv_from_date) {
        obj.from_date = lv_from_date;
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
      }

      if (lv_to_date) {
        obj.to_date = lv_to_date
      }
      //  if (this.fromDate) {
      //    let date = this.fromDate;
      //    let month = ('0' + (new Date(date.year + '-' + date.month + '-' + date.day).getUTCMonth() + 1)).slice(-2);
      //    let day = ('0' + new Date(date.year + '-' + date.month + '-' + date.day).getUTCDate()).slice(-2);
      //    obj.from_date = date.year + '-' + month + '-' + day;
      //  }
      //  console.log(this.fromDate)
      //  if (this.toDate) {
      //    let date = this.toDate;
      //    let month = ('0' + (new Date(date.year + '-' + date.month + '-' + date.day).getUTCMonth() + 1)).slice(-2);
      //    let day = ('0' + new Date(date.year + '-' + date.month + '-' + date.day).getUTCDate()).slice(-2);
      //    obj.to_date = date.year + '-' + month + '-' + day;
      //  }
      if (this.frm.value.status) {
        obj.status = this.frm.value.status;
      }
      if (this.frm.value.requestType) {
        obj.request_type = this.frm.value.requestType;
      }
      if (this.frm.value.changeID) {
        obj.change_id = this.frm.value.changeID;
      }
      if (this.frm.value.requestedBy) {
        obj.requested_by = this.frm.value.requestedBy;
      }
      return this.cs.requestHttp('post', requestURL, obj, false);
    } else {
      page++;
      const responses = JSON.parse(localStorage.getItem('filteredlist') || '{}');
      // this.fromDate = responses["fromDate"]
      // this.toDate = responses["toDate"]
      let obj = {
        is_export_all: 'N',
        manager_name: '',
        q: '',
        status: '',
        change_type: '',
        order_by: 'change_id',
        order: 'desc',
        page: page,
        per_page: size,
        from_date: '',
        to_date: '',
        request_type: '',
        change_id: '',
        requested_by: ''
      };
      if (requestWithSortAndFilter.colId) {
        obj.order_by = requestWithSortAndFilter.colId;
        obj.order = requestWithSortAndFilter.sort;
        console.log(requestWithSortAndFilter.colId);
        console.log(requestWithSortAndFilter.sort);
      }
      if (responses["managerName"]) {
        obj.manager_name = responses["managerName"];
      }
      if (responses["empName"]) {
        obj.q = responses["empName"];
      }
      if (responses["status"]) {
        obj.status = responses["status"];
      }
      if (responses["fromDate"]) {
        obj.from_date = responses["fromDate"];
      }
      if (responses["toDate"]) {
        obj.to_date = responses["toDate"];
      }

      // if (responses["fromDate"]) {
      //   let date = responses["fromDate"];
      //   let month = ('0' + (new Date(date.year + '-' + date.month + '-' + date.day).getUTCMonth() + 1)).slice(-2);
      //   let day = ('0' + new Date(date.year + '-' + date.month + '-' + date.day).getUTCDate()).slice(-2);
      //   obj.from_date = date.year + '-' + month + '-' + day;
      // }
      // if (responses["toDate"]) {
      //   let date = responses["toDate"];
      //   let month = ('0' + (new Date(date.year + '-' + date.month + '-' + date.day).getUTCMonth() + 1)).slice(-2);
      //   let day = ('0' + new Date(date.year + '-' + date.month + '-' + date.day).getUTCDate()).slice(-2);
      //   obj.to_date = date.year + '-' + month + '-' + day;
      // }
      if (responses["requestType"]) {
        obj.request_type = responses["requestType"];
      }
      if (responses["changeID"]) {
        obj.change_id = responses["changeID"];
      }
      if (responses["requestedBy"]) {
        obj.requested_by = responses["requestedBy"];
      }

      //localStorage.removeItem("filteredlist");
      return this.cs.requestHttp('post', requestURL, obj, false);
    }
    //this.cs.setHttp('get', this.cs.appUrl + 'changes/changes.json');
    //return this.cs.getHttp();
  }

  onPageSizeChanged(event: any) {
    this.gridApi.paginationSetPageSize(Number(event.target.value));
  }

  @ViewChild('closebutton') closebutton!: {
    nativeElement: { click: () => void };
  };
  @ViewChild('closebuttonm') closebuttonm!: {
    nativeElement: { click: () => void };
  };

  onSelectionChangedDialogM(event: SelectionChangedEvent) {
    const selectedRows = this.gridApiDialogM.getSelectedRows();
    if (selectedRows.length === 1) {
      this.clearData();
      this.selectedManager = selectedRows;
      this.frm.controls['managerName'].setValue(selectedRows[0].manager_name);
      this.closebuttonm.nativeElement.click();
    }
  }

  onSelectionChangedDialog(event: SelectionChangedEvent) {
    const selectedRows = this.gridApiDialog.getSelectedRows();
    if (selectedRows.length === 1) {
      this.selectedEmployee = selectedRows;
      this.frm.controls['empName'].setValue(selectedRows[0].employee_name);
      this.closebutton.nativeElement.click();
    }
  }

  onSelectionChanged(event: SelectionChangedEvent) {
    this.selectedList = this.gridApi.getSelectedRows();
    this.isARDisabled = true;
    if (this.selectedList.length >= 1) {
      this.isARDisabled = false;
    }
  }

  onApprove() {
    if (this.selectedList.length >= 1) {
      const selectedrecords = this.selectedList.filter(
        (el: any) => el.status == 'Pending'
      );
      if (this.selectedList.length == selectedrecords.length) {
        let url = 'api/changes/bulk-approved';
        let setData = this.selectedList.map((change: any) => change.change_id);
        let obj = { change_id: setData };
        this.cs.requestHttp('put', url, obj, undefined).subscribe({
          next: (response: any) => {
            this.toastr.success(response.data.message);
            this.gridApi.setDatasource(this.dataSource);
            this.isARDisabled = true;
          },
          error: (err: any) => {
            this.cs.handleError(err);
          },
        });
      } else {
        this.toastr.error('Please select only pending record');
      }
    }
  }
  onReject() {
    if (this.selectedList.length >= 1) {
      const selectedrecords = this.selectedList.filter(
        (el: any) => el.status == 'Pending'
      );
      if (this.selectedList.length == selectedrecords.length) {
        let url = 'api/changes/bulk-rejected';
        let setData = this.selectedList.map((change: any) => change.change_id);
        let obj = { change_id: setData };
        this.cs.requestHttp('put', url, obj, undefined).subscribe({
          next: (response: any) => {
            this.toastr.success(response.data.message);
            this.gridApi.setDatasource(this.dataSource);
            this.isARDisabled = true;
          },
          error: (err: any) => {
            this.cs.handleError(err);
          },
        });
      } else {
        this.toastr.error('Please select only pending record');
      }
    }
  }

  //Bulk import logic
  file!: File;
  maxsize: number = 10;
  docExt!: String

  @ViewChild('fileUploader') fileUploader!: ElementRef;

  resetFileUploader() {
    this.fileUploader.nativeElement.value = null;
  }
  // onImport(){ 
  //   console.log("inside import.")
  //   this.resetFileUploader()
  // }
  onChange(event: any) {
    if (event.target.files.length > 0) {
      this.file = event.target.files[0];
      const selResult = event.target.value.split('.');
      this.docExt = selResult.pop();
    }
  }
  // OnClick of button Upload 
  onUpload() {
    if (this.file && this.docExt.toLowerCase() == 'csv') {
      if ((this.file.size / 1048576) > this.maxsize) {
        this.toastr.error("Required file size should be less than " + this.maxsize + " MB.");
      } else {
        this.upload(this.file).subscribe({
          next: (response: any) => {
            // this.toastr.success(response.data.message);
            this.resetFileUploader()
            let url = "/api/changes/bulk_import"
            let obj = {
              "type": "Bulk Import",
              "msg": "Bulk Import",
              "file_name": response.data.filename
            }
            this.cs.requestHttp('POST', url, obj, false).subscribe({
              next: (response: any) => {
                this.toastr.success(response.data.message);
                this.frm.reset();
              },
              error: (err: any) => {
                this.spinner.hide();
                this.cs.handleError(err);
              },
              complete: () => {
                this.spinner.hide();
              },
            });
          },
          error: (err: any) => {
            this.cs.handleError(err);
          },
          complete: () => {
            this.modalService.dismissAll()
          },
        });
      }
    } else {
      this.toastr.error('Please select CSV file')
    }
  }

  upload(file: Blob): Observable<any> {
    // Create form data 
    const formData = new FormData();
    formData.append("file", file);
    let headers = new HttpHeaders();
    headers.append('Content-Type', 'multipart/form-data');
    return this.http.post(environment.apiURL + '/bulk-upload', formData, { headers: headers })
  }

  ngOnDestroy(): void {
    this.spinner.show();
    this.modalService.dismissAll();
    //  this.subscribeCls && this.subscribeCls.unsubscribe();
  }
}
