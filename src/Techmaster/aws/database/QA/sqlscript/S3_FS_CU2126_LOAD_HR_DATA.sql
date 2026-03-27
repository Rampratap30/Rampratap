LOAD DATA FROM S3 's3://rac-aws-techmaster-non-prod/QA/HR.csv'
    INTO TABLE RAC_HR_TM_EMPLOYEE_DTLS 
		FIELDS TERMINATED BY ',' 
		ENCLOSED BY '"' 
		LINES TERMINATED BY '\n' 
		IGNORE 1 LINES 
    (EMPLOYEE_ID,EMPLOYEE_NAME,EMAIL,RESOURCE_NUMBER,CONTINGENT_WORKER,HR_STATUS,LAST_HIRE_DATE,JOB_TITLE,JOB_FAMILY,JOB_CODE,JOB_ADP,ACTUAL_TERMINATION_DATE,MANAGER_EMPLOYEE_ID,MANAGER_NAME,REGION,AREA_SHORT,LOCATION_CODE,EBS_USER_NAME,ZIP_CODE);

update RAC_HR_TM_EMPLOYEE_DTLS
set actual_termination_date=null
where actual_termination_date='0000-00-00 00:00:00'

commit;
    
LOAD DATA FROM S3 's3://rac-aws-techmaster-non-prod/QA/Region.csv'
    INTO TABLE RAC_FS_TM_REGION
		FIELDS TERMINATED BY ',' 
		ENCLOSED BY '"' 
		LINES TERMINATED BY '\n' 
		IGNORE 1 LINES 
    (region_id,region_name,region_short_name,region_dir_emp_id,status);



LOAD DATA FROM S3 's3://rac-aws-techmaster-non-prod/QA/Area.csv'
    INTO TABLE RAC_FS_TM_AREA 
		FIELDS TERMINATED BY ',' 
		ENCLOSED BY '"' 
		LINES TERMINATED BY '\n' 
		IGNORE 1 LINES 
    (area_id,region_id,area_short_name,area_dir_emp_id,area_fom_emp_id,status);

LOAD DATA FROM S3 's3://rac-aws-techmaster-non-prod/QA/Job.csv'
    INTO TABLE RAC_FS_TM_JOB_CODE 
		FIELDS TERMINATED BY ',' 
		ENCLOSED BY '"' 
		LINES TERMINATED BY '\n' 
		IGNORE 1 LINES 
    (job_id,job_code,job_title,job_type,job_adp_code,status);
	
 
LOAD DATA FROM S3 's3://rac-aws-techmaster-non-prod/QA/TM.csv'
    INTO TABLE RAC_FS_TM_EMPLOYEE_DTLS 
		FIELDS TERMINATED BY ',' 
		ENCLOSED BY '"' 
		LINES TERMINATED BY '\n' 
		IGNORE 1 LINES 
    (EMPLOYEE_ID,AREA_ID,JOB_ID,ALTERNATE_EMAIL,MANAGER_ID,LOCATION_CODE,FS_STATUS,MANAGER_FLAG,RECORD_COMPLETE);
	
