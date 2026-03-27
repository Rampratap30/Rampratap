import { Component, OnInit } from '@angular/core';
import {
  AbstractControl,
  FormBuilder,
  FormGroup,
  Validators,
} from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { NgbDatepickerConfig } from '@ng-bootstrap/ng-bootstrap';
import { NgxSpinnerService } from 'ngx-spinner';
import { ToastrService } from 'ngx-toastr';
import { Subject, debounceTime, distinctUntilChanged, switchMap } from 'rxjs';
import { CoreService } from 'src/app/service/core.service';

@Component({
  selector: 'app-add-employee',
  templateUrl: './add-employee.component.html',
  styleUrls: ['./add-employee.component.css'],
})
export class AddEmployeeComponent implements OnInit {
  previousDateSelection: any;
  frm!: FormGroup;
  frmChangeMain!: FormGroup;
  frmEmpD!: FormGroup;
  frmHierarchy!: FormGroup;
  frmManager!: FormGroup;
  frmEmpJob!: FormGroup;
  frmService!: FormGroup;
  frmHrStatus!: FormGroup;
  frmAdmin!: FormGroup;
  get f() {
    return this.frm.controls;
  }
  responseData: any;
  employee: any;
  getRole: String | undefined;
  teamtypeList: any[] = [];
  regionList: any[] = [];
  areaList: any[] = [];
  locationList: any[] = [];
  managerList: any[] = [];
  jobCodeList: any[] = [];
  employee_id!: String;
  isDedicatedTo: boolean = false;
  selectItems = this.cs.selectItems;
  selectActive = this.cs.selectActive;
  workShiftDropDown = this.cs.workShiftDropDown;
  onSiteDropDown = this.cs.onSiteDropDown;
  businessOrgDropDown = this.cs.businessOrgDropDown;
  constructor(
    private spinner: NgxSpinnerService,
    private toastr: ToastrService,
    private cs: CoreService,
    private fb: FormBuilder,
    private config: NgbDatepickerConfig,
    private activatedRoute: ActivatedRoute,
    private router: Router
  ) {
    const current = new Date();
    config.minDate = {
      month: current.getMonth() + 1,
      day: current.getDate(),
      year: current.getFullYear(),
    };
    this.previousDateSelection = {
      month: current.getMonth() + 1,
      day: current.getDate(),
      year: current.getFullYear() - 50,
    };
    config.outsideDays = 'hidden';
  }

  ngOnInit(): void {
    try {
      this.isDedicatedTo = false;
      this.activatedRoute?.paramMap?.subscribe((params: any) => {
        this.employee_id = atob(String(params.get('id')));
      });

      if (!this.cs.getRole) {
        this.cs.obsGetUserInfo?.subscribe((data) => {
          this.getRole = data?.data?.userRole;
        });
      } else {
        this.getRole = this.cs.getRole;
      }

      this.frmChangeMain = this.fb.group({
        change_note: ['', Validators.required],
        change_effective_date: ['', Validators.required],
      });

      this.frmEmpD = this.fb.group({
        employeeId: ['', Validators.required],
        alternate_email: [''],
        admin_notes: [''],
      });

      this.frmHierarchy = this.fb.group({
        region: ['', Validators.required],
        area_short_name: ['', Validators.required],
      });

      this.frmManager = this.fb.group({
        manager_employee_id: ['', Validators.required],
      });

      this.frmEmpJob = this.fb.group({
        job_id: [''],
        job_title: ['', Validators.required],
        job_adp_code: ['', Validators.required],
        job_type: [''],
      });

      this.frmService = this.fb.group({
        team_type: ['', Validators.required],
        business_org: ['', Validators.required],
        work_shift: [''],
        on_call: [''],
        on_site: [''],
        dedicated: [''],
        dedicated_to: [''],
        service_advantage: [''],
        fs_status: ['', Validators.required],
        service_start_date: ['', Validators.required],
        service_end_date: [''],
        record_complete: ['', Validators.required],
      });
      this.frmHrStatus = this.fb.group({
        absence_start_date: [''],
        absence_end_date: [''],
        actual_return_to_work: [''],
      });
      this.frmAdmin = this.fb.group({
        manager_flag: ['', Validators.required],
        review_date: [''],
      });
      this.frm = this.fb.group({
        frmChangeMain: this.frmChangeMain,
        frmEmpD: this.frmEmpD,
        frmHierarchy: this.frmHierarchy,
        frmManager: this.frmManager,
        frmEmpJob: this.frmEmpJob,
        frmService: this.frmService,
        frmHrStatus: this.frmHrStatus,
        frmAdmin: this.frmAdmin,
      });

      this.employee = {

        "admin": {
          "ebs_user_name": null,
          "manager_flag": null,
          "review_date": null
        },
        "employee": {
          "admin_notes": null,
          "alternate_email": null,
          "email": null,
          "employee_id": null,
          "employee_name": null,
          "resource_number": null
        },
        "employee_job_code": {
          "job_adp_code": null,
          "job_id": null,
          "job_match_to_hr": null,
          "job_status": null,
          "job_title": null,
          "job_type": null,
          "system": {
            "system_job_adp_code": null,
            "system_job_code": null,
            "system_job_title": null
          }
        },
        "hierarchy": {
          "area_short_name": null,
          "area_status": null,
          "location_code": null,
          "location_match_to_hr": null,
          "region_name": null,
          "region_status": null,
          "system": {
            "system_area_name": null,
            "system_area_short_name": null,
            "system_location_code": null,
            "system_region_name": null
          }
        },
        "hierarchy_details": {
          "area_dir_email": null,
          "area_dir_employee_id": null,
          "area_dir_employee_name": null,
          "area_dir_resource_number": null,
          "area_fom_email": null,
          "area_fom_employee_id": null,
          "area_fom_employee_name": null,
          "area_fom_resource_number": null,
          "region_dir_email": null,
          "region_dir_employee_id": null,
          "region_dir_employee_name": null,
          "region_dir_resource_number": null
        },
        "hr_status": {
          "absence_end_date": null,
          "absence_start_date": null,
          "actual_return_to_work": null,
          "actual_termination_date": null,
          "hr_status": null,
          "last_hire_date": null
        },
        "manager": {
          "email": null,
          "manager_employee_id": null,
          "manager_flag": null,
          "manager_match_to_hr": null,
          "manager_name": null,
          "resource_number": null,
          "system": {
            "system_manager_employee_id": null,
            "system_manager_name": null
          }
        },
        "ofsc": {
          "alternate_email": null,
          "last_login": null,
          "status": null
        },
        "service": {
          "business_org": null,
          "cip": null,
          "contingent_worker": null,
          "dedicated": null,
          "dedicated_to": null,
          "fs_status": null,
          "job_type": null,
          "on_call": null,
          "on_site": null,
          "production_print": null,
          "record_complete": null,
          "service_advantage": null,
          "service_end_date": null,
          "service_start_date": null,
          "team_status": null,
          "team_type": null,
          "work_shift": null
        },
        "system": {
          "last_update_date": null,
          "last_updated_by": null
        }

        ,
        "errors": null,
        "links": null,
        "meta": null
      };
    } catch (error) {
      console.log(error);
    }
  }

  clearData() {
    this.frm.reset();
    $('#employeeId').prop('readonly', false);
    this.employee = {

      "admin": {
        "ebs_user_name": null,
        "manager_flag": null,
        "review_date": null
      },
      "employee": {
        "admin_notes": null,
        "alternate_email": null,
        "email": null,
        "employee_id": null,
        "employee_name": null,
        "resource_number": null
      },
      "employee_job_code": {
        "job_adp_code": null,
        "job_id": null,
        "job_match_to_hr": null,
        "job_status": null,
        "job_title": null,
        "job_type": null,
        "system": {
          "system_job_adp_code": null,
          "system_job_code": null,
          "system_job_title": null
        }
      },
      "hierarchy": {
        "area_short_name": null,
        "area_status": null,
        "location_code": null,
        "location_match_to_hr": null,
        "region_name": null,
        "region_status": null,
        "system": {
          "system_area_name": null,
          "system_area_short_name": null,
          "system_location_code": null,
          "system_region_name": null
        }
      },
      "hierarchy_details": {
        "area_dir_email": null,
        "area_dir_employee_id": null,
        "area_dir_employee_name": null,
        "area_dir_resource_number": null,
        "area_fom_email": null,
        "area_fom_employee_id": null,
        "area_fom_employee_name": null,
        "area_fom_resource_number": null,
        "region_dir_email": null,
        "region_dir_employee_id": null,
        "region_dir_employee_name": null,
        "region_dir_resource_number": null
      },
      "hr_status": {
        "absence_end_date": null,
        "absence_start_date": null,
        "actual_return_to_work": null,
        "actual_termination_date": null,
        "hr_status": null,
        "last_hire_date": null
      },
      "manager": {
        "email": null,
        "manager_employee_id": null,
        "manager_flag": null,
        "manager_match_to_hr": null,
        "manager_name": null,
        "resource_number": null,
        "system": {
          "system_manager_employee_id": null,
          "system_manager_name": null
        }
      },
      "ofsc": {
        "alternate_email": null,
        "last_login": null,
        "status": null
      },
      "service": {
        "business_org": null,
        "cip": null,
        "contingent_worker": null,
        "dedicated": null,
        "dedicated_to": null,
        "fs_status": null,
        "job_type": null,
        "on_call": null,
        "on_site": null,
        "production_print": null,
        "record_complete": null,
        "service_advantage": null,
        "service_end_date": null,
        "service_start_date": null,
        "team_status": null,
        "team_type": null,
        "work_shift": null
      },
      "system": {
        "last_update_date": null,
        "last_updated_by": null
      }

      ,
      "errors": null,
      "links": null,
      "meta": null
    };

  }
  onCancel() {
    this.router.navigate(['home']);
  }

  get_dropdown_regions() {
    let url = 'api/config/region/get?is_export_all=Y&status=ACTIVE';
    //let url = '../../assets/json/home/region_list_dropdown.json';
    this.cs.requestHttp('get', url).subscribe({
      next: (response: any) => {
        this.regionList = response['data'].records;
      },
      error: (err: any) => {
        this.spinner.hide();
        this.cs.handleError(err);
      },
      complete: () => { },
    });
  }
  get_dropdown_areas(value: any) {
    let url = 'api/config/area/get?region_name=' + value + '&status=ACTIVE';
    //let url = '../../assets/json/home/area_list_dropdown.json';
    this.cs.requestHttp('get', url).subscribe({
      next: (response: any) => {
        this.areaList = response['data'].records;
      },
      error: (err: any) => {
        this.spinner.hide();
        this.cs.handleError(err);
      },
      complete: () => { },
    });
  }

  get_dropdown_teamtype() {
    let url = 'api/config/team-type/get?is_export_all=Y&status=ACTIVE';
    //let url = '../../assets/json/home/team_type_list_dropdown.json';
    this.cs.requestHttp('get', url).subscribe({
      next: (response: any) => {
        this.teamtypeList = response['data'].records;
      },
      error: (err: any) => {
        this.spinner.hide();
        this.cs.handleError(err);
      },
      complete: () => { },
    });
  }
  get_dropdown_manager() {
    let url = '/api/home/get_manager_list?is_export_all=Y&order_by=EMPLOYEE_NAME&order=asc';
    this.cs.requestHttp('get', url).subscribe({
      next: (response: any) => {
        if (response['data'].records.length > 0) {
          this.managerList = response['data'].records.map((row: any) => {
            return {
              ...row,
              manageridandname: row.manager_id + ' ' + row.manager_name,
            };
          });
        }
      },
      error: (err: any) => {
        this.spinner.hide();
        this.cs.handleError(err);
      },
      complete: () => { },
    });
  }
  get_dropdown_jobCode() {
    let url =
      'api/config/job-code/get?is_export_all=Y&status=ACTIVE&order_by=JOB_TITLE&order=asc';
    this.cs.requestHttp('get', url).subscribe({
      next: (response: any) => {
        this.jobCodeList = response['data'].records.map((row: any) => {
          return {
            ...row,
            jobidandname: row.job_adp_code + ' - ' + row.job_title,
          };
        });
      },
      error: (err: any) => {
        this.spinner.hide();
        this.cs.handleError(err);
      },
      complete: () => { },
    });
  }
  bindJobCodeData(job_id: number) {
    const selectedrow = this.jobCodeList.filter(
      (job: any) => job.job_id == job_id
    );
    if (selectedrow.length > 0) {
      this.frm.patchValue({
        frmEmpJob: {
          job_id: job_id,
          job_title: selectedrow[0].job_title,
          job_adp_code: selectedrow[0].job_adp_code,
          job_type: selectedrow[0].job_type,
        }
      });
      console.log(selectedrow);
    }
  }
  doRemove(event: any) {
    this.frm.patchValue({
      frmEmpJob: {
        job_id: null,
        job_title: null,
        job_adp_code: null,
        job_type: null,
      }
    });
  }
  selectEmployee() {
    this.spinner.show();
    if (this.frmEmpD.value.employeeId != "" && this.frmEmpD.value.employeeId != null) {
      let url = 'api/employee/is_employee_exists?employee_id=' + this.frmEmpD.value.employeeId;
      this.cs.requestHttp('get', url).subscribe({
        next: (response: any) => {
          console.log(response.data)
          if (response.data != null) {
            this.get_dropdown_manager();
            this.get_dropdown_regions();
            this.get_dropdown_teamtype();
            this.get_dropdown_jobCode();
            this.employee = response['data'].records;
            $('#employeeId').prop('readonly', true);
            this.setFormData();
          } else {
            this.toastr.error(response.errors.message)
            this.frm.reset();
          }
        },
        error: (err: any) => {
          this.frm.reset();
          this.spinner.hide();
          (err.status == 400 && err?.error?.errors?.message) ? this.toastr.error(err?.error?.errors?.message) : this.cs.handleError(err);
        },
        complete: () => {
          this.spinner.hide();
          this.toastr.success('Employee exists in HRMS.')

        },
      });

    } else {
      this.toastr.error('Please enter valid employee id')
      this.frm.patchValue({
        frmEmpD: {
          employeeId: ""
        }
      })
      this.spinner.hide();
    }
  }

  // getEmployeeData() {
  //   this.spinner.show();
  //   //let url = 'api/employee/is_employee_exists?employee_id=' + this.employee_id;
  //   let url = '../../assets/json/employee/editEmployee.json';
  //   this.cs.requestHttp('get', url).subscribe({
  //     next: (response: any) => {
  //       this.employee = response['data'].records;        
  //     },
  //     error: (err: any) => {
  //       this.spinner.hide();
  //       this.cs.handleError(err);
  //     },
  //     complete: () => {
  //       this.spinner.hide();
  //     },
  //   });
  // }

  setFormData() {
    let service_start_date = null;
    let service_end_date = null;
    let review_date = null;
    let lv_absence_start_date = null;
    let lv_absence_end_date = null;
    let lv_actual_return_to_work = null;

    if (this.employee['service'].service_start_date) {
      let date = this.employee['service'].service_start_date
        .split(' ')[0]
        .split('-');
      let fd = {
        month: parseInt(date[0]),
        day: parseInt(date[1]),
        year: parseInt(date[2]),
      };
      service_start_date = fd ? fd : null;
    }

    if (this.employee['service'].service_end_date) {
      let date = this.employee['service'].service_end_date
        .split(' ')[0]
        .split('-');
      let fd = {
        month: parseInt(date[0]),
        day: parseInt(date[1]),
        year: parseInt(date[2]),
      };
      service_end_date = fd ? fd : null;
    }

    if (this.employee['admin'].review_date) {
      let date = this.employee['admin'].review_date.split(' ')[0].split('-');
      let fd = {
        month: parseInt(date[0]),
        day: parseInt(date[1]),
        year: parseInt(date[2]),
      };
      review_date = fd ? fd : null;
    }

    if (this.employee['hr_status'].absence_start_date) {
      let date = this.employee['hr_status'].absence_start_date
        .split(' ')[0]
        .split('-');
      let fd = {
        month: parseInt(date[0]),
        day: parseInt(date[1]),
        year: parseInt(date[2]),
      };
      lv_absence_start_date = fd ? fd : null;
    }

    if (this.employee['hr_status'].absence_end_date) {
      let date = this.employee['hr_status'].absence_end_date
        .split(' ')[0]
        .split('-');
      let fd = {
        month: parseInt(date[0]),
        day: parseInt(date[1]),
        year: parseInt(date[2]),
      };
      lv_absence_end_date = fd ? fd : null;
    }

    if (this.employee['hr_status'].actual_return_to_work) {
      let date = this.employee['hr_status'].actual_return_to_work
        .split(' ')[0]
        .split('-');
      let fd = {
        month: parseInt(date[0]),
        day: parseInt(date[1]),
        year: parseInt(date[2]),
      };
      lv_actual_return_to_work = fd ? fd : null;
    }

    this.frm.patchValue({
      frmEmpD: {
        alternate_email: this.employee['employee'].alternate_email,
        admin_notes: this.employee['employee'].admin_notes,
      },
      frmHierarchy: {
        region: this.employee['hierarchy'].region_name,
        area_short_name: this.employee['hierarchy'].area_short_name,
      },
      frmManager: {
        manager_employee_id: this.employee['manager'].manager_employee_id,
      },
      frmEmpJob: {
        job_title: this.employee['employee_job_code'].job_title,
        job_id: this.employee['employee_job_code'].job_id,
        job_adp_code: this.employee['employee_job_code'].job_adp_code,
        job_type: this.employee['employee_job_code'].job_type,
      },
      frmService: {
        business_org: this.employee['service'].business_org,
        work_shift: this.employee['service'].work_shift,
        on_call: this.employee['service'].on_call,
        on_site: this.employee['service'].on_site,
        dedicated: this.employee['service'].dedicated,
        dedicated_to: this.employee['service'].dedicated_to,
        service_advantage: this.employee['service'].service_advantage,
        team_type: this.employee['service'].team_type,
        fs_status: this.employee['service'].fs_status == 'ACTIVE' ? 'Active' : 'Inactive',
        service_start_date: service_start_date,
        service_end_date: service_end_date,
        record_complete: this.employee['service'].record_complete,
      },

      frmHrStatus: {
        absence_start_date: lv_absence_start_date,
        absence_end_date: lv_absence_end_date,
        actual_return_to_work: lv_actual_return_to_work,
      },
      frmAdmin: {
        manager_flag: this.employee['admin'].manager_flag
          ? this.employee['admin'].manager_flag
          : 'N',
        review_date: review_date,
      },
    });
    this.get_dropdown_areas(this.frmHierarchy.value.region);

    if (this.employee['service'].team_status != 'ACTIVE') {
      this.frm.patchValue({
        frmService: {
          team_type: null,
        }
      });
    }
    if (this.employee['employee_job_code'].job_status != 'ACTIVE') {
      this.frm.patchValue({
        frmEmpJob: {
          job_id: null,
          job_title: null,
          job_adp_code: null,
          job_type: null,
        }
      });
    }
    if (this.employee['manager'].manager_flag != 'Y') {
      this.frm.patchValue({
        frmManager: {
          manager_employee_id: null,
        }
      });
    }
    if (this.employee['hierarchy'].area_status != 'ACTIVE') {
      this.frm.patchValue({
        frmHierarchy: {
          area_short_name: null,
        }
      });
    }
    if (this.employee['hierarchy'].region_status != 'ACTIVE') {
      this.frm.patchValue({
        frmHierarchy: {
          region: null,
        }
      });
    }
  }
  onSubmit() {
    if (this.frm.valid) {
      try {
        this.spinner.show();
        let cdate = this.frmChangeMain.value.change_effective_date;
        const ca = new Date(cdate.year + '-' + cdate.month + '-' + cdate.day);
        let cmonth = ('0' + (ca.getMonth() + 1)).slice(-2);
        let cday = ('0' + cdate.day).slice(-2);

        let ssdate = this.frmService.value.service_start_date;
        const ssa = new Date(
          ssdate.year + '-' + ssdate.month + '-' + ssdate.day
        );
        let ssmonth = ('0' + (ssa.getMonth() + 1)).slice(-2);
        let ssday = ('0' + ssdate.day).slice(-2);

        let sedate = this.frmService.value.service_end_date;
        let lv_service_end_Date;
        if (sedate) {
          const sea = new Date(
            sedate.year + '-' + sedate.month + '-' + sedate.day
          );
          let semonth = ('0' + (sea.getMonth() + 1)).slice(-2);
          let seday = ('0' + sedate.day).slice(-2);
          lv_service_end_Date = sedate.year + '-' + semonth + '-' + seday;
        }

        let rdate = this.frmAdmin.value.review_date;
        let lv_rdate;
        if (rdate) {
          const ra = new Date(rdate.year + '-' + rdate.month + '-' + rdate.day);
          let rmonth = ('0' + (ra.getMonth() + 1)).slice(-2);
          let rday = ('0' + rdate.day).slice(-2);
          lv_rdate = rdate.year + '-' + rmonth + '-' + rday;
        }

        let absence_start_date = this.frmHrStatus.value.absence_start_date;
        let lv_absence_start_date;
        if (absence_start_date) {
          const a_s_ra = new Date(
            absence_start_date.year +
            '-' +
            absence_start_date.month +
            '-' +
            absence_start_date.day
          );
          let a_s_month = ('0' + (a_s_ra.getMonth() + 1)).slice(-2);
          let a_s_day = ('0' + absence_start_date.day).slice(-2);
          lv_absence_start_date =
            absence_start_date.year + '-' + a_s_month + '-' + a_s_day;
        }

        let absence_end_date = this.frmHrStatus.value.absence_end_date;
        let lv_absence_end_date;
        if (absence_end_date) {
          const a_e_ra = new Date(
            absence_end_date.year +
            '-' +
            absence_end_date.month +
            '-' +
            absence_end_date.day
          );
          let a_e_month = ('0' + (a_e_ra.getMonth() + 1)).slice(-2);
          let a_e_day = ('0' + absence_end_date.day).slice(-2);
          lv_absence_end_date =
            absence_end_date.year + '-' + a_e_month + '-' + a_e_day;
        }

        let actual_return_to_work = this.frmHrStatus.value.actual_return_to_work;
        let lv_actual_return_to_work;
        if (actual_return_to_work) {
          const a_r_ra = new Date(
            actual_return_to_work.year +
            '-' +
            actual_return_to_work.month +
            '-' +
            actual_return_to_work.day
          );
          let a_r_month = ('0' + (a_r_ra.getMonth() + 1)).slice(-2);
          let a_r_day = ('0' + actual_return_to_work.day).slice(-2);
          lv_actual_return_to_work =
            actual_return_to_work.year + '-' + a_r_month + '-' + a_r_day;
        }

        let obj = {
          change_effective_date: cdate.year + '-' + cmonth + '-' + cday,
          change_note: this.frmChangeMain.value.change_note,
          alternate_email: this.frmEmpD.value.alternate_email,
          admin_notes: this.frmEmpD.value.admin_notes,
          region: this.frmHierarchy.value.region,
          area: this.frmHierarchy.value.area_short_name,
          manager_id: this.frmManager.value.manager_employee_id,
          loc_code: null,
          job_adp: this.frmEmpJob.value.job_adp_code,
          job_title: this.frmEmpJob.value.job_title,
          job_type: this.frmEmpJob.value.job_type,
          business_org: this.frmService.value.business_org,
          dedicated: this.frmService.value.dedicated,
          dedicated_to: this.frmService.value.dedicated_to,
          on_call: this.frmService.value.on_call,
          on_site: this.frmService.value.on_site,
          service_advantage: this.frmService.value.service_advantage,
          service_start_date: ssdate.year + '-' + ssmonth + '-' + ssday,
          service_end_date: lv_service_end_Date,
          team_type: this.frmService.value.team_type,
          work_shift: this.frmService.value.work_shift,
          fs_status: this.frmService.value.fs_status,
          record_complete: this.frmService.value.record_complete,
          review_date: lv_rdate,
          manager_flag: this.frmAdmin.value.manager_flag,
          absence_start_date: lv_absence_start_date,
          absence_end_date: lv_absence_end_date,
          actual_return_to_work: lv_actual_return_to_work,
          change_type: 'ADD',
          change_status: 'Pending',
          approval_required: 'N',
          approved: 'N',
        };

        console.log(obj)

        let url = 'api/employee/add-employee/' + this.frmEmpD.value.employeeId;
        this.cs.requestHttp('put', url, obj, false).subscribe({
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
      } catch (error) {
        this.spinner.hide();
        console.log(error);
      }
    }
  }
  isHierarchySync: boolean = false;
  isJobSync: boolean = false;
  isManagerSync: boolean = false;

  private searchText$ = new Subject<string>();

  search(searchTxt: string) {
    this.searchText$.next(searchTxt);
  }


  regionChanged() {
    this.spinner.show();
    let url =
      'api/config/area/get?region_name=' +
      this.frmHierarchy.value.region +
      '&status=ACTIVE';
    this.cs.requestHttp('get', url).subscribe({
      next: (response: any) => {
        this.areaList = response['data'].records;
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

  get controlName(): AbstractControl | null {
    return this.frmService.get('dedicated_to');
  }

  onSelectValue() {
    if (
      (this.frmService.value.dedicated != null && this.frmService.value.dedicated != 'N')
      // ||
      // (this.frmService.value.on_site != null && this.frmService.value.on_site != 'N')
    ) {
      this.controlName?.setValidators(Validators.required);
      this.controlName?.updateValueAndValidity();
      this.isDedicatedTo = true;
    } else {
      this.controlName?.setValidators(null);
      this.controlName?.updateValueAndValidity();
      this.isDedicatedTo = false;
    }
  }

  displayDetail(e: any, id: any) {
    console.log(e);

    $('.list-group .list-group-item').removeClass('active');
    $(e.target).addClass('active');
    let containerAccordion = document.getElementById('containerAccordion');
    let scrollElement = document.getElementById(id);
    let topPos = scrollElement?.offsetTop;

    if (topPos != undefined) {
      if (containerAccordion != null)
        containerAccordion.scrollTop = topPos - 133;
    }
  }

  regionDoRemove() { }

  clearDateField(getField: String) {
    switch (getField) {
      case 'absence_start_date':
        {
          this.frmHrStatus.patchValue({ absence_start_date: null })
          break;
        }
      case 'absence_end_date':
        {
          this.frmHrStatus.patchValue({ absence_end_date: null })
          break;
        }
      case 'actual_return_to_work':
        {
          this.frmHrStatus.patchValue({ actual_return_to_work: null })
          break;
        }
      case 'service_end_date':
        {
          this.frmService.patchValue({ service_end_date: null })
          break;
        }
      case 'review_date':
        {
          this.frmAdmin.patchValue({ review_date: null })
          break;
        }
      default:
        {
          break;
        }
    }
  }

  ngOnDestroy() {
    this.config.minDate != null;
  }
}
