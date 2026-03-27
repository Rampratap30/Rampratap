import { Component, OnInit, ViewChild } from '@angular/core';
import {
  FormGroup,
  FormControl,
  FormBuilder,
  Validators,
} from '@angular/forms';
import { GridOptions, IDatasource, IGetRowsParams } from 'ag-grid-community';
import { RequestWithFilterAndSort } from 'src/app/common/types';
import { environment } from './../../../environments/environment';
import { NgxSpinnerService } from 'ngx-spinner';
import { ToastrService } from 'ngx-toastr';
import { ModalDismissReasons, NgbDatepickerConfig, NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { CoreService } from 'src/app/service/core.service';
import { Subscription } from 'rxjs';
import { ngxCsv } from 'ngx-csv';
import { UpperCasePipe } from '@angular/common';

@Component({
  selector: 'app-configuration',
  templateUrl: './configuration.component.html',
  styleUrls: ['./configuration.component.css'],
})
export class ConfigurationComponent implements OnInit {
  apiURL = environment.apiURL;
  gridApi: any;
  gridColumnApi: any;
  icons: any;
  defaultPageSize = environment.defaultPageSize;
  activeTab = 1;
  getRole: string | undefined;
  isDisabled: boolean = true;
  isAddDisabled: boolean = false;
  userEntry: any;
  items: string[] = ['Yes', 'No'];
  public selectItems = [
    { optionId: 'ACTIVE', optionTitle: 'ACTIVE' },
    { optionId: 'INACTIVE', optionTitle: 'INACTIVE' },
  ];
  public selectItems_y_n = [
    { optionId: 'Y', optionTitle: 'YES' },
    { optionId: 'N', optionTitle: 'NO' },
  ];

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

  notification_types = [
    { optionId: 'CSA Notifications', optionTitle: 'CSA Notifications' },
    { optionId: 'Daily Changes', optionTitle: 'Daily Changes' },
    { optionId: 'Pending Approvals', optionTitle: 'Pending Approvals' }
  ];

  // bus_types = [
  // { optionId: 'TS', optionTitle: 'TS' },
  // { optionId: 'BS', optionTitle: 'BS' },
  // ];
  rowData: any[] = [];

  frm!: FormGroup;
  subscribeCls!: Subscription;
  get f() {
    return this.frm.controls;
  }

  frmr!: FormGroup;
  get fr() {
    return this.frmr.controls;
  }

  frma!: FormGroup;
  get fa() {
    return this.frma.controls;
  }

  frml!: FormGroup;
  get fl() {
    return this.frml.controls;
  }

  frmj!: FormGroup;
  get fj() {
    return this.frmj.controls;
  }

  frmtt!: FormGroup;
  get ftt() {
    return this.frmtt.controls;
  }

  frmn!: FormGroup;
  get fn() {
    return this.frmn.controls;
  }

  public rowSelection: 'single' | 'multiple' = 'multiple';
  isRegionAdd: boolean = true;
  directorList: any[] = [];
  FOMList: any[] = [];
  regionTitle: string | undefined;

  selectedRows: any[] = [];
  regionData: any;
  responseData: any;

  constructor(
    private cs: CoreService,
    private fb: FormBuilder,
    private spinner: NgxSpinnerService,
    private toastr: ToastrService,
    private modalService: NgbModal,
    private config: NgbDatepickerConfig,
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
  @ViewChild('openTab') openTab:
    | { nativeElement: { click: () => void } }
    | undefined;

  ngOnInit(): void {
    this.frm = this.fb.group({
      region_name: [''],
      status: [''],
      area_short_name: [''],
      area_status: [''],
      location_name: [''],
      location_status: [''],
      job_adp_code: [''],
      job_code_status: [''],
      team_type_name: [''],
      team_type_status: [''],
      notification_name: [''],
      notificationstatus: [''],
    });

    this.frmr = this.fb.group({
      region_name: ['', Validators.required],
      region_short_name: ['', Validators.required],
      region_dir_Id: ['', Validators.required],
      region_dir_resource_id: [''],
      director_email_id: [''],
      region_director_name: ['', Validators.required],
      estartDate: [''],
      status: ['ACTIVE', Validators.required],
    });

    this.frma = this.fb.group({
      area_region_name: ['', Validators.required],
      //area_name: ['', Validators.required],
      area_short_name: ['', Validators.required],
      area_director_name: ['', Validators.required],
      area_fom_name: ['', Validators.required],
      estartDate: [''],
      area_dir_empId: [''],
      area_dir_resource_id: [''],
      area_fom_emp_id: [''],
      area_fom_resource_id: [''],
      status: ['ACTIVE', Validators.required],
    });

    this.frml = this.fb.group({
      //area_id: ['', Validators.required],
      location_name: ['', Validators.required],
      location_short_name: ['', Validators.required],
      //location_code_short: ['', Validators.required],
      description: ['', Validators.required],
      zip_code: ['', Validators.required],
      inactive_date: ['', Validators.required],
    });

    this.frmj = this.fb.group({
      job_id: [''],
      //job_code: ['', Validators.required],
      job_title: ['', Validators.required],
      job_type: ['', Validators.required],
      auto_add: ['', Validators.required],
      // bus_type: ['', Validators.required],
      // job_family: [''],
      job_adp_code: ['', Validators.required],
      estartDate: [''],
      status: ['ACTIVE', Validators.required],
      manager_flag: [''],
      approval_required: ['', Validators.required],
    });

    this.frmtt = this.fb.group({
      team_types_id: [''],
      team_type_name: ['', Validators.required],
      estartDate: [''],
      status: ['ACTIVE', Validators.required],
    });

    this.frmn = this.fb.group({
      notification_id: [''],
      notification_name: ['', Validators.required],
      notification_email_id: ['', [Validators.required, Validators.email]],
      //notification_subject: ['', Validators.required],
      estartDate: [''],
      status: ['ACTIVE', Validators.required],
    });
    this.icons = {
      sortAscending: '<i class="bi bi-arrow-up "/>',
      sortDescending: '<i class="bi bi-arrow-down"/>',
    };
    setTimeout(() => {
      this.get_dropdown_directors();
    }, 1000);

    setTimeout(() => {
      this.get_dropdown_fom();
    }, 1000);

  }
  closeResult: string | undefined;

  open(content: any) {
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

  addRegion(content: any) {
    this.isRegionAdd = true;
    this.regionTitle = 'Add Region';
    this.open(content);
    this.frmr.reset();
    this.frmr.controls['status'].patchValue('ACTIVE');
  }

  editRegion(content: any) {
    this.selectedRows = this.gridApi.getSelectedRows();
    if (this.selectedRows.length == 1) {
      this.regionTitle = 'Edit Region';
      this.isRegionAdd = false;
      let url = 'api/config/region/get/' + this.selectedRows[0].region_id;
      this.spinner.show();
      this.cs.requestHttp('get', url).subscribe({
        next: (response: any) => {
          this.regionData = response['data'].records[0];
          console.log(this.regionData);
          this.open(content);
          this.frmr.patchValue({
            region_id: this.regionData.region_id,
            region_name: this.regionData.region_name,
            region_short_name: this.regionData.region_short_name,
            region_dir_Id: this.regionData.region_dir_emp_id,
            region_dir_resource_id: this.regionData.dir_resource_number,
            director_email_id: this.regionData.dir_email,
            region_director_name: parseInt(this.regionData.region_dir_emp_id),
            estartDate: this.regionData.effective_start_date,
            status: this.regionData.status,
          });
        },
        error: (err: any) => {
          this.cs.handleError(err);
          this.spinner.hide();
        },
        complete: () => {
          this.spinner.hide();
        },
      });
    } else {
      this.toastr.error('Please select only one record for Edit');
    }
  }

  onRegionSubmit() {
    if (this.frmr.valid) {
      this.spinner.show();
      // let date = this.frmr.value.estartDate;
      const current = new Date();
      let date = {
        year: current.getFullYear(),
        month: current.getMonth() + 1,
        day: current.getDate(),
      }
      const a = new Date(date.year + '-' + date.month + '-' + date.day);
      let month = ('0' + (a.getMonth() + 1)).slice(-2);
      let day = ('0' + a.getDate()).slice(-2);
      let obj;
      let method = 'post';
      let url = '';
      this.selectedRows = this.gridApi.getSelectedRows();
      if (this.selectedRows.length == 1) {
        method = 'put';
        url = 'api/config/region/update/' + this.selectedRows[0].region_id;
        obj = {
          region_name: this.frmr.value.region_name,
          region_short_name: this.frmr.value.region_short_name,
          region_dir_emp_id: this.frmr.value.region_dir_Id,
          status: this.frmr.value.status,
        };

      } else {
        url = 'api/config/region/add';
        obj = {
          region_name: this.frmr.value.region_name,
          region_short_name: this.frmr.value.region_short_name,
          region_dir_emp_id: this.frmr.value.region_dir_Id,
          effective_start_date: date.year + '-' + month + '-' + day,
          status: 'ACTIVE',
        };
        this.spinner.show();
      }
      this.cs.requestHttp(method, url, obj, false).subscribe({
        next: (response: any) => {
          this.toastr.success(response.data.message);
          this.frmr.reset();
          this.modalService.dismissAll('data submitted');
          this.isDisabled = true;
          this.isAddDisabled = false;
          this.gridApi.setDatasource(this.dataSource);
          this.selectedRows = [];
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
  onDeleteRow() {
    const selectedData = this.gridApi.getSelectedRows();
    if (selectedData.length >= 1) {
      if (confirm('Are you sure you want to De-Activate this record?')) {
        this.spinner.show();
        let url = 'api/config/region/update/bulk-delete';
        let setData = selectedData.map((employee: any) => employee.region_id);
        let obj = { region_id: setData };
        console.log(obj);
        this.cs.requestHttp('put', url, obj, undefined).subscribe({
          next: (response: any) => {
            this.toastr.success(response.data.message);
            this.gridApi.setDatasource(this.dataSource);
            this.isDisabled = true;
            this.isAddDisabled = false;
            this.selectedRows = [];
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
    } else {
      this.toastr.error('Please select record for Delete');
    }
  }
  get_dropdown_directors() {
    let url = 'api/config/common/dir-list';
    this.cs.requestHttp('get', url).subscribe({
      next: (response: any) => {
        this.directorList = response['data'].records;
      },
      error: (err: any) => {
        this.cs.handleError(err);
      },
    });
  }

  get_dropdown_fom() {
    let url = 'api/config/common/fom-list';
    this.cs.requestHttp('get', url).subscribe({
      next: (response: any) => {
        this.FOMList = response['data'].records;
      },
      error: (err: any) => {
        this.cs.handleError(err);
      },
    });
  }
  regionList: any[] = [];
  get_dropdown_regions() {
    let url = 'api/config/region/get?is_export_all=Y&status=ACTIVE';
    this.cs.requestHttp('get', url).subscribe({
      next: (response: any) => {
        this.regionList = response['data'].records;
      },
      error: (err: any) => {
        this.cs.handleError(err);
      },
    });
  }
  areaList: any[] = [];
  get_dropdown_areas() {
    let url = 'api/config/area/get?is_export_all=Y&status=ACTIVE';
    this.cs.requestHttp('get', url).subscribe({
      next: (response: any) => {
        this.areaList = response['data'].records;
      },
      error: (err: any) => {
        this.cs.handleError(err);
      },
    });
  }

  bindDirectorData(employee_id: number) {
    const selectedrow = this.directorList.filter(
      (el: any) => el.employee_id == employee_id
    );
    if (selectedrow.length > 0) {
      this.frmr.patchValue({
        region_dir_Id: selectedrow[0].employee_id,
        region_dir_resource_id: selectedrow[0].resource_number,
        director_email_id: selectedrow[0].email,
      });
      console.log(selectedrow);
    }
  }
  doRemove(event: any) {
    this.frmr.patchValue({
      region_dir_Id: '',
      region_dir_resource_id: '',
      director_email_id: '',
    });
  }

  //area
  modalTitle: string | undefined;
  isRecordAdd: boolean = true;
  addArea(content: any) {
    this.get_dropdown_regions();
    this.isRecordAdd = true;
    this.modalTitle = 'Add Area';
    this.open(content);
    this.frma.reset();
    this.frma.controls['status'].patchValue('ACTIVE');
  }

  editArea(content: any) {
    this.get_dropdown_regions();
    this.selectedRows = this.gridApi.getSelectedRows();
    if (this.selectedRows.length == 1) {
      this.modalTitle = 'Edit Area';
      this.isRecordAdd = false;
      let url = 'api/config/area/get/' + this.selectedRows[0].area_id;
      this.spinner.show();
      this.cs.requestHttp('get', url).subscribe({
        next: (response: any) => {
          this.responseData = response['data'].records[0];
          this.open(content);
          this.frma.patchValue({
            area_id: this.responseData.area_id,
            area_region_name: parseInt(this.responseData.region_id),
            //area_name: this.responseData.area_name,
            area_short_name: this.responseData.area_short_name,
            area_director_name: parseInt(this.responseData.area_dir_emp_id),
            area_dir_empId: this.responseData.area_dir_emp_id,
            area_dir_resource_id: this.responseData.dir_resource_number,
            area_fom_name: parseInt(this.responseData.area_fom_emp_id),
            area_fom_emp_id: this.responseData.area_fom_emp_id,
            area_fom_resource_id: this.responseData.fom_resource_number,
            estartDate: this.responseData.effective_start_date,
            status: this.responseData.status,
          });
        },
        error: (err: any) => {
          this.cs.handleError(err);
          this.spinner.hide();
        },
        complete: () => {
          this.spinner.hide();
        },
      });
    } else {
      this.toastr.error('Please select only one record for Edit');
    }
  }
  onSubmitArea() {
    if (this.frma.valid) {
      this.spinner.show();
      //let date = this.frma.value.estartDate;
      const current = new Date();
      let date = {
        year: current.getFullYear(),
        month: current.getMonth() + 1,
        day: current.getDate(),
      }
      const a = new Date(date.year + '-' + date.month + '-' + date.day);
      let month = ('0' + (a.getMonth() + 1)).slice(-2);
      let day = ('0' + a.getDate()).slice(-2);
      let obj;
      let method = 'post';
      let url = '';
      this.selectedRows = this.gridApi.getSelectedRows();
      if (this.selectedRows.length == 1) {
        method = 'put';
        url = 'api/config/area/update/' + this.selectedRows[0].area_id;
        obj = {
          region_id: this.frma.value.area_region_name,
          // area_name: this.frma.value.area_name,
          area_short_name: this.frma.value.area_short_name,
          area_dir_emp_id: this.frma.value.area_dir_empId,
          area_fom_emp_id: this.frma.value.area_fom_emp_id,
          status: this.frma.value.status,
        };
      } else {
        url = 'api/config/area/add';
        obj = {
          region_id: this.frma.value.area_region_name,
          // area_name: this.frma.value.area_name,
          area_short_name: this.frma.value.area_short_name,
          area_dir_emp_id: this.frma.value.area_dir_empId,
          area_fom_emp_id: this.frma.value.area_fom_emp_id,
          effective_start_date: date.year + '-' + month + '-' + day,
          status: 'ACTIVE',
        };
      }
      this.cs.requestHttp(method, url, obj, false).subscribe({
        next: (response: any) => {
          this.spinner.hide();
          this.toastr.success(response.data.message);
          this.frmr.reset();
          this.modalService.dismissAll('data submitted');
          this.isDisabled = true;
          this.isAddDisabled = false;
          this.gridApi.setDatasource(this.dataSource);
          this.selectedRows = [];
        },
        error: (err: any) => {
          this.spinner.hide();
          this.cs.handleError(err);
        },
      });
    }
  }
  onDeleteRowArea() {
    const selectedData = this.gridApi.getSelectedRows();
    if (selectedData.length >= 1) {
      if (confirm('Are you sure you want to De-Activate this record?')) {
        let url = 'api/config/area/update/bulk-delete';
        let setData = selectedData.map((area: any) => area.area_id);
        let obj = { area_id: setData };
        console.log(obj);
        this.cs.requestHttp('put', url, obj, undefined).subscribe({
          next: (response: any) => {
            this.toastr.success(response.data.message);
            this.gridApi.setDatasource(this.dataSource);
          },
          error: (err) => {
            this.cs.handleError(err);
          },
        });
      }
    } else {
      this.toastr.error('Please select record for Delete');
    }
  }

  bindAreaDirectorData(employee_id: number) {
    const selectedrow = this.directorList.filter(
      (el: any) => el.employee_id == employee_id
    );
    if (selectedrow.length > 0) {
      this.frma.patchValue({
        area_dir_empId: selectedrow[0].employee_id,
        area_dir_resource_id: selectedrow[0].resource_number,
      });
      console.log(selectedrow);
    }
  }

  doRemoveArea(event: any) {
    this.frma.patchValue({
      area_dir_empId: '',
      area_dir_resource_id: '',
    });
  }
  bindAreaFOMData(employee_id: number) {
    const selectedrow = this.FOMList.filter(
      (el: any) => el.employee_id == employee_id
    );
    if (selectedrow.length > 0) {
      this.frma.patchValue({
        area_fom_emp_id: selectedrow[0].employee_id,
        area_fom_resource_id: selectedrow[0].resource_number,
      });
      console.log(selectedrow);
    }
  }

  doRemoveFOMArea(event: any) {
    this.frma.patchValue({
      area_fom_emp_id: '',
      area_fom_resource_id: '',
    });
  }

  //Job Code
  addJobCode(content: any) {
    this.isRecordAdd = true;
    this.modalTitle = 'Add Job Code';
    this.open(content);
    this.frmj.reset();
    this.frmj.controls['status'].patchValue('ACTIVE');
  }

  editJobCode(content: any) {
    this.selectedRows = this.gridApi.getSelectedRows();
    if (this.selectedRows.length == 1) {
      this.modalTitle = 'Edit Job Code';
      this.isRecordAdd = false;
      this.spinner.show();
      let url = 'api/config/job-code/get/' + this.selectedRows[0].job_id;
      this.cs.requestHttp('get', url).subscribe({
        next: (response: any) => {
          this.responseData = response['data'].records[0];
          this.open(content);
          this.frmj.patchValue({
            job_id: this.responseData.job_id,
            //job_code: this.responseData.job_code,
            job_title: this.responseData.job_title,
            job_type: this.responseData.job_type,
            auto_add: this.responseData.auto_add,
            // bus_type: this.responseData.bus_type,
            // job_family: this.responseData.job_family,
            job_adp_code: this.responseData.job_adp_code,
            estartDate: this.responseData.effective_start_date,
            status: this.responseData.status,
            manager_flag: this.responseData.manager_flag,
            approval_required: this.responseData.approval_required,
          });
        },
        error: (err: any) => {
          this.cs.handleError(err);
          this.spinner.hide();
        },
        complete: () => {
          this.spinner.hide();
        },
      });
    } else {
      this.toastr.error('Please select only one record for Edit');
    }
  }
  onSubmitJobCode() {
    if (this.frmj.valid) {
      this.spinner.show();
      //let date = this.frmj.value.estartDate;
      const current = new Date();
      let date = {
        year: current.getFullYear(),
        month: current.getMonth() + 1,
        day: current.getDate(),
      }
      const a = new Date(date.year + '-' + date.month + '-' + date.day);
      let month = ('0' + (a.getMonth() + 1)).slice(-2);
      let day = ('0' + a.getDate()).slice(-2);
      let obj;
      let method = 'post';
      let url = '';
      this.selectedRows = this.gridApi.getSelectedRows();
      if (this.selectedRows.length == 1) {
        method = 'put';
        url = 'api/config/job-code/update/' + this.responseData.job_id;
        obj = {
          //job_code: this.frmj.value.job_code,
          job_title: this.frmj.value.job_title,
          // job_family: this.frmj.value.job_family,
          job_type: this.frmj.value.job_type,
          auto_add: this.frmj.value.auto_add,
          //bus_type: this.frmj.value.bus_type, // q
          job_adp_code: this.frmj.value.job_adp_code,
          manager_flag: this.frmj.value.manager_flag,
          approval_required: this.frmj.value.approval_required,
          //effective_start_date: this.responseData.effective_start_date,
          status: this.frmj.value.status,
        };
      } else {
        url = 'api/config/job-code/add';
        obj = {
          //job_code: this.frmj.value.job_code,
          job_title: this.frmj.value.job_title,
          // job_family: this.frmj.value.job_family,
          job_type: this.frmj.value.job_type,
          auto_add: this.frmj.value.auto_add,
          //bus_type: this.frmj.value.bus_type, // q
          job_adp_code: this.frmj.value.job_adp_code,
          manager_flag: this.frmj.value.manager_flag,
          approval_required: this.frmj.value.approval_required,
          effective_start_date: date.year + '-' + month + '-' + day,
          status: 'ACTIVE',
        };
      }
      this.cs.requestHttp(method, url, obj, false).subscribe({
        next: (response: any) => {
          this.spinner.hide();
          this.toastr.success(response.data.message);
          this.frmr.reset();
          this.modalService.dismissAll('data submitted');
          this.isDisabled = true;
          this.isAddDisabled = false;
          this.gridApi.setDatasource(this.dataSource);
          this.selectedRows = [];
        },
        error: (err: any) => {
          this.spinner.hide();
          this.cs.handleError(err);
        },
      });
    }
  }
  onDeleteRowJobCode() {
    const selectedData = this.gridApi.getSelectedRows();
    if (selectedData.length >= 1) {
      if (confirm('Are you sure you want to De-Activate this record?')) {
        let url = 'api/config/job-code/update/bulk-delete';
        let setData = selectedData.map((job: any) => job.job_id);
        let obj = { job_id: setData };
        console.log(obj);
        this.cs.requestHttp('put', url, obj, undefined).subscribe({
          next: (response: any) => {
            this.toastr.success(response.data.message);
            this.gridApi.setDatasource(this.dataSource);
            this.isDisabled = true;
            this.isAddDisabled = false;
            this.selectedRows = [];
          },
          error: (err: any) => {
            this.cs.handleError(err);
          },
        });
      }
    } else {
      this.toastr.error('Please select record for Delete');
    }
  }

  //Team Types
  addTeamTypes(content: any) {
    this.isRecordAdd = true;
    this.modalTitle = 'Add Team Type';
    this.open(content);
    this.frmtt.reset();
    this.frmtt.controls['status'].patchValue('ACTIVE');
  }

  editTeamTypes(content: any) {
    this.selectedRows = this.gridApi.getSelectedRows();
    if (this.selectedRows.length == 1) {
      this.modalTitle = 'Edit Team Type';
      this.isRecordAdd = false;
      this.spinner.show();
      let url = 'api/config/team-type/get/' + this.selectedRows[0].team_type_id;
      this.cs.requestHttp('get', url).subscribe({
        next: (response: any) => {
          this.responseData = response['data'].records[0];
          this.open(content);
          this.frmtt.patchValue({
            team_type_id: this.responseData.team_type_id,
            team_type_name: this.responseData.team_type_name,
            estartDate: this.responseData.effective_start_date,
            status: this.responseData.status,
          });
        },
        error: (err: any) => {
          this.cs.handleError(err);
          this.spinner.hide();
        },
        complete: () => {
          this.spinner.hide();
        },
      });
    } else {
      this.toastr.error('Please select only one record for Edit');
    }
  }
  onSubmitTeamTypes() {
    if (this.frmtt.valid) {
      this.spinner.show();
      //let date = this.frmtt.value.estartDate;
      const current = new Date();
      let date = {
        year: current.getFullYear(),
        month: current.getMonth() + 1,
        day: current.getDate(),
      }
      const a = new Date(date.year + '-' + date.month + '-' + date.day);
      let month = ('0' + (a.getMonth() + 1)).slice(-2);
      let day = ('0' + a.getDate()).slice(-2);
      let obj;
      let method = 'post';
      let url = '';
      this.selectedRows = this.gridApi.getSelectedRows();
      if (this.selectedRows.length == 1) {
        method = 'put';
        url = 'api/config/team-type/update/' + this.responseData.team_type_id;
        obj = {
          team_type_name: this.frmtt.value.team_type_name,
          status: this.frmtt.value.status,
        };
      } else {
        url = 'api/config/team-type/add';
        obj = {
          team_type_name: this.frmtt.value.team_type_name,
          effective_start_date: date.year + '-' + month + '-' + day,
          status: 'ACTIVE',
        };
      }
      this.cs.requestHttp(method, url, obj, false).subscribe({
        next: (response: any) => {
          this.spinner.hide();
          this.toastr.success(response.data.message);
          this.frmr.reset();
          this.modalService.dismissAll('data submitted');
          this.isDisabled = true;
          this.isAddDisabled = false;
          this.gridApi.setDatasource(this.dataSource);
          this.selectedRows = [];
        },
        error: (err: any) => {
          this.spinner.hide();
          this.cs.handleError(err);
        },
      });
    }
  }
  onDeleteRowTeamTypes() {
    const selectedData = this.gridApi.getSelectedRows();
    if (selectedData.length >= 1) {
      if (confirm('Are you sure you want to De-Activate this record?')) {
        let url = 'api/config/team-type/update/bulk-delete';
        let setData = selectedData.map(
          (team_type: any) => team_type.team_type_id
        );
        let obj = { team_type_id: setData };
        console.log(obj);
        this.cs.requestHttp('put', url, obj, undefined).subscribe({
          next: (response: any) => {
            this.toastr.success(response.data.message);
            this.gridApi.setDatasource(this.dataSource);
            this.isDisabled = true;
            this.isAddDisabled = false;
            this.selectedRows = [];
          },
          error: (err: any) => {
            this.cs.handleError(err);
          },
        });
      }
    } else {
      this.toastr.error('Please select record for Delete');
    }
  }

  //Notification
  addNotification(content: any) {
    this.isRecordAdd = true;
    this.modalTitle = 'Add Notification';
    this.open(content);
    this.frmn.reset();
    this.frmn.controls['status'].patchValue('ACTIVE');
  }

  editNotification(content: any) {
    this.selectedRows = this.gridApi.getSelectedRows();
    if (this.selectedRows.length == 1) {
      this.modalTitle = 'Edit Notification';
      this.isRecordAdd = false;
      this.spinner.show();
      let url =
        'api/config/notificaion_set_up/get/' +
        this.selectedRows[0].notification_id;
      this.cs.requestHttp('get', url).subscribe({
        next: (response: any) => {
          this.responseData = response['data'].records[0];
          this.open(content);
          this.frmn.patchValue({
            notification_id: this.responseData.notification_id,
            notification_name: this.responseData.notification_name,
            notification_email_id: this.responseData.notification_email_id,
            // notification_subject: this.responseData.notification_subject,
            estartDate: this.responseData.effective_start_date,
            status: this.responseData.status,
          });
        },
        error: (err: any) => {
          this.cs.handleError(err);
          this.spinner.hide();
        },
        complete: () => {
          this.spinner.hide();
        },
      });
    } else {
      this.toastr.error('Please select only one record for Edit');
    }
  }
  onSubmitNotification() {
    if (this.frmn.valid) {
      this.spinner.show();
      //let date = this.frmn.value.estartDate;
      const current = new Date();
      let date = {
        year: current.getFullYear(),
        month: current.getMonth() + 1,
        day: current.getDate(),
      }
      const a = new Date(date.year + '-' + date.month + '-' + date.day);
      let month = ('0' + (a.getMonth() + 1)).slice(-2);
      let day = ('0' + a.getDate()).slice(-2);
      let obj;
      let method = 'post';
      let url = '';
      this.selectedRows = this.gridApi.getSelectedRows();
      if (this.selectedRows.length == 1) {
        method = 'put';
        url =
          'api/config/notificaion_set_up/update/' +
          this.responseData.notification_id;
        obj = {
          notification_name: this.frmn.value.notification_name,
          email_id: this.frmn.value.notification_email_id,
          // notification_subject: this.frmn.value.notification_subject,
          status: this.frmn.value.status,
        };
      } else {
        url = 'api/config/notificaion_set_up/add';
        obj = {
          notification_name: this.frmn.value.notification_name,
          email_id: this.frmn.value.notification_email_id,
          // notification_subject: this.frmn.value.notification_subject,
          effective_start_date: date.year + '-' + month + '-' + day,
          status: 'ACTIVE',
        };
      }
      this.cs.requestHttp(method, url, obj, false).subscribe({
        next: (response: any) => {
          this.spinner.hide();
          this.toastr.success(response.data.message);
          this.frmr.reset();
          this.modalService.dismissAll('data submitted');
          this.isDisabled = true;
          this.isAddDisabled = false;
          this.gridApi.setDatasource(this.dataSource);
          this.selectedRows = [];
        },
        error: (err: any) => {
          this.spinner.hide();
          this.cs.handleError(err);
        },
      });
    }
  }
  onDeleteRowNotification() {
    const selectedData = this.gridApi.getSelectedRows();
    if (selectedData.length >= 1) {
      if (confirm('Are you sure you want to De-Activate this record?')) {
        let url = 'api/config/notificaion_set_up/update/bulk-delete';
        let setData = selectedData.map(
          (notification: any) => notification.notification_id
        );
        let obj = { notification_id: setData };
        console.log(obj);
        this.cs.requestHttp('put', url, obj, undefined).subscribe({
          next: (response: any) => {
            this.toastr.success(response.data.message);
            this.gridApi.setDatasource(this.dataSource);
            this.isDisabled = true;
            this.isAddDisabled = false;
            this.selectedRows = [];
          },
          error: (err: any) => {
            this.cs.handleError(err);
          },
        });
      }
    } else {
      this.toastr.error('Please select record for Delete');
    }
  }

  gridOptions: GridOptions = {
    defaultColDef: {
      sortable: false,
      //unSortIcon: true,
      resizable: true,
      //filter:true,
    },
    rowModelType: 'infinite',
  };

  onGridReady(params: any) {
    this.isDisabled = true;
    this.isAddDisabled = false;
    this.resetForm();
    this.frm.reset();
    this.gridApi = params.api;
    this.gridColumnApi = params.columnApi;
    this.gridApi.setDatasource(this.dataSource);
  }

  dataSource: IDatasource = {
    getRows: (params: IGetRowsParams) => {
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
      this.getConfigData(
        request,
        this.gridApi.paginationGetCurrentPage(),
        this.gridApi.paginationGetPageSize()
      ).subscribe({
        next: (response: any) => {
          params.successCallback(
            response['data'].records,
            response['data'].total_items
          );
          this.autoSizeAll(false);
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

  getConfigData(
    requestWithSortAndFilter: RequestWithFilterAndSort,
    page: number,
    size: number
  ) {
    page++;
    this.spinner.show();
    let query = 'page=' + page + '&per_page=' + size;
    if (requestWithSortAndFilter.colId) {
      query +=
        '&order_by=' +
        requestWithSortAndFilter.colId +
        '&order=' +
        requestWithSortAndFilter.sort;
    }
    let url = '';
    switch (this.activeTab) {
      case 1: {
        // region
        url = '/api/config/region/get?';
        this.frm.value.region_name
          ? (query += '&region_name=' + this.frm.value.region_name)
          : '';
        this.frm.value.status
          ? (query += '&status=' + this.frm.value.status)
          : '';
        break;
      }
      case 2: {
        // area
        url = '/api/config/area/get?';
        this.frm.value.area_short_name
          ? (query += '&area_short_name=' + this.frm.value.area_short_name)
          : '';
        this.frm.value.area_status
          ? (query += '&status=' + this.frm.value.area_status)
          : '';
        break;
      }
      case 3: {
        // Location
        url = '/api/config/location/get?';
        this.frm.value.location_name
          ? (query += '&location_name=' + this.frm.value.location_name)
          : '';
        this.frm.value.location_status
          ? (query += '&status=' + this.frm.value.location_status)
          : '';
        break;
      }
      case 4: {
        // Jobcode
        url = '/api/config/job-code/get?';
        this.frm.value.job_adp_code
          ? (query += '&job_adp_code=' + this.frm.value.job_adp_code)
          : '';
        this.frm.value.job_code_status
          ? (query += '&status=' + this.frm.value.job_code_status)
          : '';
        break;
      }
      case 5: {
        //Team_types
        url = '/api/config/team-type/get?';
        this.frm.value.team_type_name
          ? (query += '&team_type_name=' + this.frm.value.team_type_name)
          : '';
        this.frm.value.team_type_status
          ? (query += '&status=' + this.frm.value.team_type_status)
          : '';
        break;
      }
      case 6: {
        //Notification notification_name ,notificationstatus
        url = '/api/config/notificaion_set_up/get?';
        this.frm.value.notification_name
          ? (query += '&notification_name=' + this.frm.value.notification_name)
          : '';
        this.frm.value.notificationstatus
          ? (query += '&status=' + this.frm.value.notificationstatus)
          : '';
        break;
      }
      default: {
        url = '/api/config/region/get?';
        this.frm.value.region_name
          ? (query += '&region_name=' + this.frm.value.region_name)
          : '';
        this.frm.value.status
          ? (query += '&status=' + this.frm.value.status)
          : '';
        break;
      }
    }
    let reqURL = url + query;
    return this.cs.requestHttp('get', reqURL);
  }

  onPageSizeChanged(event: any) {
    this.gridApi.paginationSetPageSize(Number(event.target.value));
  }

  autoSizeAll(skipHeader: boolean) {
    const allColumnIds: string[] = [];
    this.gridColumnApi.getColumns()!.forEach((column: any) => {
      allColumnIds.push(column.getId());
    });
    this.gridColumnApi.autoSizeColumns(allColumnIds, skipHeader);
  }

  columnDefs: any = [
    {
      headerName: 'Select',
      field: 'select',
      width: 50,
      pinned: 'left',
      lockPinned: true,
      cellClass: 'lock-pinned',
      headerCheckboxSelection: true,
      headerCheckboxSelectionFilteredOnly: true,
      checkboxSelection: true,
      sortable: false,
    },
    { headerName: 'Region Name', field: 'region_name' },
    { headerName: 'Region Short Name', field: 'region_short_name' },
    { headerName: 'Director Name', field: 'dir_employee_name' },
    { headerName: 'Director Id', field: 'region_dir_emp_id' },
    { headerName: 'Director Resource Number', field: 'dir_resource_number' },
    { headerName: 'Director Email ID', field: 'dir_email' },
    // { headerName: 'Effective Start Date', field: 'effective_start_date' },
    //  { headerName: 'Effective End Date', field: 'effective_end_date' },
    { headerName: 'Status', field: 'status' },
  ];

  columnDefsArea: any = [
    {
      headerName: 'Select',
      field: 'select',
      width: 50,
      pinned: 'left',
      lockPinned: true,
      cellClass: 'lock-pinned',
      headerCheckboxSelection: true,
      headerCheckboxSelectionFilteredOnly: true,
      checkboxSelection: true,
      sortable: false,
    },
    { headerName: 'Region Name', field: 'region_name' },
    { headerName: 'Area Short Name', field: 'area_short_name' },
    { headerName: 'Director Emp Id', field: 'area_dir_emp_id' },
    { headerName: 'Director Name', field: 'dir_employee_name' },
    { headerName: 'Fom Emp Id', field: 'area_fom_emp_id' },
    { headerName: 'Fom Name', field: 'fom_employee_name' },
    //{ headerName: 'Effective Start Date', field: 'effective_start_date' },
    //  { headerName: 'Effective End Date', field: 'effective_end_date' },
    { headerName: 'Status', field: 'status' },
  ];

  columnLocationDefs: any = [
    {
      headerName: 'Select',
      field: 'select',
      width: 50,
      pinned: 'left',
      lockPinned: true,
      cellClass: 'lock-pinned',
      headerCheckboxSelection: true,
      headerCheckboxSelectionFilteredOnly: true,
      checkboxSelection: true,
      sortable: false,
    },
    { headerName: 'Location Code', field: 'location_code' },
    { headerName: 'Description ', field: 'description' },
    { headerName: 'Zip Code', field: 'zip_code' },
    { headerName: 'Inactive Date', field: 'inactive_date' },
  ];

  columnJobcodeDefs: any = [
    {
      headerName: 'Select',
      field: 'select',
      width: 50,
      pinned: 'left',
      lockPinned: true,
      cellClass: 'lock-pinned',
      headerCheckboxSelection: true,
      headerCheckboxSelectionFilteredOnly: true,
      checkboxSelection: true,
      sortable: false,
    },
    { headerName: 'Job Id', field: 'job_id', sortable: true, unSortIcon: true },
    //{ headerName: 'Job Code', field: 'job_code' },
    { headerName: 'Job ADP', field: 'job_adp_code', sortable: true, unSortIcon: true },
    { headerName: 'Job Title', field: 'job_title', sortable: true, unSortIcon: true },
    { headerName: 'Job Type', field: 'job_type', sortable: true, unSortIcon: true },
    { headerName: 'Manager Flag', field: 'manager_flag', sortable: true, unSortIcon: true },
    { headerName: 'Approval Required', field: 'approval_required', sortable: true, unSortIcon: true },
    { headerName: 'Auto Add', field: 'auto_add', sortable: true, unSortIcon: true },
    //{ headerName: 'Effective Start Date', field: 'effective_start_date' },
    // { headerName: 'Effective End Date', field: 'effective_end_date' },
    { headerName: 'Status', field: 'status', sortable: true, unSortIcon: true },
  ];

  columnTeamTypesDefs: any = [
    {
      headerName: 'Select',
      field: 'select',
      width: 50,
      pinned: 'left',
      lockPinned: true,
      cellClass: 'lock-pinned',
      headerCheckboxSelection: true,
      headerCheckboxSelectionFilteredOnly: true,
      checkboxSelection: true,
      sortable: false,
    },
    { headerName: 'Team Type Id', field: 'team_type_id' },
    { headerName: 'Team Type Name', field: 'team_type_name' },
    //{ headerName: 'Effective Start Date', field: 'effective_start_date' },
    //  { headerName: 'Effective End Date', field: 'effective_end_date' },
    { headerName: 'Status', field: 'status' },
  ];

  columnDefs_Notification: any = [
    {
      headerName: 'Select',
      field: 'select',
      width: 50,
      pinned: 'left',
      lockPinned: true,
      cellClass: 'lock-pinned',
      headerCheckboxSelection: true,
      headerCheckboxSelectionFilteredOnly: true,
      checkboxSelection: true,
      sortable: false,
    },
    { headerName: 'Notification Name', field: 'notification_name' },
    { headerName: 'Email Id', field: 'notification_email_id' },
    // { headerName: 'Notification Subject', field: 'notification_subject' },
    //{ headerName: 'Effective Start Date', field: 'effective_start_date' },
    // { headerName: 'Effective End Date', field: 'effective_end_date' },
    { headerName: 'Status', field: 'status' },
  ];

  onSelectionChanged(event: any) {
    this.selectedRows = this.gridApi.getSelectedRows();
    if (this.selectedRows.length > 0) {
      this.isDisabled = false;
      this.isAddDisabled = true;
    } else {
      this.isDisabled = true;
      this.isAddDisabled = false;
    }
  }

  onAddRow() {
    if (
      this.userEntry.value.add_region_name ||
      this.userEntry.value.add_region_short_name ||
      this.userEntry.value.add_region_dir_Id ||
      this.userEntry.value.add_director_email_id ||
      this.userEntry.value.add_region_dir_resource_id
    ) {
      let newrows = [
        {
          select: '',
          edit: '',
          region_name: this.userEntry.value.add_region_name,
          region_short_name: this.userEntry.value.add_region_short_name,
          employee_name: this.userEntry.value.add_region_director_name,
          region_dir_emp_id: this.userEntry.value.add_region_dir_Id,
          resource_number: this.userEntry.value.add_director_email_id,
          email: this.userEntry.value.add_region_dir_resource_id,
          status: '',
        },
      ];
      var res = this.gridApi.applyTransaction({
        add: newrows,
        addIndex: 9,
      });
    }
  }

  //region tab
  onSearchSubmit() {
    this.gridApi.setDatasource(this.dataSource);
  }

  resetForm() {
    this.frm.reset();
    this.frmr.reset();
    this.frma.reset();
    this.frml.reset();
    this.frmj.reset();
    this.frmtt.reset();
    this.frmn.reset();
  }

  clearData() {
    this.resetForm();
    this.gridApi.setDatasource(this.dataSource);
    this.selectedRows = [];
    this.isDisabled = true;
    this.isAddDisabled = false;

  }

  ngOnDestroy(): void {
    this.config.minDate != null;
    this.subscribeCls && this.subscribeCls.unsubscribe();
  }

  ExportData() {
    switch (this.activeTab) {
      case 1: {
        var params = {
          columnKeys: [
            'region_name',
            'region_short_name',
            'dir_employee_name',
            'region_dir_emp_id',
            'dir_resource_number',
            'dir_email',
            // 'effective_start_date',
            'status',
          ],
        };
        this.gridApi.exportDataAsCsv(params);
        break;
      }
      case 2: {
        var params = {
          columnKeys: [
            'region_name',
            'area_short_name',
            'area_dir_emp_id',
            'dir_employee_name',
            'area_fom_emp_id',
            'fom_employee_name',
            //'effective_start_date',
            //'effective_end_date',
            'status',
          ],
        };
        this.gridApi.exportDataAsCsv(params);
        break;
      }
      case 3: {
        var params = {
          columnKeys: [
            'location_code',
            'description',
            'zip_code',
            'inactive_date',
          ],
        };
        this.gridApi.exportDataAsCsv(params);
        break;
      }
      case 4: {
        var params = {
          columnKeys: [
            'job_id',
            //'job_code',
            'job_adp_code',
            'job_title',
            'job_type',
            'manager_flag',
            'approval_required',
            'auto_add',
            //'effective_start_date',
            // 'effective_end_date',
            'status',
          ],
        };
        this.gridApi.exportDataAsCsv(params);
        break;
      }
      case 5: {
        var params = {
          columnKeys: [
            'team_type_id',
            'team_type_name',
            //'effective_start_date',
            // 'effective_end_date',
            'status',
          ],
        };
        this.gridApi.exportDataAsCsv(params);
        break;
      }
      case 6: {
        var params = {
          columnKeys: [
            'notification_name',
            'notification_email_id',
            // 'notification_subject',
            //'effective_start_date',
            // 'effective_end_date',
            'status',
          ],
        };
        this.gridApi.exportDataAsCsv(params);
        break;
      }
    }
  }
  BulkExportData() {
    let query = 'is_export_all=Y';
    let url;
    this.spinner.show();
    switch (this.activeTab) {
      case 1: {
        url = 'api/config/region/get?';
        break;
      }
      case 2: {
        url = 'api/config/area/get?';
        break;
      }
      case 3: {
        url = 'api/config/location/get?';
        break;
      }
      case 4: {
        url = 'api/config/job-code/get?';
        break;
      }
      case 5: {
        url = 'api/config/team-type/get?';
        break;
      }
      case 6: {
        url = 'api/config/notificaion_set_up/get?';
        break;
      }

      default: {
        url = 'api/config/region/get?';
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

  BulkExportLocationData() {
    this.spinner.show();
    let url = '/api/home/bulk_export';
    let obj = {
      msg: 'Location Screen',
      type: 'location',
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
  exportToCSV(data: any) {
    let formatdata = []
    switch (this.activeTab) {
      case 1: { //region
        formatdata = data.map((row: any) => {
          return {
            region_name: row.region_name,
            region_short_name: row.region_short_name,
            director_name: row.dir_employee_name,
            Director_Id: row.region_dir_emp_id,
            director_resource_number: row.dir_resource_number,
            Director_Email_ID: row.dir_email,
            //effective_start_date: row.effective_start_date,
            status: row.status
          };
        })
        break;
      }
      case 2: { // area
        formatdata = data.map((row: any) => {
          return {
            region_name: row.region_name,
            area_short_name: row.area_short_name,
            Director_Emp_Id: row.area_dir_emp_id,
            director_name: row.dir_employee_name,
            Fom_Emp_Id: row.area_fom_emp_id,
            Fom_Name: row.fom_employee_name,
            //effective_start_date: row.effective_start_date,
            status: row.status
          };
        })
        break;
      }
      case 3: {//Location
        formatdata = data.map((row: any) => {
          return {
            location_code: row.location_code,
            description: row.description,
            zip_code: row.zip_code,
            inactive_date: row.inactive_date,
          };
        })
        break;
      }
      case 4: { //Job Code
        formatdata = data.map((row: any) => {
          return {
            job_id: row.job_id,
            //job_code: row.job_code,
            job_adp_code: row.job_adp_code,
            job_title: row.job_title,
            job_type: row.job_type,
            auto_add: row.auto_add,
            manager_flag: row.manager_flag,
            approval_required: row.approval_required,
            //effective_start_date: row.effective_start_date,
            status: row.status
          };
        })
        break;
      }
      case 5: { //team type
        formatdata = data.map((row: any) => {
          return {
            team_type_id: row.team_type_id,
            team_type_name: row.team_type_name,
            //effective_start_date: row.effective_start_date,
            status: row.status
          };
        })
        break;
      }
      case 6: { // Notification
        formatdata = data.map((row: any) => {
          return {
            notification_name: row.notification_name,
            notification_email_id: row.notification_email_id,
            // notification_subject: row.notification_subject,
            //effective_start_date: row.effective_start_date,
            status: row.status
          };
        })
        break;
      }
      default: {
        //url = 'api/config/region/get?';
        break;
      }
    }


    var keys = Object.keys(formatdata[0]);
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
      headers: keys.map(function (x) { return x.toUpperCase().replaceAll('_', ' '); }),
    };
    try {
      const fileInfo = new ngxCsv(formatdata, 'ViewsReport', options);
    } catch (e) {
      this.toastr.error('Failed to export');
    }
  }
}
