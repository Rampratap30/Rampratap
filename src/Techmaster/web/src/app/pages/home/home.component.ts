import { Component, OnInit, ViewChild } from '@angular/core';
import { FormBuilder, FormControl, FormGroup } from '@angular/forms';
import {
  ModalDismissReasons,
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
import { NgxSpinnerService } from 'ngx-spinner';
import { ToastrService } from 'ngx-toastr';
import { RequestWithFilterAndSort } from 'src/app/common/types';
import { CoreService } from 'src/app/service/core.service';
import { environment } from './../../../environments/environment';
import { Router } from '@angular/router';
@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css'],
})
export class HomeComponent implements OnInit {

  currentManager: any;
  date: any;
  searchDialog: any;
  btnDisabled: boolean = true;
  //ag-grid
  defaultPageSize = environment.defaultPageSize;
  defaultDialogSize = environment.defaultDialogSize;
  gridApi: any;
  gridColumnApi: any;
  gridApiDialog: any;
  gridColumnApiDialog: any;
  gridApiDialogM: any;
  gridColumnApiDialogM: any;
  getRole: String | undefined;
  getUserName: String | undefined;
  user_id: String | undefined;
  encoded_employee_id!: String;
  rc_employee_name!: String;
  rc_hr_status!: String;
  btnDisableds: boolean = true;
  public paginationPageSize: number | undefined;
  public rowSelection: 'single' | 'multiple' = 'multiple';
  public rowSelectionDialog: 'single' | 'multiple' = 'single';
  retriveValuesHome: boolean = false;

  frm!: FormGroup;
  get f() {
    return this.frm.controls;
  }
  frmTran!: FormGroup;
  get ft() {
    return this.frmTran.controls;
  }
  managerData: any[] = [];
  employeeData: any[] = [];
  apiURL = environment.apiURL;
  rowData: any[] = [];
  rowDataR: any[] = [];
  selectedManager: any[] = [];
  selectedEmployee: any[] = [];
  selectedEmployeeList: any[] = [];
  closeResult = '';

  constructor(
    private spinner: NgxSpinnerService,
    private toastr: ToastrService,
    private cs: CoreService,
    private modalService: NgbModal,
    private fb: FormBuilder,
    private config: NgbDatepickerConfig,
    private router: Router
  ) {
    const current = new Date();
    config.minDate = {
      year: current.getFullYear(),
      month: current.getMonth() + 1,
      day: current.getDate(),
    };
    //config.maxDate = { year: 2099, month: 12, day: 31 };
    config.outsideDays = 'hidden';
  }

  ngOnInit(): void {
    this.spinner.show();
    if (!this.cs.getRole) {
      this.cs.obsGetUserInfo?.subscribe((data) => {
        this.getRole = data?.data?.userRole;
        this.getUserName = data?.data?.userName;
        this.user_id = data?.data?.user_id;
      });
    } else {
      this.getRole = this.cs.getRole;
      this.getUserName = this.cs.userName;
      this.user_id = this.cs.user_id;
    }

    // this.paginationPageSize = 10;
    this.frm = this.fb.group({
      managerName: [''],
      managerID: [''],
      empName: [''],
      empNumber: [''],
      reNumber: [''],
    });
    this.frmTran = this.fb.group({
      currentManager: [''],
      newManager: [''],
      eDate: [''],
    });

    let response = (localStorage.getItem("homeRetriveValue"));
    if (response != "false" || response != null) {
      const responses = JSON.parse(localStorage.getItem('homeSearchLS') || '{}');
      this.frm = this.fb.group({
        managerName: responses["managerName"],
        managerID: responses["managerID"],
        empName: responses["empName"],
        empNumber: [''],
        reNumber: [''],
      });

      if (this.frm.value.managerName != '') {
        this.btnDisableds = false;
      }
      if (this.frm.value.empName != '') {
        this.btnDisableds = false;
      }

    }

    setTimeout(() => {
      this.spinner.hide();
      const navigation_obj = {
        page: 'home'
      }
      localStorage.setItem("navigationLS", JSON.stringify(navigation_obj));
    }, 3000);
  }
  public defaultColDef: ColDef = {
    flex: 1,
    minWidth: 100,
  };

  openSearchDialogManager(val: any) {
    this.searchDialog = val;
    this.gridApiDialogM.setDatasource(this.dataSourceManager);
  }

  openSearchDialog(val: any) {
    this.searchDialog = val;
    this.gridApiDialog.setDatasource(this.dataSourceEmployee);
  }

  columnDefs: any = [
    {
      headerName: 'Employee ID',
      field: 'employee_id',
      width: 150,
      pinned: 'left',
      lockPinned: true,
      cellClass: 'lock-pinned',
      headerCheckboxSelection: true,
      headerCheckboxSelectionFilteredOnly: true,
      checkboxSelection: true,
      cellRenderer: this.createHyperLink.bind(this),
    },
    { headerName: 'Resource Number', field: 'resource_number', width: 175 },
    { headerName: 'Employee Name', field: 'employee_name', width: 200 },
    { headerName: 'Manager Name', field: 'manager_name', width: 200 },
    { headerName: 'Area', field: 'area_short_name', width: 100 },
    // { headerName: 'Location', field: 'location_code', width: 150 },
    { headerName: 'Team Type', field: 'team_type_name', width: 150 },
    { headerName: 'HR Status', field: 'hr_status', width: 150 },
    { headerName: 'FS Status', field: 'fs_status', width: 150 },
    { headerName: 'Admin Notes', field: 'admin_notes', width: 150 },
    { headerName: 'Pending Change Count', field: 'change_count', sortable: false, width: 215 },
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
    rowModelType: 'infinite',
  };

  createHyperLink(params: any): any {
    if (!params.data) {
      return;
    }
    let keyData = params.valueFormatted ? params.valueFormatted : params.value;

    const spanElement = document.createElement('span');
    spanElement.innerHTML = `<a class="idUnderline" href="javascript:void(0);"> ${keyData}</a>`;
    spanElement.addEventListener('click', ($event) => {
      $event.preventDefault();
      this.router.navigate(['/viewEmployee/' + btoa(keyData)]);
    });

    return spanElement;
  }

  onGridReadyDialogM(params: any) {
    this.gridApiDialogM = params.api;
    this.gridColumnApiDialogM = params.columnApi;
  }

  onGridReadyDialog(params: any) {
    this.gridApiDialog = params.api;
    this.gridColumnApiDialog = params.columnApi;
  }

  onSearchSubmit() {
    if (this.frm.value.managerName != '') {
      this.btnDisableds = false;
    }
    if (this.frm.value.empName != '') {
      this.btnDisableds = false;
    }

    this.lsHomeSearch();
  }

  lsHomeSearch() {
    const home_search_obj = {
      managerName: this.frm.value.managerName,
      empName: this.frm.value.empName,
      managerID: this.frm.value.managerID,
    }

    const navigation_obj = {
      page: 'home'
    }

    localStorage.setItem("homeSearchLS", JSON.stringify(home_search_obj));
    localStorage.setItem("navigationLS", JSON.stringify(navigation_obj));
    this.gridApi.setDatasource(this.dataSourceOnSearch);
  }

  onGridReady(params: any) {
    this.gridApi = params.api;
    this.gridColumnApi = params.columnApi;
    this.gridApi.setDatasource(this.dataSource);
  }

  dataSourceManager: IDatasource = {
    getRows: (params: IGetRowsParams) => {
      this.spinner.show();
      let sort = undefined;
      let colId = undefined;
      if (params.sortModel[0]) {
        sort = params.sortModel[0].sort;
        colId = params.sortModel[0].colId;
      }
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
          params.successCallback(
            response['data'].records,
            response['data'].total_items
          );
          this.gridApiDialogM.hideOverlay();
          if (response['data'].total_items <= 0) {
            this.gridApiDialogM.showNoRowsOverlay();
          }
        },
        error: (err: any) => {
          this.cs.handleError(err);
          this.spinner.hide();
        },
        complete: () => {
          this.spinner.hide();
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
    let requestURL = this.apiURL + url + query;
    console.log(requestURL);
    return this.cs.requestHttp('get', url + query);
  }

  dataSourceEmployee: IDatasource = {
    getRows: (params: IGetRowsParams) => {
      this.spinner.show();
      let sort = undefined;
      let colId = undefined;
      if (params.sortModel[0]) {
        sort = params.sortModel[0].sort;
        colId = params.sortModel[0].colId;
      }
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
          params.successCallback(
            response['data'].records,
            response['data'].total_items
          );
          this.gridApiDialog.hideOverlay();
          if (response['data'].total_items <= 0) {
            this.gridApiDialog.showNoRowsOverlay();
          }
        },
        error: (err: any) => {
          this.cs.handleError(err);
          this.spinner.hide();
        },
        complete: () => {
          this.spinner.hide();
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
    //{base_url}/v1/home/get_employee_list?page=1&per_page=10&order=asc&manager_id=141361&manager_name=Wolfe&q=Nielsen, Rob
    let url = 'api/home/get_employee_list?';
    let query = '';
    query += 'page=' + page + '&per_page=' + size;
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
        this.selectedManager[0].manager_name;
    }
    if (this.frm.value.empName) {
      query += '&q=' + this.frm.value.empName;
    }
    return this.cs.requestHttp('get', url + query);
  }

  //Dashboard
  dataSource: IDatasource = {
    getRows: (params: IGetRowsParams) => {
      this.spinner.show();
      let sort = undefined;
      let colId = undefined;
      if (params.sortModel[0]) {
        sort = params.sortModel[0].sort;
        colId = params.sortModel[0].colId;
      }
      let request: RequestWithFilterAndSort = {
        colId: colId,
        sort: sort,
        filterModel: params.filterModel,
        data: undefined,
      };
      setTimeout(() => {
        this.get_home_dashboard_data(
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
            this.cs.handleError(err);
            this.spinner.hide();
          },
          complete: () => {
            this.spinner.hide();
          },
        });
      }, 2000);
    },
  };

  get_home_dashboard_data(
    requestWithSortAndFilter: RequestWithFilterAndSort,
    page: number,
    size: number
  ) {
    page++;
    //{base_url}/v1/home/get?page=1&per_page=10&order=asc&manager_id=141361&manager_name=Wolfe&q=Nielsen, Rob
    let url = 'api/home/get?';
    let query = '';

    query += 'page=' + page + '&per_page=' + size;
    if (requestWithSortAndFilter.colId) {
      query +=
        '&order_by=' +
        requestWithSortAndFilter.colId +
        '&order=' +
        requestWithSortAndFilter.sort;
    }
    if (this.frm.value.managerName) {
      query +=
        '&manager_id=' +
        this.frm.value.managerID +
        '&manager_name=' +
        this.frm.value.managerName;
    }
    // if (this.selectedManager.length > 0) {
    //   query +=
    //     '&manager_id=' +
    //     this.selectedManager[0].manager_id +
    //     '&manager_name=' +
    //     this.selectedManager[0].manager_name;
    // }
    if (this.frm.value.empName) {
      query += '&q=' + this.frm.value.empName;
    }
    if (this.getRole == 'MANAGER') {
      query += '&manager_id=' +
        this.user_id;
    }
    let requestURL = url + query;
    console.log(requestURL);
    return this.cs.requestHttp('get', requestURL);
  }

  //on Serach
  dataSourceOnSearch: IDatasource = {
    getRows: (params: IGetRowsParams) => {
      this.spinner.show();
      let sort = undefined;
      let colId = undefined;
      if (params.sortModel[0]) {
        sort = params.sortModel[0].sort;
        colId = params.sortModel[0].colId;
      }
      let request: RequestWithFilterAndSort = {
        colId: colId,
        sort: sort,
        filterModel: params.filterModel,
        data: undefined,
      };
      this.on_search_btn(
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
          this.cs.handleError(err);
          this.spinner.hide();
        },
        complete: () => {
          this.spinner.hide();
        },
      });
    },
  };

  on_search_btn(
    requestWithSortAndFilter: RequestWithFilterAndSort,
    page: number,
    size: number
  ) {
    page++;
    let url = 'api/home/get?';
    let query = '';
    query += 'page=' + page + '&per_page=' + size;
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
        this.selectedManager[0].manager_name;
    }
    if (this.frm.value.empName) {
      query += '&q=' + this.frm.value.empName;
    }

    let requestURL = url + query;
    console.log(requestURL);
    return this.cs.requestHttp('get', requestURL);
  }


  onPageSizeChanged(event: any) {
    this.gridApi.paginationSetPageSize(Number(event.target.value));
  }

  onSubmitTransfer() {
    if (this.frmTran.valid) {
      this.spinner.show();
      let date = this.frmTran.value.eDate;
      const a = new Date(date.year + '-' + date.month + '-' + date.day);
      let month = ('0' + (a.getMonth() + 1)).slice(-2);
      let day = ('0' + (date.day)).slice(-2);

      let setData = this.selectedEmployeeList.map(
        (employee: any) => employee.employee_id
      );

      let obj = {
        employee_id: setData,
        manager_id: this.frmTran.value.newManager,
        change_effective_date: date.year + '-' + month + '-' + day,
      };
      let url = 'api/home/manager_transfer';
      this.cs.requestHttp('POST', url, obj, false).subscribe({
        next: (response: any) => {
          this.toastr.success(response.data.message);
          this.modalService.dismissAll();
          this.frmTran.reset();
          this.gridApi.setDatasource(this.dataSource);
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

  onSubmit() {
    const selectedRows = this.gridApiDialog.getSelectedRows();
    if (this.searchDialog == 1) {
    } else {
      this.searchDialog = selectedRows.length === 1 ? selectedRows[0].name : '';
    }
  }

  clearData() {
    this.frm.reset();
    while (this.selectedManager.length) {
      this.selectedManager.pop();
    }
    if (
      localStorage.getItem("homeSearchLS")
    ) {
      localStorage.removeItem("homeSearchLS");
    }
    this.btnDisableds = true;
    this.gridApi.setDatasource(this.dataSource);
  }

  //allow only one record
  onBtTransfer(content: any) {
    if (this.selectedEmployeeList.length > 0) {
      const currentManager = this.selectedEmployeeList[0].manager_name;
      const selectedrecords = this.selectedEmployeeList.filter(
        (el: any) =>
          el.manager_id == this.selectedEmployeeList[0].manager_id &&
          el.area_id == this.selectedEmployeeList[0].area_id
      );
      if (this.selectedEmployeeList.length == selectedrecords.length) {
        this.frmTran.controls['currentManager'].patchValue(currentManager);
        this.get_dropdown_managers();
        this.open(content);
      } else {
        this.toastr.error(
          'Please select employee who has same Manager and Area',
          ''
        ); // match region condition
      }
    } else {
      this.toastr.error('Please select at least one employee record', '');
    }
    this.btnDisableds = true;
  }

  open(content: any) {
    this.modalService
      .open(content, { ariaLabelledBy: 'modal-basic-title' })
      .result.then(
        (result) => {
          this.closeResult = `Closed with: ${result}`;
        },
        (reason) => {
          this.closeResult = `Dismissed ${this.getDismissReason(reason)}`;
        }
      );
  }

  openChanges(content: any) {
    this.modalService
      .open(content, { size: 'lg', ariaLabelledBy: 'modal-basic-title' })
      .result.then(
        (result) => {
          this.closeResult = `Closed with: ${result}`;
        },
        (reason) => {
          this.closeResult = `Dismissed ${this.getDismissReason(reason)}`;
        }
      );
  }
  private getDismissReason(reason: any): string {
    if (reason === ModalDismissReasons.ESC) {
      return 'by pressing ESC';
    } else if (reason === ModalDismissReasons.BACKDROP_CLICK) {
      return 'by clicking on a backdrop';
    } else {
      return `with: ${reason}`;
    }
  }

  onBtExport() {
    this.spinner.show();
    let empNames = "";
    let managers = "";
    if (this.frm.value.empName) {
      empNames = this.frm.value.empName;
    }
    if (this.frm.value.managerName) {
      managers = this.frm.value.managerName;
    }
    let url = '/api/home/bulk_export?type=Home_Screen';
    let obj = {
      msg: 'Home Screen',
      type: 'export',
      attribute1: managers,
      attribute2: empNames
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


  onBtExportBulk() {
    this.spinner.show();
    let url = '/api/home/bulk_export?type=Home_Screen';
    let obj = {
      msg: 'Home Screen',
      type: 'home',
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

  @ViewChild('closebutton') closebutton!: {
    nativeElement: { click: () => void };
  };
  @ViewChild('closebutton1') closebuttonm!: {
    nativeElement: { click: () => void };
  };

  onSelectionChangedDialogM(event: SelectionChangedEvent) {
    const selectedRows = this.gridApiDialogM.getSelectedRows();
    if (selectedRows.length === 1) {
      this.clearData();
      this.selectedManager = selectedRows;
      if (selectedRows[0].manager_name.length > 0) {
        this.btnDisableds = false;
      }
      this.frm.controls['managerName'].setValue(selectedRows[0].manager_name);
      this.frm.controls['managerID'].setValue(selectedRows[0].manager_id);
      this.lsHomeSearch();
      this.closebuttonm.nativeElement.click();
    }
  }

  onSelectionChangedDialog(event: SelectionChangedEvent) {
    const selectedRows = this.gridApiDialog.getSelectedRows();
    if (selectedRows.length === 1) {
      this.selectedEmployee = selectedRows;
      if (selectedRows[0].employee_name.length > 0) {
        this.btnDisableds = false;
      }
      this.frm.controls['empName'].setValue(selectedRows[0].employee_name);
      this.lsHomeSearch();
      this.closebutton.nativeElement.click();
    }
  }

  onSelectionChanged(event: SelectionChangedEvent) {
    this.selectedEmployeeList = this.gridApi.getSelectedRows();
    if (this.selectedEmployeeList.length > 0) {
      this.btnDisabled = false;
    } else {
      this.btnDisabled = true;
    }
  }

  get_dropdown_managers() {
    this.spinner.show();
    let url;

    // if (this.getRole == 'ADMIN') {
    // url = '/api/home/get_manager_list?is_export_all=Y';
    // } else {
    // let area_short_name = this.selectedEmployeeList[0].area_short_name;
    // url = '/api/config/common/area-fom?area=' + area_short_name;
    // }
    url = '/api/home/get_manager_list?is_export_all=Y';
    this.cs.requestHttp('get', url).subscribe({
      next: (response: any) => {
        //this.rowDataR = response['data'].records;
        this.selectItems = response['data'].records;
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

  columnDefsR: ColDef[] = [
    { headerName: 'Change Id', field: 'change_id', width: 110 },
    { headerName: 'Effective Date', field: 'change_effective_date' },
    { headerName: 'Status', field: 'change_status', width: 115 },
    { headerName: 'Change Notes', field: 'change_note', width: 340 },
  ];
  public selectControl = new FormControl();
  selectItems: any[] = [];
  gridApiChangeR: any;
  gridColumnApiChangeR: any;

  //allow only one record
  onBtRequestChanges(content: any) {
    this.encoded_employee_id = btoa(this.selectedEmployeeList[0].employee_id);
    this.rc_employee_name = this.selectedEmployeeList[0].employee_name;
    this.rc_hr_status = this.selectedEmployeeList[0].hr_status;
    if (this.selectedEmployeeList.length == 1) {
      //this.currentManager = this.selectedEmployeeList[0].manager_name;
      this.openChanges(content);
    } else {
      this.selectedEmployeeList.length > 1
        ? this.toastr.error('Please select only one employee record', '')
        : this.toastr.error('Please select at least one employee record', '');
    }
    this.btnDisableds = true;
  }
  onGridReadyChangeR(params: any) {
    this.gridApiChangeR = params.api;
    this.gridColumnApiChangeR = params.columnApi;
    this.gridApiChangeR.setDatasource(this.dataSourceChangeRequest);
  }

  dataSourceChangeRequest: IDatasource = {
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
      this.getRequestChanges(
        request,
        this.gridApiChangeR.paginationGetCurrentPage(),
        this.gridApiChangeR.paginationGetPageSize()
      ).subscribe({
        next: (response: any) => {
          this.spinner.hide();
          params.successCallback(
            response['data'].records,
            response['data'].records.length
          );
          this.gridApiChangeR.hideOverlay();
          if (response['data'].records.length <= 0) {
            this.gridApiChangeR.showNoRowsOverlay();
          }
        },
        error: (err: any) => {
          this.spinner.hide();
          this.cs.handleError(err);
        },
      });
    },
  };
  getRequestChanges(
    requestWithSortAndFilter: RequestWithFilterAndSort,
    page: number,
    size: number
  ) {
    this.spinner.show();
    let url =
      'api/home/get_change_request?employee_id=' +
      this.selectedEmployeeList[0].employee_id;
    //let url = "home/request_changes.json";
    return this.cs.requestHttp('get', url);
  }

  onSelectionChangedChangeR(event: SelectionChangedEvent) {
    const selectedRows = this.gridApiChangeR.getSelectedRows();
    if (selectedRows.length == 1) {
      this.modalService.dismissAll();
      this.router.navigate([
        '/viewChanges/' +
        btoa(selectedRows[0].change_id) +
        '/' +
        btoa(this.selectedEmployeeList[0].employee_id),
      ]);
    }
  }

  onTransferCancel() {
    this.modalService.dismissAll();
    this.frmTran.reset();
  }

  onBtAddEmployee() {
    this.router.navigate(['addEmployee'])
  }

  ngOnDestroy(): void {
    this.modalService.dismissAll();
    this.config.minDate != null;
    //  this.subscribeCls && this.subscribeCls.unsubscribe();
  }
}
