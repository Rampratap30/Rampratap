DELIMITER //
CREATE PROCEDURE `RAC_FS_TM_EMP_SYNC_OFSC_DATA_PROCEDURE`()
BEGIN

DECLARE finished                	INTEGER DEFAULT 0;
DECLARE v_change_id                	INTEGER DEFAULT 0;
DECLARE v_employee_id               BIGINT(60)  DEFAULT 0;
DECLARE v_alternate_email           VARCHAR(400);
DECLARE v_employee_name             VARCHAR(400);
DECLARE v_fs_alternate_email        VARCHAR(400);
DECLARE v_status                    VARCHAR(100);
DECLARE v_production_print          VARCHAR(100);
DECLARE v_job_title                 VARCHAR(400);
DECLARE v_job_adp                   VARCHAR(400);
DECLARE v_job_type                  VARCHAR(400);
DECLARE v_team_type                 VARCHAR(400);
DECLARE v_manager_id                BIGINT(60);
DECLARE v_manager_flag              VARCHAR(400); 
DECLARE v_service_start_date        TIMESTAMP;
DECLARE v_service_end_date          TIMESTAMP;
DECLARE v_absence_start_date        TIMESTAMP;
DECLARE v_absence_end_date          TIMESTAMP;
DECLARE v_actual_return_to_work     TIMESTAMP;
DECLARE v_work_shift                VARCHAR(400);
DECLARE v_cip                       VARCHAR(400);
DECLARE v_business_org              VARCHAR(400);
DECLARE v_on_call                   VARCHAR(400);
DECLARE v_on_site                   VARCHAR(400);
DECLARE v_service_advantage         VARCHAR(400);
DECLARE v_dedicated                 VARCHAR(400);
DECLARE v_dedicated_to              VARCHAR(400);
DECLARE v_area                      VARCHAR(400);
DECLARE v_region                    VARCHAR(400);
DECLARE v_fs_status                 VARCHAR(400);
DECLARE v_hr_status                 VARCHAR(400);
DECLARE v_review_date               TIMESTAMP;
DECLARE v_record_complete           VARCHAR(10);
DECLARE v_approval_required         VARCHAR(10);
DECLARE v_csa_notif_flag            VARCHAR(10);
DECLARE v_change_status				VARCHAR(50);

#fetch ofsc records whose values for ofsc status,alternate email or print production is updated
DECLARE ofscEmployee 
   CURSOR FOR 
      SELECT 
		fs.employee_id,
        fs.employee_name,
		ofsc.alternate_email,
		fs.alternate_email,
		ofsc.status,
		ofsc.production_print,
		/****other values of change type****/
		(select job.job_title from RAC_FS_TM_JOB_CODE job where job.job_id= fs.job_id) job_title,
		(select job.job_adp_code from RAC_FS_TM_JOB_CODE job where job.job_id= fs.job_id) job_adp,
		(select job.job_type from RAC_FS_TM_JOB_CODE job where job.job_id= fs.job_id) job_type,
		(select team.team_type_name from RAC_FS_TM_TEAM_TYPE team where team.team_type_id= fs.team_type_id) team_type,
		fs.manager_id,
		fs.manager_flag,
		fs.service_start_date,
		fs.service_end_date,
		fs.absence_start_date,
		fs.absence_end_date,
		fs.actual_return_to_work,
		fs.work_shift,
		fs.cip,
		fs.business_org,
		fs.on_call,
		fs.on_site,
		fs.service_advantage,
		fs.dedicated,
		fs.dedicated_to,
		(select area.area_short_name from RAC_FS_TM_AREA area where area.area_id= fs.area_id) area,
		(select region.region_name from RAC_FS_TM_AREA area,RAC_FS_TM_REGION region where area.area_id= fs.area_id
		and area.region_id= region.region_id) region,
		fs.fs_status,
		hr.hr_status,
        fs.review_date,
        fs.record_complete
		FROM  RAC_FS_TM_OFSC_DTLS ofsc,RAC_FS_TM_EMPLOYEE_DTLS fs,RAC_HR_TM_EMPLOYEE_DTLS hr
		WHERE hr.employee_id = fs.employee_id
		AND ofsc.resource_number = hr.resource_number
		# AND upper(FS_STATUS) = 'ACTIVE'
		and ofsc.RESOURCE_NUMBER not like '%T%'
		AND (COALESCE(ofsc.alternate_email,'X') != COALESCE(fs.alternate_email,'X') 
		     OR COALESCE(ofsc.status,'INACTIVE') != COALESCE(fs.ofsc_status,'INACTIVE' )
			 OR COALESCE(ofsc.production_print,'N') != COALESCE(fs.production_print,'N')) ;
		
DECLARE CONTINUE HANDLER 
        FOR NOT FOUND SET finished = 1;

	
	/*opening cursor of new employees*/
	OPEN ofscEmployee;
    
    
	/*looping cursor of new employees*/
    getofscEmployeeDetails: LOOP
		
		/*fetching new employees data in variables*/
		FETCH ofscEmployee 
		INTO v_employee_id,
        v_employee_name,
		v_alternate_email,
		v_fs_alternate_email,
		v_status,
		v_production_print,
		v_job_title             ,
		v_job_adp               ,
		v_job_type              ,
		v_team_type             ,
		v_manager_id            ,
		v_manager_flag          ,
		v_service_start_date    ,
		v_service_end_date      ,
		v_absence_start_date    ,
		v_absence_end_date      ,
		v_actual_return_to_work ,
		v_work_shift            ,
		v_cip                   ,
		v_business_org          ,
		v_on_call               ,
		v_on_site               ,
		v_service_advantage     ,
		v_dedicated             ,
		v_dedicated_to          ,
		v_area                  ,
		v_region                ,
		v_fs_status             ,
		v_hr_status             ,
        v_review_date,
        v_record_complete;
        
		/*exiting loop when no records found*/
		IF finished = 1 THEN 
			LEAVE getofscEmployeeDetails;
		END IF;
         
		IF v_service_end_date ='0000-00-00 00:00:00'
		THEN
		  set v_service_end_date =null;
		END IF;
		
		/*fetching new change id for new change request*/
		SELECT IF (max(change_id) IS NULL,1,max(change_id)+1)  
		  INTO v_change_id
		  FROM RAC_FS_TM_EMPLOYEE_UPD;

		/*creating new change request by inserting in RAC_FS_TM_EMPLOYEE_UPD table */
		/*since record for new employee added the change type will be ADD type*/
        INSERT INTO RAC_FS_TM_EMPLOYEE_UPD
        	(CHANGE_ID,
             CHANGE_NOTE,
			 CHANGE_EFFECTIVE_DATE ,
			 EMPLOYEE_ID,
             EMPLOYEE_NAME,
			 PRODUCTION_PRINT,
			 ALTERNATE_EMAIL,
			 OFSC_STATUS,
			 APPROVAL_REQUIRED,
			 APPROVED,
			 CHANGE_TYPE,
			 CHANGE_STATUS,
			 REQUESTED_BY,
             CREATED_BY,
             LAST_UPDATED_BY,
			 JOB_TITLE,
			 JOB_ADP,
			 JOB_TYPE,
			 TEAM_TYPE,
			 MANAGER_ID,
			 MANAGER_FLAG,
			 SERVICE_START_DATE,
			 SERVICE_END_DATE,
			 ABSENCE_START_DATE,
			 ABSENCE_END_DATE,
			 ACTUAL_RETURN_TO_WORK,
			 WORK_SHIFT,
			 CIP,
			 BUSINESS_ORG,
			 ON_CALL,
			 ON_SITE,
			 SERVICE_ADVANTAGE,
			 DEDICATED,
			 DEDICATED_TO,
			 AREA,
			 REGION,
			 FS_STATUS,
			 HR_STATUS,
             REVIEW_DATE,
             RECORD_COMPLETE
			 )
			 VALUES
			 (v_change_id,
             'Change from OFSC sync up',
			 CURRENT_TIMESTAMP,
			 v_employee_id,
             v_employee_name,
			 v_production_print,
			 v_alternate_email,
			 v_status,
			 'N',
			 'Y',
			 'UPDATE',
			 'Pending',
			 'OFSC',
             'OFSC',
             'OFSC',
              v_job_title,
			  v_job_adp,
			  v_job_type,
			  v_team_type,
			  v_manager_id,
			  v_manager_flag,
			  v_service_start_date,
			  v_service_end_date,
			  v_absence_start_date,
			  v_absence_end_date,
			  v_actual_return_to_work,
			  v_work_shift,
			  v_cip,
			  v_business_org,
			  v_on_call,
			  v_on_site,
			  v_service_advantage,
			  v_dedicated,
			  v_dedicated_to,
			  v_area,
			  v_region,
			  v_fs_status,
			  v_hr_status,
              v_review_date,
              v_record_complete
			 );
			 
    COMMIT;
	
	/****Calling procedure to set approval flag****/
	CALL RAC_FS_TM_APPROVAL_FLAG_PROCEDURE(v_change_id);
	
	/****Calling procedure to set csa flag****/
	CALL RAC_FS_TM_CSA_FLAG_PROCEDURE(v_change_id);  

  BEGIN
   DECLARE CONTINUE HANDLER FOR NOT FOUND 
	BEGIN
		set v_approval_required = 'N';
        set v_csa_notif_flag ='N';
        set v_change_status='N';
	END;
				
		SELECT APPROVAL_REQUIRED,CSA_NOTIFICATION_REQUIRED,CHANGE_STATUS
		INTO v_approval_required,v_csa_notif_flag,v_change_status
		FROM
			RAC_FS_TM_EMPLOYEE_UPD
		WHERE change_id = v_change_id;
	END;
    
    IF v_change_status = 'Approved'
    THEN
    Update  RAC_FS_TM_EMPLOYEE_DTLS
		Set alternate_email = v_alternate_email,
			ofsc_status = v_status,
			production_print = v_production_print
		Where employee_id=v_employee_id;	
		COMMIT;
   
    END IF;
  
  
    IF v_approval_required = 'N' AND v_csa_notif_flag = 'N' #AND v_change_status != 'Approved'
	THEN
		/*Inserting in main tech master table*/
		Update  RAC_FS_TM_EMPLOYEE_DTLS
		Set alternate_email = v_alternate_email,
			ofsc_status = v_status,
			production_print = v_production_print
		Where employee_id=v_employee_id;
		commit;
		


		UPDATE RAC_FS_TM_EMPLOYEE_UPD
		SET CHANGE_STATUS = 'Processed',
			ALTERNATE_EMAIL_OLD=v_fs_alternate_email,
			last_update_date = CURRENT_TIMESTAMP,
			last_updated_by = 'OFSC'
		WHERE change_id=v_change_id;
		
		COMMIT;
	END IF;

    END LOOP getofscEmployeeDetails;
	CLOSE ofscEmployee;

   update RAC_FS_TM_EMPLOYEE_DTLS fs
set ofsc_last_login = (select distinct last_login from RAC_FS_TM_OFSC_DTLS ofsc,RAC_HR_TM_EMPLOYEE_DTLS hr
 where ofsc.resource_number=hr.resource_number
 and ofsc.RESOURCE_NUMBER not like '%T%'
 AND hr.employee_id=fs.employee_id);   

commit;

END
//
DELIMITER ;
