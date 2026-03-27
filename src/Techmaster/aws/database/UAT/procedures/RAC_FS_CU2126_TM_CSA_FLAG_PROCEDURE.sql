DELIMITER //
CREATE PROCEDURE RAC_FS_TM_CSA_FLAG_PROCEDURE(IN P_IN_CHANGE_ID BIGINT(10),OUT P_OUT_RET_STS varchar(10))
BEGIN

DECLARE finished                	INTEGER DEFAULT 0;
DECLARE v_employee_id               BIGINT(10);
DECLARE v_job_adp                   VARCHAR(100); 
DECLARE v_fs_job_adp                VARCHAR(100);
DECLARE v_job_adp_chk               VARCHAR(10);
DECLARE v_job_title                 VARCHAR(400); 
DECLARE v_fs_job_title              VARCHAR(400);
DECLARE v_job_title_chk             VARCHAR(10);
DECLARE v_team_type                 VARCHAR(100);
DECLARE v_fs_team_type              VARCHAR(100);
DECLARE v_team_type_chk             VARCHAR(10);
DECLARE v_manager_id                BIGINT(10);
DECLARE v_fs_manager_id             BIGINT(10);
DECLARE v_manager_chk               VARCHAR(10);
DECLARE v_manager_flag              VARCHAR(10);
DECLARE v_fs_manager_flag           VARCHAR(10);
DECLARE v_manager_flag_chk          VARCHAR(10);
DECLARE v_admin_notes               VARCHAR(4000); 
DECLARE v_fs_admin_notes            VARCHAR(4000); 
DECLARE v_admin_notes_chk           VARCHAR(10);
DECLARE v_fs_status                 VARCHAR(100); 
DECLARE v_old_fs_status             VARCHAR(100);      
DECLARE v_fs_status_chk             VARCHAR(10); 
DECLARE v_hr_status                 VARCHAR(100);
DECLARE v_old_hr_status             VARCHAR(100);
DECLARE v_hr_status_chk             VARCHAR(10);	
DECLARE v_area_short_name           VARCHAR(100); 
DECLARE v_fs_area_short_name        VARCHAR(100);
DECLARE v_area_short_chk            VARCHAR(10);
DECLARE v_region                    VARCHAR(100);
DECLARE v_fs_region                 VARCHAR(100);
DECLARE v_region_chk                VARCHAR(10);
DECLARE v_alternate_email           VARCHAR(400); 
DECLARE v_fs_alternate_email        VARCHAR(400);
DECLARE v_alternate_email_chk       VARCHAR(10);
DECLARE v_review_date               TIMESTAMP;
DECLARE v_fs_review_date            TIMESTAMP;
DECLARE v_review_date_chk           VARCHAR(10);
DECLARE v_change_type               VARCHAR(100);
DECLARE v_location_code             VARCHAR(100);
DECLARE v_fs_location_code          VARCHAR(100);
DECLARE v_location_code_chk         VARCHAR(10);
DECLARE v_actual_termination_date          TIMESTAMP;



#fetch change request details from  table
DECLARE changeRecord
   CURSOR FOR 
	SELECT 
		up.employee_id,
		up.job_adp,
		(select job_adp from RAC_FS_TM_JOB_CODE job where job.job_id = fs.job_id),
		(select csa_notification_flag from RAC_FS_TM_REQ_CLMS where field_name ='JOB_ADP'),
		up.job_title,
		(select job_title from RAC_FS_TM_JOB_CODE job where job.job_id = fs.job_id),
		(select csa_notification_flag from RAC_FS_TM_REQ_CLMS where field_name ='JOB_TITLE'),
		up.team_type,
		(select team_type from RAC_FS_TM_TEAM_TYPE team where team.team_type_id = fs.team_type_id),
		(select csa_notification_flag from RAC_FS_TM_REQ_CLMS where field_name ='TEAM_TYPE'),
		up.manager_id,
		fs.manager_id,
		(select csa_notification_flag from RAC_FS_TM_REQ_CLMS where field_name ='MANAGER_ID'),
		up.manager_flag,
		fs.manager_flag,
		(select csa_notification_flag from RAC_FS_TM_REQ_CLMS where field_name ='MANAGER_FLAG'),
		up.admin_notes,
		fs.admin_notes,
		(select csa_notification_flag from RAC_FS_TM_REQ_CLMS where field_name ='ADMIN_NOTES'),
		up.fs_status,
		fs.fs_status,
		(select csa_notification_flag from RAC_FS_TM_REQ_CLMS where field_name ='FS_STATUS'),
		up.hr_status,
		(SELECT hr_status from RAC_HR_TM_EMPLOYEE_DTLS hr where hr.employee_id = up.employee_id),
		(select csa_notification_flag from RAC_FS_TM_REQ_CLMS where field_name ='HR_STATUS'),
		up.area,
		(select area_short_name from RAC_FS_TM_AREA area where area.area_id = fs.area_id),
		(select csa_notification_flag from RAC_FS_TM_REQ_CLMS where field_name ='AREA_SHORT'),
		up.region,
		(select region from RAC_FS_TM_AREA area,RAC_FS_TM_REGION region where area.area_id = fs.area_id and region.region_id = area.region_id),
		(select csa_notification_flag from RAC_FS_TM_REQ_CLMS where field_name ='REGION'),
		up.alternate_email,
		fs.alternate_email,
		(select csa_notification_flag from RAC_FS_TM_REQ_CLMS where field_name ='OFSC_ALTERNATE_EMAIL'),
		up.review_date,
		#fs.review_date,
		(select csa_notification_flag from RAC_FS_TM_REQ_CLMS where field_name ='REVIEW_DATE' and up.review_date IS NOT NULL),
		up.change_type,
		up.loc_code,
		fs.location_code,
		(select csa_notification_flag from RAC_FS_TM_REQ_CLMS where field_name ='LOCATION_CODE'),
		(select actual_termination_date from RAC_HR_TM_EMPLOYEE_DTLS hr where hr.employee_id = fs.employee_id)
	FROM
		RAC_FS_TM_EMPLOYEE_UPD up,
		RAC_FS_TM_EMPLOYEE_DTLS fs
	WHERE
        fs.employee_id = up.employee_id
		AND up.change_id = P_IN_CHANGE_ID; 
		
	DECLARE CONTINUE HANDLER 
        FOR NOT FOUND SET finished = 1;


	
	
	CALL RAC_FS_TM_WRITE_LOG_MESSAGES('RAC_FS_TM_APPROVAL_FLAG_PROCEDURE','Begin Procedure');
	
	/*opening cursor of new employees*/
	OPEN changeRecord;
    
    CALL RAC_FS_TM_WRITE_LOG_MESSAGES('RAC_FS_TM_APPROVAL_FLAG_PROCEDURE','Cursor changeRecord Opened');	
    

	/*looping cursor of input employees*/
    getDetails: LOOP
		
		/*fetching records for input employees*/
		FETCH changeRecord 
		 INTO v_employee_id ,		 
		 v_job_adp , 
		 v_fs_job_adp ,
		 v_job_adp_chk,
		 v_job_title , 
		 v_fs_job_title ,
		 v_job_title_chk ,
		 v_team_type , 
		 v_fs_team_type ,
		 v_team_type_chk,
		 v_manager_id , 
		 v_fs_manager_id ,
		 v_manager_chk,
		 v_manager_flag , 
		 v_fs_manager_flag ,
         v_manager_flag_chk,		 
		 v_admin_notes , 
		 v_fs_admin_notes ,
		 v_admin_notes_chk,
		 v_fs_status , 
	     v_old_fs_status ,
		 v_fs_status_chk,
		 v_hr_status ,
		 v_old_hr_status ,	
		 v_hr_status_chk,
		 v_area_short_name , 
		 v_fs_area_short_name ,
		 v_area_short_chk ,
		 v_region , 
		 v_fs_region ,
		 v_region_chk ,
		 v_alternate_email , 
		 v_fs_alternate_email ,
		 v_alternate_email_chk,
		 v_review_date ,
		 #v_fs_review_date,
		 v_review_date_chk,
		 v_change_type,
		 v_location_code,
         v_fs_location_code,
         v_location_code_chk,
		 v_actual_termination_date;
		
     /*exiting loop when no records found*/
		IF finished = 1 THEN 
        CALL RAC_FS_TM_WRITE_LOG_MESSAGES('RAC_FS_TM_APPROVAL_FLAG_PROCEDURE','Leaving getDetails loop');
			LEAVE getDetails;
		END IF;
		
	UPDATE RAC_FS_TM_EMPLOYEE_UPD
	   SET CSA_CHANGE_COMMENT=''
	 WHERE CHANGE_ID = P_IN_CHANGE_ID
	    AND CSA_CHANGE_COMMENT IS NULL;
	
    #If new employee is added to tech master the approval_flag will be Y for the change request		
	IF (v_change_type ='ADD')
	THEN 
	
	  UPDATE RAC_FS_TM_EMPLOYEE_UPD
	     SET CSA_NOTIFICATION_REQUIRED = 'Y',CSA_CHANGE_COMMENT=CONCAT(CSA_CHANGE_COMMENT,'New Hire')
	   WHERE CHANGE_ID = P_IN_CHANGE_ID;
	   
	   
      COMMIT;	  
	  	  
	END IF;
	
	IF v_region != v_fs_region AND v_region_chk='Y'
		THEN
      UPDATE RAC_FS_TM_EMPLOYEE_UPD
	     SET CSA_NOTIFICATION_REQUIRED = 'Y',CSA_CHANGE_COMMENT=CONCAT(CSA_CHANGE_COMMENT,'Region Change')
	   WHERE CHANGE_ID = P_IN_CHANGE_ID;
	   
      COMMIT;	
	END IF;
	
	IF v_area_short_name != v_fs_area_short_name  AND v_area_short_chk ='Y'
		THEN
      UPDATE RAC_FS_TM_EMPLOYEE_UPD
	     SET CSA_NOTIFICATION_REQUIRED = 'Y',CSA_CHANGE_COMMENT=CONCAT(CSA_CHANGE_COMMENT,'Area Change')
	   WHERE CHANGE_ID = P_IN_CHANGE_ID;
	   
      COMMIT;	
	  ITERATE getDetails;
	  	
	END IF;
	
    /*IF v_location_code != v_fs_location_code AND (v_location_code IS NOT NULL OR v_location_code !='') AND v_location_code_chk ='Y'
	THEN
      UPDATE RAC_FS_TM_EMPLOYEE_UPD
	     SET CSA_NOTIFICATION_REQUIRED = 'Y'
	   WHERE CHANGE_ID = P_IN_CHANGE_ID;
	   
      COMMIT;	  
	  ITERATE getDetails;		
		 
	END IF;*/
	
	 IF v_alternate_email != v_fs_alternate_email AND (v_alternate_email IS NOT NULL OR v_alternate_email !='') AND v_alternate_email_chk ='Y'
	THEN
      UPDATE RAC_FS_TM_EMPLOYEE_UPD
	     SET CSA_NOTIFICATION_REQUIRED = 'Y',CSA_CHANGE_COMMENT=CONCAT(CSA_CHANGE_COMMENT,'Cell_Number')
	   WHERE CHANGE_ID = P_IN_CHANGE_ID;
	   
      COMMIT;	
		 
	END IF;
	
	IF v_manager_id != v_fs_manager_id  AND v_manager_chk ='Y'
		THEN
      UPDATE RAC_FS_TM_EMPLOYEE_UPD
	     SET CSA_NOTIFICATION_REQUIRED = 'Y',CSA_CHANGE_COMMENT=CONCAT(CSA_CHANGE_COMMENT,'Manager_Change')
	   WHERE CHANGE_ID = P_IN_CHANGE_ID;
	   
      COMMIT;	  
		
	END IF;
	
	
	IF v_job_adp != v_fs_job_adp  AND v_job_adp_chk ='Y'
		THEN
      UPDATE RAC_FS_TM_EMPLOYEE_UPD
	     SET CSA_NOTIFICATION_REQUIRED = 'Y',CSA_CHANGE_COMMENT=CONCAT(CSA_CHANGE_COMMENT,'Job_ADP change')
	   WHERE CHANGE_ID = P_IN_CHANGE_ID;
	   
      COMMIT;	  
    	  
		
	END IF;
	
	IF v_job_title != v_fs_job_title  AND v_job_title_chk ='Y'
		THEN
      UPDATE RAC_FS_TM_EMPLOYEE_UPD
	     SET CSA_NOTIFICATION_REQUIRED = 'Y',CSA_CHANGE_COMMENT=CONCAT(CSA_CHANGE_COMMENT,'Job Title Change')
	   WHERE CHANGE_ID = P_IN_CHANGE_ID;
	   
      COMMIT;	  
		 
	END IF;
	
	IF v_fs_status != v_old_fs_status  AND v_fs_status_chk ='Y'
		THEN
      UPDATE RAC_FS_TM_EMPLOYEE_UPD
	     SET CSA_NOTIFICATION_REQUIRED = 'Y',CSA_CHANGE_COMMENT=CONCAT(CSA_CHANGE_COMMENT,'FS Status')
	   WHERE CHANGE_ID = P_IN_CHANGE_ID;
	   
      COMMIT;	  
 	
	END IF;
	
	IF v_hr_status != v_old_hr_status AND v_hr_status_chk ='Y'
		THEN
      UPDATE RAC_FS_TM_EMPLOYEE_UPD
	     SET CSA_NOTIFICATION_REQUIRED = 'Y',CSA_CHANGE_COMMENT=CONCAT(CSA_CHANGE_COMMENT,'HR Status')
	   WHERE CHANGE_ID = P_IN_CHANGE_ID;
	   
      COMMIT;	  
		
	END IF;
	
	IF v_manager_flag != v_fs_manager_flag AND v_manager_flag_chk ='Y'
		THEN
      UPDATE RAC_FS_TM_EMPLOYEE_UPD
	     SET CSA_NOTIFICATION_REQUIRED = 'Y',CSA_CHANGE_COMMENT=CONCAT(CSA_CHANGE_COMMENT,'Manager Flag')
	   WHERE CHANGE_ID = P_IN_CHANGE_ID;
	   
      COMMIT;	  
		
	END IF;
	
	
	IF v_admin_notes != v_fs_admin_notes AND (v_admin_notes IS NOT NULL OR v_admin_notes !='') AND v_admin_notes_chk ='Y'
		THEN
      UPDATE RAC_FS_TM_EMPLOYEE_UPD
	     SET CSA_NOTIFICATION_REQUIRED = 'Y',CSA_CHANGE_COMMENT=CONCAT(CSA_CHANGE_COMMENT,'ADmin Notes')
	   WHERE CHANGE_ID = P_IN_CHANGE_ID;
	   
      COMMIT;	  
		
	END IF;
	
	IF  v_review_date IS NOT NULL AND v_review_date_chk ='Y' AND v_review_date!='0000-00-00 00:00:00'
		THEN
      UPDATE RAC_FS_TM_EMPLOYEE_UPD
	     SET CSA_NOTIFICATION_REQUIRED = 'Y',CSA_CHANGE_COMMENT=CONCAT(CSA_CHANGE_COMMENT,'Review Date')
	   WHERE CHANGE_ID = P_IN_CHANGE_ID;
	   
      COMMIT;	  
		
	END IF;

	IF v_hr_status != v_old_hr_status  AND v_hr_status_chk ='Y'
		THEN
      UPDATE RAC_FS_TM_EMPLOYEE_UPD
	     SET CSA_NOTIFICATION_REQUIRED = 'Y',CSA_CHANGE_COMMENT=CONCAT(CSA_CHANGE_COMMENT,'HR Status')
	   WHERE CHANGE_ID = P_IN_CHANGE_ID;
	   
      COMMIT;	  
 	
	END IF;
	
	IF v_actual_termination_date IS NOT NULL AND v_actual_termination_date !='0000-00-00 00:00:00'
		THEN
      UPDATE RAC_FS_TM_EMPLOYEE_UPD
	     SET CSA_NOTIFICATION_REQUIRED = 'Y',CSA_CHANGE_COMMENT=CONCAT(CSA_CHANGE_COMMENT,'Termed')
	   WHERE CHANGE_ID = P_IN_CHANGE_ID;
	   
      COMMIT;		 
 	
	END IF;
	CALL RAC_FS_TM_WRITE_LOG_MESSAGES('RAC_FS_TM_BULK_IMPORT_PROCEDURE','End of getDetails Loop');	
    
    END LOOP getDetails;
	CLOSE changeRecord;

    UPDATE RAC_FS_TM_EMPLOYEE_UPD
	     SET CSA_NOTIFICATION_REQUIRED = 'N'
	   WHERE CHANGE_ID = P_IN_CHANGE_ID
	     AND (CSA_NOTIFICATION_REQUIRED != 'Y' OR CSA_NOTIFICATION_REQUIRED IS NULL );
	
    COMMIT;	
 CALL RAC_FS_TM_WRITE_LOG_MESSAGES('RAC_FS_TM_BULK_IMPORT_PROCEDURE','End of Procedure');	

END
//
DELIMITER ;
