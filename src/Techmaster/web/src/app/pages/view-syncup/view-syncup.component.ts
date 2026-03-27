import { Component } from '@angular/core';
import { AbstractControl, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { NgbDatepickerConfig } from '@ng-bootstrap/ng-bootstrap';
import { ToastrService } from 'ngx-toastr';
import { CoreService } from 'src/app/service/core.service';
import { ActivatedRoute, Router } from '@angular/router';
import { NgxSpinnerService } from 'ngx-spinner';
import { Subject, debounceTime, distinctUntilChanged, switchMap } from 'rxjs';
import { diff } from 'deep-object-diff';

@Component({
  selector: 'app-view-syncup',
  templateUrl: './view-syncup.component.html',
  styleUrls: ['./view-syncup.component.css']
})
export class ViewSyncupComponent {
  isDedicatedTo: boolean = false;
  constructor(
    private toastr: ToastrService,
    private cs: CoreService,
    private fb: FormBuilder,
    private activatedRoute: ActivatedRoute,
    private spinner: NgxSpinnerService,
    private config: NgbDatepickerConfig,
    private router: Router
  ) {
    const current = new Date();
    config.minDate = {
      month: current.getMonth() + 1,
      day: current.getDate(),
      year: current.getFullYear(),
    };

    config.outsideDays = 'hidden';
  }

  frm!: FormGroup;
  frmChangeMain!: FormGroup;
  frmEmpD!: FormGroup;
  frmHierarchy!: FormGroup;
  frmManager!: FormGroup;
  frmEmpJob!: FormGroup;
  frmService!: FormGroup;
  frmHrStatus!: FormGroup;
  frmAdmin!: FormGroup;
  change_id!: String;
  employee_id!: String;
  retriveValues: boolean = false;

  summaryRegion: boolean = false;
  summaryASN: boolean = false;
  summaryManagerEMPId: boolean = false;
  summaryJobADPCode: boolean = false;
  summaryBO: boolean = false;
  summaryJobType: boolean = false;
  summaryTeamType: boolean = false;
  summaryWS: boolean = false;
  summaryOnCall: boolean = false;
  summaryOnSite: boolean = false;
  summaryDedicated: boolean = false;
  summaryDedicatedTo: boolean = false;
  summarySA: boolean = false;
  summaryFSStatus: boolean = false;
  summarySSD: boolean = false;
  summarySED: boolean = false;
  summaryRC: boolean = false;
  summaryARTD: boolean = false;
  summaryHRStatus: boolean = false;
  summaryASD: boolean = false;
  summaryAED: boolean = false;
  summaryARTW: boolean = false;
  summaryLHD: boolean = false;
  summaryManagerFlag: boolean = false;
  pre_change_id!: String;

  get f() {
    return this.frm.controls;
  }
  responseData: any;
  employee: any;

  teamtypeList: any[] = [];
  regionList: any[] = [];
  areaList: any[] = [];
  locationList: any[] = [];
  managerList: any[] = [];
  jobCodeList: any[] = [];

  getRole: String | undefined;
  user_id: String | undefined;

  selectItems = this.cs.selectItems;
  selectActive = this.cs.selectActive;
  workShiftDropDown = this.cs.workShiftDropDown;
  onSiteDropDown = this.cs.onSiteDropDown;


  ngOnInit(): void {
    this.isDedicatedTo = false;
    if (!this.cs.getRole) {
      this.cs.obsGetUserInfo?.subscribe((data) => {
        this.getRole = data?.data?.userRole;
        this.user_id = data?.data?.user_id;
      });
    } else {
      this.getRole = this.cs.getRole;
      this.user_id = this.cs.user_id;
    }
    this.activatedRoute.paramMap.subscribe((params) => {
      this.change_id = atob(String(params.get('changeId')));
      this.employee_id = atob(String(params.get('employeeId')));
    });

    this.frmChangeMain = this.fb.group({
      change_note: ['', Validators.required],
      change_effective_date: ['', Validators.required],
    });

    this.frmEmpD = this.fb.group({
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

    this.get_dropdown_manager();
    this.get_dropdown_regions();
    this.get_dropdown_teamtype();
    this.get_dropdown_jobCode();
    this.getData();
  }
  get_dropdown_manager() {
    let url = '/api/home/get_manager_list?is_export_all=Y';
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
  get_dropdown_areas(value: any) {
    let url = 'api/config/area/get?region_name=' + value + '&status=ACTIVE';
    this.cs.requestHttp('get', url).subscribe({
      next: (response: any) => {
        this.areaList = response['data'].records;
      },
      error: (err: any) => {
        this.cs.handleError(err);
      },
    });
  }

  get_dropdown_teamtype() {
    let url = 'api/config/team-type/get?is_export_all=Y&status=ACTIVE';
    this.cs.requestHttp('get', url).subscribe({
      next: (response: any) => {
        this.teamtypeList = response['data'].records;
      },
      error: (err: any) => {
        this.cs.handleError(err);
      },
    });
  }

  get_dropdown_jobCode() {
    let url = 'api/config/job-code/get?is_export_all=Y&status=ACTIVE&order_by=JOB_TITLE&order=asc';
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
      this.frmEmpJob.patchValue({
        job_title: selectedrow[0].job_title,
        job_adp_code: selectedrow[0].job_adp_code,
        job_type: selectedrow[0].job_type,
      });
      console.log(selectedrow);
    }
  }
  doRemove(event: any) {
    this.frmEmpJob.patchValue({
      job_title: this.responseData['employee_job_code'].job_title,
      job_adp_code: this.responseData['employee_job_code'].job_adp_code,
      job_id: this.responseData['employee_job_code'].job_id,
      job_type: this.responseData['employee_job_code'].job_type,
    });
  }


  getEmployeeData() {
    let url = 'api/employee/get?employee_id=' + this.employee_id;
    this.spinner.show();
    this.cs.requestHttp('GET', url).subscribe({
      next: (response: any) => {
        this.employee = response?.data?.records;
      },
      error: (err: any) => {
        this.spinner.hide();
        this.cs.handleError(err);
      },
      complete: () => {
        this.changeSummary();
        this.onSelectValue();
        this.spinner.hide();
      },
    });
  }
  getData() {
    let url = 'api/changes/change-info?change_id=' + this.change_id;
    this.spinner.show();
    this.cs.requestHttp('get', url).subscribe({
      next: (response: any) => {
        this.responseData = response['data'].records;

        let service_start_date = null;
        let service_end_date = null;
        let review_date = null;
        let lv_change_effective_date = null;
        let lv_absence_start_date = null;
        let lv_absence_end_date = null;
        let lv_actual_return_to_work = null;

        if (this.responseData['change_system'].change_effective_date) {
          let date = this.responseData['change_system'].change_effective_date
            .split(' ')[0]
            .split('-');
          let fd = {
            month: parseInt(date[0]),
            day: parseInt(date[1]),
            year: parseInt(date[2]),
          };
          lv_change_effective_date = fd ? fd : null;
        }

        if (this.responseData['service'].service_start_date) {
          let date = this.responseData['service'].service_start_date
            .split(' ')[0]
            .split('-');
          let fd = {
            month: parseInt(date[0]),
            day: parseInt(date[1]),
            year: parseInt(date[2]),
          };
          service_start_date = fd ? fd : null;
        }

        if (this.responseData['service'].service_end_date) {
          let date = this.responseData['service'].service_end_date
            .split(' ')[0]
            .split('-');
          let fd = {
            month: parseInt(date[0]),
            day: parseInt(date[1]),
            year: parseInt(date[2]),
          };
          service_end_date = fd ? fd : null;
        }

        if (this.responseData['admin'].review_date) {
          let date = this.responseData['admin'].review_date
            .split(' ')[0]
            .split('-');
          let fd = {
            month: parseInt(date[0]),
            day: parseInt(date[1]),
            year: parseInt(date[2]),
          };
          review_date = fd ? fd : null;
        }

        if (this.responseData['hr_status'].absence_start_date) {
          let date = this.responseData['hr_status'].absence_start_date
            .split(' ')[0]
            .split('-');
          let fd = {
            month: parseInt(date[0]),
            day: parseInt(date[1]),
            year: parseInt(date[2]),
          };
          lv_absence_start_date = fd ? fd : null;
        }

        if (this.responseData['hr_status'].absence_end_date) {
          let date = this.responseData['hr_status'].absence_end_date
            .split(' ')[0]
            .split('-');
          let fd = {
            month: parseInt(date[0]),
            day: parseInt(date[1]),
            year: parseInt(date[2]),
          };
          lv_absence_end_date = fd ? fd : null;
        }

        if (this.responseData['hr_status'].actual_return_to_work) {
          let date = this.responseData['hr_status'].actual_return_to_work
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
          frmChangeMain: {
            change_id: this.responseData['change_system'].change_id,
            change_note: this.responseData['change_system'].change_note,
            change_effective_date: lv_change_effective_date,
          },
          frmEmpD: {
            admin_notes: this.responseData['employee'].admin_notes,
          },
          frmHierarchy: {
            region: this.responseData['hierarchy'].region_name,
            area_short_name: this.responseData['hierarchy'].area_short_name,
          },
          frmManager: {
            manager_employee_id: this.responseData['manager'].manager_employee_id,
          },
          frmEmpJob: {
            job_id: this.responseData['employee_job_code'].job_id,
            job_title: this.responseData['employee_job_code'].job_title,
            job_adp_code: this.responseData['employee_job_code'].job_adp_code,
            job_type: this.responseData['employee_job_code'].job_type,
          },
          frmService: {
            business_org: this.responseData['service'].business_org,
            work_shift: this.responseData['service'].work_shift,
            on_call: this.responseData['service'].on_call,
            on_site: this.responseData['service'].on_site,
            dedicated: this.responseData['service'].dedicated,
            dedicated_to: this.responseData['service'].dedicated_to,
            service_advantage: this.responseData['service'].service_advantage,
            team_type: this.responseData['service'].team_type,
            fs_status: this.responseData['service'].fs_status,
            service_start_date: service_start_date,
            service_end_date: service_end_date,
            record_complete: this.responseData['service'].record_complete,
          },
          frmHrStatus: {
            absence_start_date: lv_absence_start_date,
            absence_end_date: lv_absence_end_date,
            actual_return_to_work: lv_actual_return_to_work,
          },
          frmAdmin: {
            manager_flag: this.responseData['admin'].manager_flag,
            review_date: review_date,
          },
        });

        this.get_dropdown_areas(this.frmHierarchy.value.region);

        if (this.responseData['change_system'].change_status == "Processed") {
          this.pre_change_id = ""
          let url = 'api/changes/pre-change-id?change_id=' + this.change_id + '&employee_id=' + this.employee_id;
          this.spinner.show();
          this.cs.requestHttp('GET', url).subscribe({
            next: (response: any) => {
              this.pre_change_id = response?.data?.records?.change_id;
            },
            error: (err: any) => {
              this.spinner.hide();
              this.cs.handleError(err);
            },
            complete: () => {
              if (this.pre_change_id != "") {
                let url = 'api/changes/change-info?change_id=' + this.pre_change_id;
                this.spinner.show();
                this.cs.requestHttp('GET', url).subscribe({
                  next: (response: any) => {
                    this.employee = response?.data?.records;
                  },
                  error: (err: any) => {
                    this.spinner.hide();
                    this.cs.handleError(err);
                  },
                  complete: () => {
                    this.changeSummary();
                    this.onSelectValue();
                    this.spinner.hide();
                  },
                });

              }
              else {
                this.getEmployeeData();
              }

              this.spinner.hide();
            },
          });
        }
        else {

          this.getEmployeeData();
          // if (this.responseData['service'].team_status != 'ACTIVE') {
          //   this.frm.patchValue({
          //     frmService: {
          //       team_type: null,
          //     }
          //   });
          // }
          // if (this.responseData['employee_job_code'].job_status != 'ACTIVE') {
          //   this.frm.patchValue({
          //     frmEmpJob: {
          //       job_id: null,
          //       job_title: null,
          //       job_adp_code: null,
          //       job_type: null,
          //     }
          //   });
          // }
          // if (this.responseData['manager'].manager_flag != 'Y') {
          //   this.frm.patchValue({
          //     frmManager: {
          //       manager_employee_id: null,
          //     }
          //   });
          // }
          // if (this.responseData['hierarchy'].area_status != 'ACTIVE') {
          //   this.frm.patchValue({
          //     frmHierarchy: {
          //       area_short_name: null,
          //     }
          //   });
          // }
          // if (this.responseData['hierarchy'].region_status != 'ACTIVE') {
          //   this.frm.patchValue({
          //     frmHierarchy: {
          //       region: null,
          //     }
          //   });
          // }

        }

      },
      error: (err: any) => {
        this.spinner.hide();
        this.cs.handleError(err);
      },
      complete: () => {
        setTimeout(() => {
          this.spinner.hide();
        }, 3000);

      },
    });
  }

  changeSummary() {
    try {
      let comparisonRecords: any;
      comparisonRecords = diff(this.employee, this.responseData);
      if (comparisonRecords['hierarchy'] && 'region_name' in comparisonRecords['hierarchy']) this.summaryRegion = true;
      if (comparisonRecords['hierarchy'] && 'area_short_name' in comparisonRecords['hierarchy']) this.summaryASN = true;
      if (comparisonRecords['manager'] && 'manager_employee_id' in comparisonRecords['manager']) this.summaryManagerEMPId = true;
      if (comparisonRecords['employee_job_code'] && 'job_adp_code' in comparisonRecords['employee_job_code']) this.summaryJobADPCode = true;

      if (comparisonRecords['service']) {
        if ('business_org' in comparisonRecords['service']) this.summaryBO = true;
        if ('team_type' in comparisonRecords['service']) this.summaryTeamType = true;
        if ('work_shift' in comparisonRecords['service']) this.summaryWS = true;
        if ('on_call' in comparisonRecords['service']) this.summaryOnCall = true;
        if ('on_site' in comparisonRecords['service']) this.summaryOnSite = true;
        if ('dedicated' in comparisonRecords['service']) this.summaryDedicated = true;
        if ('dedicated_to' in comparisonRecords['service']) this.summaryDedicatedTo = true;
        if ('service_advantage' in comparisonRecords['service']) this.summarySA = true;
        if ('fs_status' in comparisonRecords['service']) this.summaryFSStatus = true;
        if ('service_start_date' in comparisonRecords['service']) this.summarySSD = true;
        if ('service_end_date' in comparisonRecords['service']) this.summarySED = true;
        if ('record_complete' in comparisonRecords['service']) this.summaryRC = true;
      }

      if (comparisonRecords['admin']) {
        if ('manager_flag' in comparisonRecords['admin']) this.summaryManagerFlag = true;
      }

      if (comparisonRecords['hr_status']) {
        if ('absence_start_date' in comparisonRecords['hr_status']) this.summaryASD = true;
        if ('absence_end_date' in comparisonRecords['hr_status']) this.summaryAED = true;
        if ('actual_return_to_work' in comparisonRecords['hr_status']) this.summaryARTW = true;
      }

    } catch (error) {
      console.log(error);
    }
  }


  onSubmit() {
    if (this.frm.valid) {
      this.spinner.show();

      let cdate = this.frmChangeMain.value.change_effective_date;
      let lv_cdate;
      if (cdate) {
        const ca = new Date(cdate.year + '-' + cdate.month + '-' + cdate.day);
        let cmonth = ('0' + (ca.getMonth() + 1)).slice(-2);
        let cday = ('0' + (cdate.day)).slice(-2);
        lv_cdate = cdate.year + '-' + cmonth + '-' + cday;
      }

      let ssdate = this.frmService.value.service_start_date;
      let lv_ssdate;
      if (ssdate) {
        const ssa = new Date(
          ssdate.year + '-' + ssdate.month + '-' + ssdate.day
        );
        let ssmonth = ('0' + (ssa.getMonth() + 1)).slice(-2);
        let ssday = ('0' + (ssdate.day)).slice(-2);
        lv_ssdate = ssdate.year + '-' + ssmonth + '-' + ssday;
      }

      let sedate = this.frmService.value.service_end_date;
      let lv_sedate;
      if (sedate) {
        const sea = new Date(
          sedate.year + '-' + sedate.month + '-' + sedate.day
        );
        let semonth = ('0' + (sea.getMonth() + 1)).slice(-2);
        let seday = ('0' + (sedate.day)).slice(-2);
        lv_sedate = sedate.year + '-' + semonth + '-' + seday;
      }

      let rdate = this.frmAdmin.value.review_date;
      let lv_rdate;
      if (rdate) {
        const ra = new Date(rdate.year + '-' + rdate.month + '-' + rdate.day);
        let rmonth = ('0' + (ra.getMonth() + 1)).slice(-2);
        let rday = ('0' + (rdate.day)).slice(-2);
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
        change_effective_date: lv_cdate,
        change_note: this.frmChangeMain.value.change_note,
        alternate_email: this.frmEmpD.value.alternate_email,
        admin_notes: this.frmEmpD.value.admin_notes,
        region: this.frmHierarchy.value.region,
        area_short_name: this.frmHierarchy.value.area_short_name,
        manager_id: this.frmManager.value.manager_employee_id,
        loc_code: '',
        job_adp: this.frmEmpJob.value.job_adp_code,
        job_title: this.frmEmpJob.value.job_title,
        job_type: this.frmEmpJob.value.job_title,
        cip: this.employee["service"].cip,
        contingent_worker: this.employee["service"].contingent_worker,
        business_org: this.frmService.value.business_org,
        team_type: this.frmService.value.team_type,
        work_shift: this.frmService.value.work_shift,
        fs_status: this.frmService.value.fs_status,
        dedicated: this.frmService.value.dedicated,
        dedicated_to: this.frmService.value.dedicated_to,
        on_call: this.frmService.value.on_call,
        on_site: this.frmService.value.on_site,

        record_complete: this.frmService.value.record_complete,
        service_advantage: this.frmService.value.service_advantage,
        service_start_date: lv_ssdate,
        service_end_date: lv_sedate,

        manager_flag: this.frmAdmin.value.manager_flag,
        review_date: lv_rdate,
        absence_start_date: lv_absence_start_date,
        absence_end_date: lv_absence_end_date,
        actual_return_to_work: lv_actual_return_to_work,
        change_type: 'UPDATE',
        change_status: 'Pending',
        approval_required: 'N',
        approved: 'N',

      };
      let url = 'api/changes/update/' + this.change_id;
      this.cs.requestHttp('PUT', url, obj, false).subscribe({
        next: (response: any) => {
          this.spinner.hide();
          this.toastr.success(response.data.message);

        },
        error: (err: any) => {
          this.spinner.hide();
          this.cs.handleError(err);
        },
      });
    }
  }
  onApprove() {
    if (confirm('Are you sure you want to Approve this data?')) {
      let url = 'api/changes/bulk-approved';
      let obj = { change_id: [this.change_id] };
      this.cs.requestHttp('put', url, obj, false).subscribe({
        next: (response: any) => {
          this.toastr.success(response.data.message);
          this.router.navigate(['changes']);
        },
        error: (err: any) => {
          this.cs.handleError(err);
        },
      });
    }
  }

  onReject() {
    if (confirm('Are you sure you want to Reject this data?')) {
      let url = 'api/changes/bulk-rejected';
      let obj = { change_id: [this.change_id] };
      this.cs.requestHttp('put', url, obj, false).subscribe({
        next: (response: any) => {
          this.toastr.success(response.data.message);
          this.router.navigate(['changes']);
        },
        error: (err: any) => {
          this.cs.handleError(err);
        },
      });
    }
  }

  clearData() {
    this.frm.reset();
  }

  onCancel() {
    this.retriveValues = true;
    localStorage.setItem("retriveValues", JSON.stringify(this.retriveValues));
    this.router.navigate(['changes']);
  }

  onSearchSubmit() { }
  private searchText$ = new Subject<string>();

  search(searchTxt: string) {
    this.searchText$.next(searchTxt);
  }

  getLocationCode(event: any) {
    console.log(event)
    this.searchText$.pipe(
      debounceTime(300),
      distinctUntilChanged(),
      switchMap(searchTxt =>
        this.searchLocationcode(searchTxt))
    ).subscribe({
      next: (response: any) => {
        this.locationList = response['data'].records;
      },
      error: (err: any) => {
        this.cs.handleError(err);
      },
    });
  }

  searchLocationcode(term: any) {
    console.log(term)
    let url =
      'api/config/location/get?location_name=' + term;
    return this.cs.requestHttp('get', url);
  }

  regionChanged() {
    this.spinner.show();
    let url = 'api/config/area/get?region_name=' + this.frmHierarchy.value.region + '&status=ACTIVE';
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

  displayDetail(e: any, id: any) {
    let targetComponentId;

    $('.list-group .list-group-item').removeClass('active');
    (e.target.getAttribute('data-rac-parent-id')) ? targetComponentId = e.target.getAttribute('data-rac-parent-id') : targetComponentId = e.target.id;
    $('#' + targetComponentId).addClass('active');
    let containerAccordion = document.getElementById('containerAccordion');
    let scrollElement = document.getElementById(id);
    let topPos = scrollElement?.offsetTop;

    if (topPos != undefined) {
      if (containerAccordion != null)
        containerAccordion.scrollTop = topPos - 133;
    }
  }

  regionDoRemove() {

  }

  onSelectManager() {
    this.spinner.show();
    let url = 'api/employee/is_employee_as_manager?employee_id=' + this.employee["employee"].employee_id;
    this.cs.requestHttp('get', url).subscribe({
      next: (response: any) => {
        if (response?.data?.count > 0) {
          this.frm.patchValue({
            frmAdmin: {
              manager_flag: this.employee['admin'].manager_flag
                ? this.employee['admin'].manager_flag
                : 'N',
            }
          })
          this.toastr.success("User can't update the manager flag.");
        }
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

  ngOnDestroy() {
    this.config.minDate != null;
  }
}
