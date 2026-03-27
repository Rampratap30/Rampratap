DELIMITER //
CREATE PROCEDURE `RAC_FS_TM_ONE_TIME_PROCEDURE`()
BEGIN

DECLARE finished                	INTEGER DEFAULT 0;
DECLARE v_change_id                	INTEGER DEFAULT 0;
DECLARE v_employee_id               BIGINT(60)  DEFAULT 0;
DECLARE v_alternate_email           VARCHAR(400);
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

#fetch ofsc records whose values for ofsc status,alternate email or print production is updated
DECLARE ofscEmployee 
   CURSOR FOR 
      SELECT 
		fs.employee_id,
		null,
		null,
		null,
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
		FROM  RAC_FS_TM_EMPLOYEE_DTLS fs,RAC_HR_TM_EMPLOYEE_DTLS hr
		WHERE hr.employee_id = fs.employee_id
		AND fs.EMPLOYEE_ID not in (
		SELECT EMPLOYEE_ID FROM RAC_FS_TM_EMPLOYEE_UPD
		);
		
DECLARE CONTINUE HANDLER 
        FOR NOT FOUND SET finished = 1;

	
	/*opening cursor of new employees*/
	OPEN ofscEmployee;
    
    
	/*looping cursor of new employees*/
    getofscEmployeeDetails: LOOP
		
		/*fetching new employees data in variables*/
		FETCH ofscEmployee 
		INTO v_employee_id,
		v_alternate_email,
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
             'AWS-ONE-TIME',
			 CURRENT_TIMESTAMP,
			 v_employee_id,
			 v_production_print,
			 v_alternate_email,
			 v_status,
			 'N',
			 'Y',
			 'ADD',
			 'Processed',
			 'AWS-ONE-TIME',
             'AWS-ONE-TIME',
             'AWS-ONE-TIME',
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
	
	UPDATE RAC_FS_TM_EMPLOYEE_UPD
	SET CHANGE_STATUS = 'Processed',
		last_update_date = CURRENT_TIMESTAMP,
		last_updated_by = 'AWS-ONE-TIME'
	WHERE change_id=v_change_id;
	
	COMMIT;
	

    END LOOP getofscEmployeeDetails;
	CLOSE ofscEmployee;

commit;

END
//
DELIMITER ;
