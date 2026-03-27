import { Component } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { GridOptions, IDatasource, IGetRowsParams } from 'ag-grid-community';
import { NgxSpinnerService } from 'ngx-spinner';
import { Subscription } from 'rxjs';
import { RequestWithFilterAndSort } from 'src/app/common/types';
import { ToastrService } from 'ngx-toastr';
import { ngxCsv } from 'ngx-csv';
import { CoreService } from 'src/app/service/core.service';
import { Router } from '@angular/router';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'app-views',
  templateUrl: './views.component.html',
  styleUrls: ['./views.component.css'],
})
export class ViewsComponent {
  defaultPageSize = environment.defaultPageSize;
  defaultDialogSize = environment.defaultDialogSize;
  subscribeCls!: Subscription;
  private gridApi: any;
  private gridColumnApi: any;
  retriveView: boolean = false;
  frm!: FormGroup;
  get f() {
    return this.frm.controls;
  }
  isSearchDisable: boolean = true;
  tab: any;

  constructor(
    private cs: CoreService,
    private fb: FormBuilder,
    private spinner: NgxSpinnerService,
    private toastr: ToastrService,
    private router: Router
  ) { }
  ngOnInit(): void {
    let response = (localStorage.getItem("retriveView"));
    if (response == "false" || response == null) {
      this.frm = this.fb.group({
        empName: [''],
        empStatus: [''],
        fsStatus: [''],
        jobType: [''],

      });
      this.frm.valueChanges.subscribe((v) => {
        this.isSearchDisable = this.frm.controls['empName'].value ? false : true;
        this.isSearchDisable = this.frm.controls['empStatus'].value ? false : true;
        this.isSearchDisable = this.frm.controls['fsStatus'].value ? false : true;
        this.isSearchDisable = this.frm.controls['jobType'].value ? false : true;
      });
    } else {
      const responseTab = JSON.parse(localStorage.getItem('tabView') || '{}');
      if (Object.keys(responseTab).length > 0) {
        const responses = JSON.parse(localStorage.getItem('filteredlistView') || '{}');
        this.frm = this.fb.group({
          empName: responses["empName"],
          empStatus: responses["empStatus"],
          fsStatus: responses["fsStatus"],
          jobType: responses["jobType"],
        });
        this.frm.valueChanges.subscribe((v) => {
          this.isSearchDisable = responses["empName"] ? true : false;
          this.isSearchDisable = responses["empStatus"] ? true : false
          this.isSearchDisable = responses["fsStatus"] ? true : false
          this.isSearchDisable = responses["jobType"] ? true : false
        });
      } else {
        this.frm = this.fb.group({
          empName: [''],
          empStatus: [''],
          fsStatus: [''],
          jobType: [''],
        });
        this.frm.valueChanges.subscribe((v) => {
          this.isSearchDisable = this.frm.controls['empName'].value ? false : true;
          this.isSearchDisable = this.frm.controls['empStatus'].value ? false : true;
          this.isSearchDisable = this.frm.controls['fsStatus'].value ? false : true;
          this.isSearchDisable = this.frm.controls['jobType'].value ? false : true;
        });
      }
    }
    const navigation_obj = {
      page: 'view'
    }
    localStorage.setItem("navigationLS", JSON.stringify(navigation_obj));
  }
  empStatus = this.cs.selectActive;
  fsStatusDropDown = this.cs.fsStatus;
  job_types = [
    { optionId: 'FIELD SUPT', optionTitle: 'FIELD SUPT' },
    { optionId: 'FSM', optionTitle: 'FSM' },
    { optionId: 'TAS', optionTitle: 'TAS' },
    { optionId: 'TECH', optionTitle: 'TECH' },
    { optionId: 'DIR', optionTitle: 'DIR' },
    { optionId: 'OPS', optionTitle: 'OPS' },
    { optionId: 'REGION DIR', optionTitle: 'REGION DIR' },
    { optionId: 'TSE', optionTitle: 'TSE' },
  ];
  tabs = [
    { id: 1, value: 'New Hires' },
    { id: 2, value: 'Recent Terms' },
    { id: 3, value: 'On LOA' },
    { id: 4, value: 'Hierarchy Mismatches' },
    { id: 5, value: 'Job Mismatches' },
    { id: 6, value: 'Manager Mismatches' },
    { id: 7, value: 'All Mismatches' },
    { id: 8, value: 'Managers not set to self' },
    { id: 9, value: 'Records not completed' },
    { id: 10, value: 'Admin Review' },
  ];

  selectedTab(e: any) {
    this.spinner.show();
    const viewTabLS = localStorage.getItem('viewTabLS');
    const responseTab = JSON.parse(localStorage.getItem('tabView') || '{}');
    // if (Object.keys(responseTab).length > 0) {
    if (viewTabLS == 'true' && Object.keys(responseTab).length > 0) {
      this.tab = responseTab;
      setTimeout(() => {
        this.gridApi.setDatasource(this.dataSource);
      }, 1000);
    }
    else {
      localStorage.removeItem("tabView");
      localStorage.removeItem("filteredlistView");
      localStorage.removeItem("retriveView");
      this.frm = this.fb.group({
        empName: [''],
        empStatus: [''],
        fsStatus: [''],
        jobType: [''],
      });
      this.frm.valueChanges.subscribe((v) => {
        this.isSearchDisable = this.frm.controls['empName'].value ? false : true;
        this.isSearchDisable = this.frm.controls['empStatus'].value ? false : true;
        this.isSearchDisable = this.frm.controls['fsStatus'].value ? false : true;
        this.isSearchDisable = this.frm.controls['jobType'].value ? false : true;
      });
      this.tab = e;
      const tabObj = {
        id: this.tab.id,
        value: this.tab.value
      }
      localStorage.setItem("tabView", JSON.stringify(tabObj));
      setTimeout(() => {
        this.gridApi.setDatasource(this.dataSource);
      }, 500);
    }
    this.spinner.hide();
  }
  onSearchSubmit() {
    this.spinner.show();
    const obj = {
      empName: this.frm.value.empName,
      empStatus: this.frm.value.empStatus,
      fsStatus: this.frm.value.fsStatus,
      jobType: this.frm.value.jobType
    }
    localStorage.setItem("filteredlistView", JSON.stringify(obj));
    const navigation_obj = {
      page: 'view'
    }
    localStorage.setItem("navigationLS", JSON.stringify(navigation_obj));
    this.retriveView = false;
    localStorage.setItem("retriveView", `${this.retriveView}`);
    setTimeout(() => {
      this.gridApi.setDatasource(this.dataSource);
    }, 500);
    this.spinner.hide();
  }
  clearData() {
    this.frm.reset();
    localStorage.removeItem("filteredlistView");
    localStorage.removeItem("retriveView");
    localStorage.removeItem("tabView");
    localStorage.removeItem("viewTabLS");
    this.gridApi.setDatasource(this.dataSource);
  }

  columnDefs: any = [
    {
      headerName: 'Employee ID',
      field: 'employee_id',
      width: 150,
      pinned: 'left',
      lockPinned: true,
      cellClass: 'lock-pinned',
      //cellRenderer: function (params: any) {
      //  let keyData = params.valueFormatted
      //    ? params.valueFormatted
      //    : params.value;
      //  let newLink = `<a class="idUnderline" href="viewEmployee/${btoa(
      //    keyData
      //  )}">${keyData}</a>`;
      //  return newLink;
      //},
      cellRenderer: this.createHyperLink.bind(this),
    },
    { headerName: 'Resource Number', field: 'resource_number' },
    { headerName: 'Employee Name', field: 'employee_name' },
    { headerName: 'Manager Name', field: 'manager_name' },
    { headerName: 'Team Type', field: 'team_type_name' },
    { headerName: 'Area', field: 'area_short_name' },
    { headerName: 'Region', field: 'region_name' },
    { headerName: 'Admin Notes', field: 'admin_notes' },
    { headerName: 'HR Status', field: 'hr_status' },
    { headerName: 'FS Status', field: 'fs_status' },
  ];

  rowData: any[] = [];

  gridOptions: GridOptions = {
    defaultColDef: {
      sortable: false, //filter:true,
      unSortIcon: false,
      resizable: true,
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
      // const tabObj = {
      //   id: this.tab.id,
      //   value: this.tab.value
      // }
      // localStorage.setItem("tabView", JSON.stringify(tabObj));
      $event.preventDefault();
      this.router.navigate(['/viewEmployee/' + btoa(keyData)]);
    });

    return spanElement;
  }

  onGridReady(params: any) {
    console.log('onGridReady');
    this.gridApi = params.api;
    this.gridColumnApi = params.columnApi;
    // this.gridApi.setDatasource(this.dataSource);
  }

  dataSource: IDatasource = {
    getRows: (params: IGetRowsParams) => {
      this.spinner.show();
      let sort = undefined;
      let colId = undefined;
      this.spinner.show();
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
      this.subscribeCls = this.getEmployee(
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

  getEmployee(
    requestWithSortAndFilter: RequestWithFilterAndSort,
    page: number,
    size: number
  ) {
    let response = (localStorage.getItem("retriveView"));
    if (response == "false" || response == null) {
      page++;
      let query = 'page=' + page + '&per_page=' + size;
      if (requestWithSortAndFilter.colId) {
        query +=
          '&order_by=' +
          requestWithSortAndFilter.colId +
          '&order=' +
          requestWithSortAndFilter.sort;
      }
      if (this.frm.value.empName) {
        query += '&q=' + this.frm.value.empName;
      }
      if (this.frm.value.empStatus) {
        query += '&status=' + this.frm.value.empStatus;
      }
      if (this.frm.value.fsStatus) {
        query += '&fs_status=' + this.frm.value.fsStatus;
      }
      if (this.frm.value.jobType) {
        query += '&job_type=' + this.frm.value.jobType;
      }
      let url;
      switch (this.tab.id) {
        case 1: {
          //
          url = 'api/view/get_new_hire_list?';
          // url = "viewemployees/new_hire.json"
          this.columnDefs = [
            {
              headerName: 'Employee ID',
              field: 'employee_id',
              width: 150,
              pinned: 'left',
              lockPinned: true,
              cellClass: 'lock-pinned',
              cellRenderer: this.createHyperLink.bind(this),
            },
            { headerName: 'Resource Number', field: 'resource_number' },
            { headerName: 'Employee Name', field: 'employee_name' },
            { headerName: 'Manager Name', field: 'manager_name' },
            { headerName: 'Team Type', field: 'team_type_name' },
            { headerName: 'Area', field: 'area_short_name' },
            { headerName: 'Region', field: 'region_name' },
            { headerName: 'Admin Notes', field: 'admin_notes' },
            { headerName: 'HR Status', field: 'hr_status' },
            { headerName: 'FS Status', field: 'fs_status' },
          ];
          break;
        }
        case 2: {
          url = 'api/view/get_recent_term_list?';
          //url = "viewemployees/new_hire.json"
          this.columnDefs = [
            {
              headerName: 'Employee ID',
              field: 'employee_id',
              width: 150,
              pinned: 'left',
              lockPinned: true,
              cellClass: 'lock-pinned',
              cellRenderer: this.createHyperLink.bind(this),
            },
            { headerName: 'Resource Number', field: 'resource_number' },
            { headerName: 'Employee Name', field: 'employee_name' },
            { headerName: 'Manager Name', field: 'manager_name' },
            { headerName: 'Team Type', field: 'team_type_name' },
            { headerName: 'Area', field: 'area_short_name' },
            { headerName: 'Region', field: 'region_name' },
            { headerName: 'Admin Notes', field: 'admin_notes' },
            { headerName: 'HR Status', field: 'hr_status' },
            { headerName: 'FS Status', field: 'fs_status' },
          ];
          break;
        }
        case 3: {
          url = 'api/view/get_loa_list?';
          //url = "viewemployees/new_hire.json"
          this.columnDefs = [
            {
              headerName: 'Employee ID',
              field: 'employee_id',
              width: 150,
              pinned: 'left',
              lockPinned: true,
              cellClass: 'lock-pinned',
              cellRenderer: this.createHyperLink.bind(this),
            },
            { headerName: 'Resource Number', field: 'resource_number' },
            { headerName: 'Employee Name', field: 'employee_name' },
            { headerName: 'Manager Name', field: 'manager_name' },
            { headerName: 'Team Type', field: 'team_type_name' },
            { headerName: 'Area', field: 'area_short_name' },
            { headerName: 'Region', field: 'region_name' },
            { headerName: 'Admin Notes', field: 'admin_notes' },
            { headerName: 'HR Status', field: 'hr_status' },
            { headerName: 'FS Status', field: 'fs_status' },
          ];
          break;
        }
        case 4: {
          url = 'api/view/get_hierarchy_mismatches_list?';
          //url = "viewemployees/new_hire.json"
          this.columnDefs = [
            {
              headerName: 'Employee ID',
              field: 'employee_id',
              width: 150,
              pinned: 'left',
              lockPinned: true,
              cellClass: 'lock-pinned',
              cellRenderer: this.createHyperLink.bind(this),
            },
            { headerName: 'Resource Number', field: 'resource_number' },
            { headerName: 'Employee Name', field: 'employee_name' },
            { headerName: 'Manager Name', field: 'manager_name' },
            { headerName: 'Area', field: 'area_short_name' },
            { headerName: 'Manager Area', field: 'system_area_short_name' },
            { headerName: 'Region', field: 'region_name' },
            { headerName: 'Manager Region', field: 'system_region_name' },
            { headerName: 'Admin Notes', field: 'admin_notes' },
            { headerName: 'HR Status', field: 'hr_status' },
            { headerName: 'FS Status', field: 'fs_status' },
          ];
          break;
        }
        case 5: {
          url = 'api/view/get_job_mismatches_list?';
          //url = "viewemployees/new_hire.json"
          this.columnDefs = [
            {
              headerName: 'Employee ID',
              field: 'employee_id',
              width: 150,
              pinned: 'left',
              lockPinned: true,
              cellClass: 'lock-pinned',
              cellRenderer: this.createHyperLink.bind(this),
            },
            { headerName: 'Resource Number', field: 'resource_number' },
            { headerName: 'Employee Name', field: 'employee_name' },
            { headerName: 'Manager Name', field: 'manager_name' },
            { headerName: 'Job ADP Code', field: 'job_adp' },
            { headerName: 'System Job ADP Code', field: 'system_job_adp' },
            { headerName: 'Admin Notes', field: 'admin_notes' },
            { headerName: 'HR Status', field: 'hr_status' },
            { headerName: 'FS Status', field: 'fs_status' },
          ];
          break;
        }
        case 6: {
          url = 'api/view/get_manager_mismatches_list?';
          //url = "viewemployees/new_hire.json"
          this.columnDefs = [
            {
              headerName: 'Employee ID',
              field: 'employee_id',
              width: 150,
              pinned: 'left',
              lockPinned: true,
              cellClass: 'lock-pinned',
              cellRenderer: this.createHyperLink.bind(this),
            },
            { headerName: 'Resource Number', field: 'resource_number' },
            { headerName: 'Employee Name', field: 'employee_name' },
            { headerName: 'Manager Name', field: 'manager_name' },
            { headerName: 'System Manager Name', field: 'system_manager_name' },
            { headerName: 'Admin Notes', field: 'admin_notes' },
            { headerName: 'HR Status', field: 'hr_status' },
            { headerName: 'FS Status', field: 'fs_status' },
          ];
          break;
        }
        case 7: {
          url = 'api/view/get_all_mismatches_list?';
          //url = "viewemployees/new_hire.json"
          this.columnDefs = [
            {
              headerName: 'Employee ID',
              field: 'employee_id',
              width: 150,
              pinned: 'left',
              lockPinned: true,
              cellClass: 'lock-pinned',
              cellRenderer: this.createHyperLink.bind(this),
            },
            { headerName: 'Resource Number', field: 'resource_number' },
            { headerName: 'Employee Name', field: 'employee_name' },
            { headerName: 'Manager Name', field: 'manager_name' },
            { headerName: 'Team Type', field: 'team_type_name' },
            { headerName: 'Area', field: 'area_short_name' },
            { headerName: 'Region', field: 'region_name' },
            { headerName: 'Admin Notes', field: 'admin_notes' },
            { headerName: 'HR Status', field: 'hr_status' },
            { headerName: 'FS Status', field: 'fs_status' },
          ];
          break;
        }
        case 8: {
          url = 'api/view/get_managers_not_self_list?';
          //url = "viewemployees/new_hire.json"
          this.columnDefs = [
            {
              headerName: 'Employee ID',
              field: 'employee_id',
              width: 150,
              pinned: 'left',
              lockPinned: true,
              cellClass: 'lock-pinned',
              cellRenderer: this.createHyperLink.bind(this),
            },
            { headerName: 'Resource Number', field: 'resource_number' },
            { headerName: 'Employee Name', field: 'employee_name' },
            { headerName: 'Manager Name', field: 'manager_name' },
            { headerName: 'Team Type', field: 'team_type_name' },
            { headerName: 'Area', field: 'area_short_name' },
            { headerName: 'Region', field: 'region_name' },
            { headerName: 'Admin Notes', field: 'admin_notes' },
            { headerName: 'HR Status', field: 'hr_status' },
            { headerName: 'FS Status', field: 'fs_status' },
          ];
          break;
        }
        case 9: {
          url = 'api/view/get_record_not_complete_list?';
          //url = "viewemployees/new_hire.json"
          this.columnDefs = [
            {
              headerName: 'Employee ID',
              field: 'employee_id',
              width: 150,
              pinned: 'left',
              lockPinned: true,
              cellClass: 'lock-pinned',
              cellRenderer: this.createHyperLink.bind(this),
            },
            { headerName: 'Resource Number', field: 'resource_number' },
            { headerName: 'Employee Name', field: 'employee_name' },
            { headerName: 'Manager Name', field: 'manager_name' },
            { headerName: 'Team Type', field: 'team_type_name' },
            { headerName: 'Area', field: 'area_short_name' },
            { headerName: 'Region', field: 'region_name' },
            { headerName: 'Admin Notes', field: 'admin_notes' },
            { headerName: 'HR Status', field: 'hr_status' },
            { headerName: 'FS Status', field: 'fs_status' },
          ];
          break;
        }
        case 10: {
          url = 'api/view/get_admin_review_list?';
          //url = "viewemployees/new_hire.json"
          this.columnDefs = [
            {
              headerName: 'Employee ID',
              field: 'employee_id',
              width: 150,
              pinned: 'left',
              lockPinned: true,
              cellClass: 'lock-pinned',
              cellRenderer: this.createHyperLink.bind(this),
            },
            { headerName: 'Resource Number', field: 'resource_number' },
            { headerName: 'Employee Name', field: 'employee_name' },
            { headerName: 'Manager Name', field: 'manager_name' },
            { headerName: 'Team Type', field: 'team_type_name' },
            { headerName: 'Area', field: 'area_short_name' },
            { headerName: 'Region', field: 'region_name' },
            { headerName: 'Admin Notes', field: 'admin_notes' },
            { headerName: 'HR Status', field: 'hr_status' },
            { headerName: 'FS Status', field: 'fs_status' },
          ];
          break;
        }

        default: {
          url = 'api/view/get_loa_list?';
          //url = "viewemployees/new_hire.json"
          this.columnDefs = [
            {
              headerName: 'Employee ID',
              field: 'employee_id',
              width: 150,
              pinned: 'left',
              lockPinned: true,
              cellClass: 'lock-pinned',
              cellRenderer: this.createHyperLink.bind(this),
            },
            { headerName: 'Resource Number', field: 'resource_number' },
            { headerName: 'Employee Name', field: 'employee_name' },
            { headerName: 'Manager Name', field: 'manager_name' },
            { headerName: 'Team Type', field: 'team_type_name' },
            { headerName: 'Area', field: 'area_short_name' },
            { headerName: 'Region', field: 'region_name' },
            { headerName: 'Admin Notes', field: 'admin_notes' },
            { headerName: 'HR Status', field: 'hr_status' },
            { headerName: 'FS Status', field: 'fs_status' },
          ];
          break;
        }
      }
      let reqURL = url + query;
      console.log(reqURL);
      return this.cs.requestHttp('get', reqURL);

    }
    else {
      const tabViews = JSON.parse(localStorage.getItem('tabView') || '{}');
      const responses = JSON.parse(localStorage.getItem('filteredlistView') || '{}');
      page++;
      let query = 'page=' + page + '&per_page=' + size;
      if (requestWithSortAndFilter.colId) {
        query +=
          '&order_by=' +
          requestWithSortAndFilter.colId +
          '&order=' +
          requestWithSortAndFilter.sort;
      }
      if (responses["empName"]) {
        query += '&q=' + responses["empName"];
      }
      if (responses["empStatus"]) {
        query += '&status=' + responses["empStatus"];
      }
      if (responses["fsStatus"]) {
        query += '&fs_status=' + responses["fsStatus"];
      }
      if (responses["jobType"]) {
        query += '&job_type=' + responses["jobType"];
      }
      let url;
      switch (tabViews["id"]) {
        case 1: {
          url = 'api/view/get_new_hire_list?';
          //url = "../../assets/json/views/new_hire1.json"
          this.columnDefs = [
            {
              headerName: 'Employee ID',
              field: 'employee_id',
              width: 150,
              pinned: 'left',
              lockPinned: true,
              cellClass: 'lock-pinned',
              cellRenderer: this.createHyperLink.bind(this),
            },
            { headerName: 'Resource Number', field: 'resource_number' },
            { headerName: 'Employee Name', field: 'employee_name' },
            { headerName: 'Manager Name', field: 'manager_name' },
            { headerName: 'Team Type', field: 'team_type_name' },
            { headerName: 'Area', field: 'area_short_name' },
            { headerName: 'Region', field: 'region_name' },
            { headerName: 'Admin Notes', field: 'admin_notes' },
            { headerName: 'HR Status', field: 'hr_status' },
            { headerName: 'FS Status', field: 'fs_status' },
          ];
          break;
        }
        case 2: {
          url = 'api/view/get_recent_term_list?';
          //url = "viewemployees/new_hire.json"
          this.columnDefs = [
            {
              headerName: 'Employee ID',
              field: 'employee_id',
              width: 150,
              pinned: 'left',
              lockPinned: true,
              cellClass: 'lock-pinned',
              cellRenderer: this.createHyperLink.bind(this),
            },
            { headerName: 'Resource Number', field: 'resource_number' },
            { headerName: 'Employee Name', field: 'employee_name' },
            { headerName: 'Manager Name', field: 'manager_name' },
            { headerName: 'Team Type', field: 'team_type_name' },
            { headerName: 'Area', field: 'area_short_name' },
            { headerName: 'Region', field: 'region_name' },
            { headerName: 'Admin Notes', field: 'admin_notes' },
            { headerName: 'HR Status', field: 'hr_status' },
            { headerName: 'FS Status', field: 'fs_status' },
          ];
          break;
        }
        case 3: {
          url = 'api/view/get_loa_list?';
          //url = "viewemployees/new_hire.json"
          this.columnDefs = [
            {
              headerName: 'Employee ID',
              field: 'employee_id',
              width: 150,
              pinned: 'left',
              lockPinned: true,
              cellClass: 'lock-pinned',
              cellRenderer: this.createHyperLink.bind(this),
            },
            { headerName: 'Resource Number', field: 'resource_number' },
            { headerName: 'Employee Name', field: 'employee_name' },
            { headerName: 'Manager Name', field: 'manager_name' },
            { headerName: 'Team Type', field: 'team_type_name' },
            { headerName: 'Area', field: 'area_short_name' },
            { headerName: 'Region', field: 'region_name' },
            { headerName: 'Admin Notes', field: 'admin_notes' },
            { headerName: 'HR Status', field: 'hr_status' },
            { headerName: 'FS Status', field: 'fs_status' },
          ];
          break;
        }
        case 4: {
          url = 'api/view/get_hierarchy_mismatches_list?';
          //url = "../../assets/json/views/get_hierarchy_mismatches_list1.json"
          this.columnDefs = [
            {
              headerName: 'Employee ID',
              field: 'employee_id',
              width: 150,
              pinned: 'left',
              lockPinned: true,
              cellClass: 'lock-pinned',
              cellRenderer: this.createHyperLink.bind(this),
            },
            { headerName: 'Resource Number', field: 'resource_number' },
            { headerName: 'Employee Name', field: 'employee_name' },
            { headerName: 'Manager Name', field: 'manager_name' },
            { headerName: 'Area', field: 'area_short_name' },
            { headerName: 'System Area', field: 'system_area_short_name' },
            { headerName: 'Region', field: 'region_name' },
            { headerName: 'System Region', field: 'system_region_name' },
            { headerName: 'Admin Notes', field: 'admin_notes' },
            { headerName: 'HR Status', field: 'hr_status' },
            { headerName: 'FS Status', field: 'fs_status' },
          ];
          break;
        }
        case 5: {
          url = 'api/view/get_job_mismatches_list?';
          //url = "../../assets/json/views/Job_mismatch.json"
          this.columnDefs = [
            {
              headerName: 'Employee ID',
              field: 'employee_id',
              width: 150,
              pinned: 'left',
              lockPinned: true,
              cellClass: 'lock-pinned',
              cellRenderer: this.createHyperLink.bind(this),
            },
            { headerName: 'Resource Number', field: 'resource_number' },
            { headerName: 'Employee Name', field: 'employee_name' },
            { headerName: 'Manager Name', field: 'manager_name' },
            { headerName: 'Job ADP Code', field: 'job_adp' },
            { headerName: 'System Job ADP Code', field: 'system_job_adp' },
            { headerName: 'Admin Notes', field: 'admin_notes' },
            { headerName: 'HR Status', field: 'hr_status' },
            { headerName: 'FS Status', field: 'fs_status' },
          ];
          break;
        }
        case 6: {
          url = 'api/view/get_manager_mismatches_list?';
          //url = "viewemployees/new_hire.json"
          this.columnDefs = [
            {
              headerName: 'Employee ID',
              field: 'employee_id',
              width: 150,
              pinned: 'left',
              lockPinned: true,
              cellClass: 'lock-pinned',
              cellRenderer: this.createHyperLink.bind(this),
            },
            { headerName: 'Resource Number', field: 'resource_number' },
            { headerName: 'Employee Name', field: 'employee_name' },
            { headerName: 'Manager Name', field: 'manager_name' },
            { headerName: 'System Manager Name', field: 'system_manager_name' },
            { headerName: 'Admin Notes', field: 'admin_notes' },
            { headerName: 'HR Status', field: 'hr_status' },
            { headerName: 'FS Status', field: 'fs_status' },
          ];
          break;
        }
        case 7: {
          url = 'api/view/get_all_mismatches_list?';
          //url = "viewemployees/new_hire.json"
          this.columnDefs = [
            {
              headerName: 'Employee ID',
              field: 'employee_id',
              width: 150,
              pinned: 'left',
              lockPinned: true,
              cellClass: 'lock-pinned',
              cellRenderer: this.createHyperLink.bind(this),
            },
            { headerName: 'Resource Number', field: 'resource_number' },
            { headerName: 'Employee Name', field: 'employee_name' },
            { headerName: 'Manager Name', field: 'manager_name' },
            { headerName: 'Team Type', field: 'team_type_name' },
            { headerName: 'Area', field: 'area_short_name' },
            { headerName: 'Region', field: 'region_name' },
            { headerName: 'Admin Notes', field: 'admin_notes' },
            { headerName: 'HR Status', field: 'hr_status' },
            { headerName: 'FS Status', field: 'fs_status' },
          ];
          break;
        }
        case 8: {
          url = 'api/view/get_managers_not_self_list?';
          //url = "viewemployees/new_hire.json"
          this.columnDefs = [
            {
              headerName: 'Employee ID',
              field: 'employee_id',
              width: 150,
              pinned: 'left',
              lockPinned: true,
              cellClass: 'lock-pinned',
              cellRenderer: this.createHyperLink.bind(this),
            },
            { headerName: 'Resource Number', field: 'resource_number' },
            { headerName: 'Employee Name', field: 'employee_name' },
            { headerName: 'Manager Name', field: 'manager_name' },
            { headerName: 'Team Type', field: 'team_type_name' },
            { headerName: 'Area', field: 'area_short_name' },
            { headerName: 'Region', field: 'region_name' },
            { headerName: 'Admin Notes', field: 'admin_notes' },
            { headerName: 'HR Status', field: 'hr_status' },
            { headerName: 'FS Status', field: 'fs_status' },
          ];
          break;
        }
        case 9: {
          url = 'api/view/get_record_not_complete_list?';
          //url = "viewemployees/new_hire.json"
          this.columnDefs = [
            {
              headerName: 'Employee ID',
              field: 'employee_id',
              width: 150,
              pinned: 'left',
              lockPinned: true,
              cellClass: 'lock-pinned',
              cellRenderer: this.createHyperLink.bind(this),
            },
            { headerName: 'Resource Number', field: 'resource_number' },
            { headerName: 'Employee Name', field: 'employee_name' },
            { headerName: 'Manager Name', field: 'manager_name' },
            { headerName: 'Team Type', field: 'team_type_name' },
            { headerName: 'Area', field: 'area_short_name' },
            { headerName: 'Region', field: 'region_name' },
            { headerName: 'Admin Notes', field: 'admin_notes' },
            { headerName: 'HR Status', field: 'hr_status' },
            { headerName: 'FS Status', field: 'fs_status' },
          ];
          break;
        }
        case 10: {
          url = 'api/view/get_admin_review_list?';
          //url = "viewemployees/new_hire.json"
          this.columnDefs = [
            {
              headerName: 'Employee ID',
              field: 'employee_id',
              width: 150,
              pinned: 'left',
              lockPinned: true,
              cellClass: 'lock-pinned',
              cellRenderer: this.createHyperLink.bind(this),
            },
            { headerName: 'Resource Number', field: 'resource_number' },
            { headerName: 'Employee Name', field: 'employee_name' },
            { headerName: 'Manager Name', field: 'manager_name' },
            { headerName: 'Team Type', field: 'team_type_name' },
            { headerName: 'Area', field: 'area_short_name' },
            { headerName: 'Region', field: 'region_name' },
            { headerName: 'Admin Notes', field: 'admin_notes' },
            { headerName: 'HR Status', field: 'hr_status' },
            { headerName: 'FS Status', field: 'fs_status' },
          ];
          break;
        }
        default: {
          url = 'api/view/get_loa_list?';
          //url = "viewemployees/new_hire.json"
          this.columnDefs = [
            {
              headerName: 'Employee ID',
              field: 'employee_id',
              width: 150,
              pinned: 'left',
              lockPinned: true,
              cellClass: 'lock-pinned',
              cellRenderer: this.createHyperLink.bind(this),
            },
            { headerName: 'Resource Number', field: 'resource_number' },
            { headerName: 'Employee Name', field: 'employee_name' },
            { headerName: 'Manager Name', field: 'manager_name' },
            { headerName: 'Team Type', field: 'team_type_name' },
            { headerName: 'Area', field: 'area_short_name' },
            { headerName: 'Region', field: 'region_name' },
            { headerName: 'Admin Notes', field: 'admin_notes' },
            { headerName: 'HR Status', field: 'hr_status' },
            { headerName: 'FS Status', field: 'fs_status' },
          ];
          break;
        }
      }
      let reqURL = url + query;
      //let reqURL = url;    
      //localStorage.removeItem("filteredlistView");
      //localStorage.removeItem("tabView");
      return this.cs.requestHttp('get', reqURL);
    }

  }

  onPageSizeChanged(event: any) {
    this.gridApi.paginationSetPageSize(Number(event.target.value));
  }

  downloadCSV() {
    let query = 'is_export_all=Y';
    let url;
    this.spinner.show();
    switch (this.tab.id) {
      case 1: {
        //
        url = 'api/view/get_new_hire_list?';
        //url = "viewemployees/new_hire.json"
        break;
      }
      case 2: {
        url = 'api/view/get_recent_term_list?';
        //url = "viewemployees/new_hire.json"
        break;
      }
      case 3: {
        url = 'api/view/get_loa_list?';
        //url = "viewemployees/new_hire.json"
        break;
      }
      case 4: {
        url = 'api/view/get_hierarchy_mismatches_list?';
        // url = "viewemployees/new_hire.json"
        break;
      }
      case 5: {
        url = 'api/view/get_job_mismatches_list?';
        //url = "viewemployees/new_hire.json"
        break;
      }
      case 6: {
        url = 'api/view/get_manager_mismatches_list?';
        //url = "viewemployees/new_hire.json"
        break;
      }
      case 7: {
        url = 'api/view/get_all_mismatches_list?';
        //url = "viewemployees/new_hire.json"
        break;
      }
      case 8: {
        url = 'api/view/get_managers_not_self_list?';
        //url = "viewemployees/new_hire.json"
        break;
      }
      case 9: {
        url = 'api/view/get_record_not_complete_list?';
        //url = "viewemployees/new_hire.json"
        break;
      }
      case 10: {
        url = 'api/view/get_admin_review_list?';
        //url = "viewemployees/new_hire.json"
        break;
      }

      default: {
        url = 'api/view/get_loa_list?';
        //url = "viewemployees/new_hire.json"
        break;
      }
    }
    let reqURL = url + query;
    console.log(reqURL);
    this.cs.requestHttp('get', reqURL).subscribe({
      next: (response: any) => {
        console.log(response);
        if (response['data'].records.length >= 1) {
          this.exportToCSV(response['data'].records);
        } else {
          this.toastr.error('Records are not available to export');
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
  }
  exportToCSV(data: any) {
    var keys = Object.keys(data[0]);
    let options = {
      fieldSeparator: ',',
      quoteStrings: '"',
      decimalseparator: '.',
      showLabels: true,
      showTitle: false,
      title: 'Your title',
      useBom: true,
      noDownload: false,
      removeEmptyValues: true,
      headers: keys,
    };
    try {
      const fileInfo = new ngxCsv(data, 'ViewsReport', options);
    } catch (e) {
      this.toastr.error('Failed to export');
    }
  }
  ngOnDestroy(): void {
    this.subscribeCls && this.subscribeCls.unsubscribe();
  }
}
