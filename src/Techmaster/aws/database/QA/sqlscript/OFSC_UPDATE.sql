update RAC_FS_TM_EMPLOYEE_DTLS dt
set alternate_email=
(select distinct alternate_email from RAC_FS_TM_OFSC_DTLS of inner join RAC_HR_TM_EMPLOYEE_DTLS hr 
on of.resource_number=hr.resource_number
where  dt.employee_id=hr.employee_id);


update RAC_FS_TM_EMPLOYEE_DTLS dt
set ofsc_last_login=
(select distinct last_login from RAC_FS_TM_OFSC_DTLS of inner join RAC_HR_TM_EMPLOYEE_DTLS hr 
on of.resource_number=hr.resource_number
where  dt.employee_id=hr.employee_id);

update RAC_FS_TM_EMPLOYEE_DTLS dt
set production_print=
(select distinct production_print from RAC_FS_TM_OFSC_DTLS of inner join RAC_HR_TM_EMPLOYEE_DTLS hr 
on of.resource_number=hr.resource_number
where  dt.employee_id=hr.employee_id);

update RAC_FS_TM_EMPLOYEE_DTLS dt
set ofsc_status=
(select distinct status from RAC_FS_TM_OFSC_DTLS of inner join RAC_HR_TM_EMPLOYEE_DTLS hr 
on of.resource_number=hr.resource_number
where  dt.employee_id=hr.employee_id);

commit;