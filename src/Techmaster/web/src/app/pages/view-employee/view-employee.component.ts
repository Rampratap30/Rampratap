import { Component, OnInit } from '@angular/core';
import { ModalDismissReasons, NgbDatepickerConfig, NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { ViewportScroller } from '@angular/common';
import {
  ColDef,
  GridOptions,
  IDatasource,
  IGetRowsParams,
  SelectionChangedEvent,
} from 'ag-grid-community';
import { CoreService } from 'src/app/service/core.service';
import { ActivatedRoute, Router } from '@angular/router';
import { NgxSpinnerService } from 'ngx-spinner';
import { ToastrService } from 'ngx-toastr';
import { RequestWithFilterAndSort } from 'src/app/common/types';
import { FormBuilder, FormGroup } from '@angular/forms';

@Component({
  selector: 'app-view-employee',
  templateUrl: './view-employee.component.html',
  styleUrls: ['./view-employee.component.css'],
})
export class ViewEmployeeComponent implements OnInit {
  closeResult = '';
  employee!: any;
  rowDataChanges: any[] = [];
  getRole: String | undefined;
  employee_id: String | undefined;
  encoded_employee_id!: String;
  gridApiChangeR: any;
  gridColumnApiChangeR: any;
  rowDataR: any[] = [];
  selected_syncup_type!: string;
  public rowSelectionDialog: 'single' | 'multiple' = 'single';
  frmSyncUp!: FormGroup;
  retriveView: boolean = false;
  get fSyncUp() {
    return this.frmSyncUp.controls;
  }
  constructor(
    private router: Router,
    private modalService: NgbModal,
    private cs: CoreService,
    private activatedRoute: ActivatedRoute,
    private spinner: NgxSpinnerService,
    private toastr: ToastrService,
    private fb: FormBuilder,
    private config: NgbDatepickerConfig,
    private scroller: ViewportScroller,
  ) {
    const current = new Date();
    config.minDate = {
      year: current.getFullYear(),
      month: current.getMonth() + 1,
      day: current.getDate(),
    };

    config.outsideDays = 'hidden';

  }
  ngOnInit(): void {
    this.activatedRoute.paramMap.subscribe((params) => {
      this.encoded_employee_id = String(params.get('id'));
      this.employee_id = atob(String(params.get('id')));
    });

    if (!this.cs.getRole) {
      this.cs.obsGetUserInfo?.subscribe((data) => {
        this.getRole = data?.data?.userRole;
      });
    } else {
      this.getRole = this.cs.getRole;
    }

    try {
      this.getEmployeeData();
    } catch (error) {
      console.log(error);
    }

    this.frmSyncUp = this.fb.group({
      eDate: ['']
    });

  }
  gridOptions: GridOptions = {
    defaultColDef: {
      sortable: true,
    },
    rowModelType: 'infinite',
    noRowsOverlayComponent: '<div>no rows</div>',
  };

  public defaultColDef: ColDef = {
    flex: 1,
    minWidth: 100,
  };

  getEmployeeData() {
    if (this.employee_id) {
      this.spinner.show();
      let url = '/api/employee/get?employee_id=' + this.employee_id;
      this.cs.requestHttp('GET', url).subscribe({
        next: (response: any) => {
          this.employee = response?.data?.records;
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
  }
  openChanges(content: any) {
    this.modalService.open(content, { size: 'lg', ariaLabelledBy: 'modal-basic-title' }).result.then(
      (result: any) => {
        this.closeResult = `Closed with: ${result}`;
      },
      (reason: any) => {
        this.closeResult = `Dismissed ${this.getDismissReason(reason)}`;
      },
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

  onBtRequestChanges(content: any) {
    this.openChanges(content);
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
      this.employee_id;
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
        this.encoded_employee_id,
      ]);
    }
  }

  columnDefsR: ColDef[] = [
    { headerName: 'Change Id', field: 'change_id', width: 110 },
    { headerName: 'Effective Date', field: 'change_effective_date' },
    { headerName: 'Status', field: 'change_status', width: 115 },
    { headerName: 'Change Notes', field: 'change_note', width: 340 },
  ];

  isHierarchySync: boolean = false
  isJobSync: boolean = false
  isManagerSync: boolean = false

  onSyncup(content: any, type: any) {
    const syncup_types = ['job', 'hierarchy', 'manager'];
    if (syncup_types.includes(type)) {
      this.selected_syncup_type = type;
      this.open(content);
    }
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
  onSubmitSyncUp() {
    if (this.frmSyncUp.valid) {
      this.spinner.show();
      let date = this.frmSyncUp.value.eDate;
      const a = new Date(date.year + '-' + date.month + '-' + date.day);
      let month = ('0' + (a.getMonth() + 1)).slice(-2);
      let day = ('0' + (date.day)).slice(-2);

      let url = 'api/employee/syncup/' + this.employee_id;
      let obj = {
        syncup_type: this.selected_syncup_type,
        change_effective_date: date.year + '-' + month + '-' + day
      };


      this.cs.requestHttp('put', url, obj, undefined).subscribe({
        next: (response: any) => {
          this.toastr.success(response.data.message);
          this.frmSyncUp.reset();
          this.modalService.dismissAll();
          this.selected_syncup_type == 'hierarchy' ? this.isHierarchySync = true : ''
          this.selected_syncup_type == 'job' ? this.isJobSync = true : ''
          this.selected_syncup_type == 'manager' ? this.isManagerSync = true : ''
        },
        error: (err: any) => {
          this.spinner.hide();
          this.cs.handleError(err);
        },
        complete: () => {
          this.spinner.hide();
        },
      });

    }
  }

  goBack(): void {
    const nav_responses = JSON.parse(localStorage.getItem('navigationLS') || '{}');
    if (nav_responses["page"] == 'view') {
      this.retriveView = true;
      localStorage.setItem("retriveView", JSON.stringify(this.retriveView));
      this.router.navigate([`views`]);
    }
    else {
      this.router.navigate([`home`])
    }
    // this.retriveView = true;
    // localStorage.setItem("retriveView", JSON.stringify(this.retriveView));
    // const responseTab = JSON.parse(localStorage.getItem('tabView') || '{}');
    // if (Object.keys(responseTab).length > 0) {
    //   this.router.navigate([`views`])
    // } else {
    //   this.router.navigate([`home`])
    // }
  }


  displayDetail(e: any, id: any) {
    console.log(e)

    $(".list-group .list-group-item").removeClass("active");
    $(e.target).addClass("active");
    let containerAccordion = document.getElementById('containerAccordion');
    let scrollElement = document.getElementById(id);
    let topPos = scrollElement?.offsetTop;

    if (topPos != undefined) {
      if (containerAccordion != null) containerAccordion.scrollTop = topPos - 133;
    }
  }

  ngOnDestroy(): void {
    this.spinner.show();
    this.modalService.dismissAll();
    this.config.minDate != null;
  }
}
