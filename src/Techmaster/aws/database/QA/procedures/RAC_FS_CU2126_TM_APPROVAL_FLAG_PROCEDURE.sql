DELIMITER //
CREATE PROCEDURE RAC_FS_TM_APPROVAL_FLAG_PROCEDURE(IN P_IN_CHANGE_ID BIGINT(10))
BEGIN

DECLARE finished                	INTEGER DEFAULT 0;
DECLARE v_employee_id               BIGINT(10);
DECLARE v_job_adp                   VARCHAR(100)DEFAULT NULL;
DECLARE v_fs_job_adp                VARCHAR(100)DEFAULT NULL;
DECLARE v_job_adp_chk               VARCHAR(10)DEFAULT 'N';
DECLARE v_job_title                 VARCHAR(400) DEFAULT NULL; 
DECLARE v_fs_job_title              VARCHAR(400) DEFAULT NULL;
DECLARE v_job_title_chk             VARCHAR(10) DEFAULT 'N';
DECLARE v_team_type                 VARCHAR(100) DEFAULT NULL;
DECLARE v_fs_team_type              VARCHAR(100) DEFAULT NULL;
DECLARE v_team_type_chk             VARCHAR(10) DEFAULT 'N';
DECLARE v_manager_id                BIGINT(10) DEFAULT 0;
DECLARE v_fs_manager_id             BIGINT(10) DEFAULT 0;
DECLARE v_manager_chk               VARCHAR(10) DEFAULT 'N';
DECLARE v_manager_flag              VARCHAR(10) DEFAULT NULL;
DECLARE v_fs_manager_flag           VARCHAR(10) DEFAULT NULL;
DECLARE v_manager_flag_chk          VARCHAR(10) DEFAULT 'N';
DECLARE v_admin_notes               VARCHAR(4000) DEFAULT NULL; 
DECLARE v_fs_admin_notes            VARCHAR(4000) DEFAULT NULL; 
DECLARE v_admin_notes_chk           VARCHAR(10) DEFAULT 'N';
DECLARE v_fs_status                 VARCHAR(100) DEFAULT NULL;
DECLARE v_old_fs_status             VARCHAR(100) DEFAULT NULL;
DECLARE v_fs_status_chk             VARCHAR(10) DEFAULT 'N';
DECLARE v_hr_status                 VARCHAR(100) DEFAULT NULL;
DECLARE v_old_hr_status             VARCHAR(100) DEFAULT NULL;
DECLARE v_hr_status_chk             VARCHAR(10) DEFAULT 'N';
DECLARE v_area_short_name           VARCHAR(100) DEFAULT NULL; 
DECLARE v_fs_area_short_name        VARCHAR(100) DEFAULT NULL;
DECLARE v_area_short_chk            VARCHAR(10) DEFAULT 'N';
DECLARE v_region                    VARCHAR(100) DEFAULT NULL;
DECLARE v_fs_region                 VARCHAR(100) DEFAULT NULL;
DECLARE v_region_chk                VARCHAR(10) DEFAULT 'N';
DECLARE v_employee_name             VARCHAR(500) DEFAULT NULL;
DECLARE v_fs_employee_name          VARCHAR(500) DEFAULT NULL;
DECLARE v_employee_name_chk         VARCHAR(10) DEFAULT 'N';
DECLARE v_alternate_email           VARCHAR(400) DEFAULT NULL;
DECLARE v_fs_alternate_email        VARCHAR(400) DEFAULT NULL;
DECLARE v_alternate_email_chk       VARCHAR(10) DEFAULT 'N';
DECLARE v_review_date               TIMESTAMP DEFAULT NULL;
DECLARE v_fs_review_date            TIMESTAMP DEFAULT NULL;
DECLARE v_review_date_chk           VARCHAR(10) DEFAULT 'N';
DECLARE v_change_type               VARCHAR(100) DEFAULT NULL;
#DECLARE v_location_code             VARCHAR(100);
#DECLARE v_fs_location_code          VARCHAR(100);
#DECLARE v_location_code_chk         VARCHAR(10);
DECLARE v_absence_start_date        TIMESTAMP DEFAULT NULL;
DECLARE v_fs_absence_start_date     TIMESTAMP DEFAULT NULL;
DECLARE v_absence_start_date_chk    VARCHAR(10);
DECLARE v_absence_end_date          TIMESTAMP DEFAULT NULL;
DECLARE v_fs_absence_end_date       TIMESTAMP DEFAULT NULL;
DECLARE v_absence_end_date_chk      VARCHAR(10);
DECLARE v_return_to_work            TIMESTAMP DEFAULT NULL;
DECLARE v_fs_return_to_work         TIMESTAMP DEFAULT NULL;
DECLARE v_return_to_work_chk        VARCHAR(10);


#fetch change request details from  table
DECLARE changeRecord
   CURSOR FOR 
	SELECT 
		up.employee_id,
		up.job_adp,
		(select job_adp from RAC_FS_TM_JOB_CODE job where job.job_id = fs.job_id),
		(select approval_req from RAC_FS_TM_REQ_CLMS where field_name ='JOB_ADP_CODE'),
        up.employee_name,
		fs.employee_name,
		(select approval_req from RAC_FS_TM_REQ_CLMS where field_name ='EMPLOYEE_NAME'),
		up.job_title,
		(select job_title from RAC_FS_TM_JOB_CODE job where job.job_id = fs.job_id),
		(select approval_req from RAC_FS_TM_REQ_CLMS where field_name ='JOB_TITLE'),
		up.team_type,
		(select team_type from RAC_FS_TM_TEAM_TYPE team where team.team_type_id = fs.team_type_id),
		(select approval_req from RAC_FS_TM_REQ_CLMS where field_name ='TEAM_TYPE'),
		up.manager_id,
		fs.manager_id,
		(select approval_req from RAC_FS_TM_REQ_CLMS where field_name ='MANAGER_EMPLOYEE_ID'),
		up.manager_flag,
		fs.manager_flag,
		(select approval_req from RAC_FS_TM_REQ_CLMS where field_name ='MANAGER_FLAG'),
		up.admin_notes,
		fs.admin_notes,
		(select approval_req from RAC_FS_TM_REQ_CLMS where field_name ='ADMIN_NOTES'),
		up.fs_status,
		fs.fs_status,
		(select approval_req from RAC_FS_TM_REQ_CLMS where field_name ='FS_STATUS'),
		up.hr_status,
		(SELECT hr_status from RAC_HR_TM_EMPLOYEE_DTLS hr where hr.employee_id = up.employee_id),
		(select approval_req from RAC_FS_TM_REQ_CLMS where field_name ='HR_STATUS'),
		up.area,
		(select area_short_name from RAC_FS_TM_AREA area where area.area_id = fs.area_id),
		(select approval_req from RAC_FS_TM_REQ_CLMS where field_name ='AREA_SHORT'),
		up.region,
		(select region from RAC_FS_TM_AREA area,RAC_FS_TM_REGION region where area.area_id = fs.area_id and region.region_id = area.region_id),
		(select approval_req from RAC_FS_TM_REQ_CLMS where field_name ='REGION'),
		up.alternate_email,
		fs.alternate_email,
		(select approval_req from RAC_FS_TM_REQ_CLMS where field_name ='OFSC_ALTERNATE_EMAIL'),
		up.review_date,
		#fs.review_date,
		(select approval_req from RAC_FS_TM_REQ_CLMS where field_name ='REVIEW_DATE' and up.review_date IS NOT NULL),
		up.change_type,
       # up.review_date,
        up.absence_start_date,
        fs.absence_start_date,
        (select approval_req from RAC_FS_TM_REQ_CLMS where field_name ='ABSENCE_START_DATE' and up.absence_start_date IS NOT NULL),
        up.absence_end_date,
        fs.absence_end_date,
        (select approval_req from RAC_FS_TM_REQ_CLMS where field_name ='ABSENCE_END_DATE' and up.absence_start_date IS NOT NULL),
		up.actual_return_to_work,
        fs.actual_return_to_work,
        (select approval_req from RAC_FS_TM_REQ_CLMS where field_name ='ACTUAL_RETURN_TO_WORK' and up.actual_return_to_work IS NOT NULL)/*,/*,
		up.loc_code,
		fs.location_code,
		(select approval_req from RAC_FS_TM_REQ_CLMS where field_name ='LOCATION_CODE')*/
	FROM
		RAC_FS_TM_EMPLOYEE_UPD up,
		RAC_FS_TM_EMPLOYEE_DTLS fs
	WHERE
        fs.employee_id = up.employee_id
		AND up.change_id = P_IN_CHANGE_ID
		AND COALESCE(up.APPROVAL_REQUIRED,'N') != 'Y'
		AND COALESCE(up.APPROVED,'N') != 'Y'; 
		
	DECLARE CONTINUE HANDLER 
        FOR NOT FOUND SET finished = 1;

	/*opening cursor of new employees*/
	OPEN changeRecord;
        

	/*looping cursor of input employees*/
    getDetails: LOOP
		
		/*fetching records for input employees*/
		FETCH changeRecord 
		 INTO v_employee_id ,		 
		 v_job_adp , 
		 v_fs_job_adp ,
		 v_job_adp_chk,
         v_employee_name,
         v_fs_employee_name,
         v_employee_name_chk,
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
         v_absence_start_date,
         v_fs_absence_start_date,
         v_absence_start_date_chk,
         v_absence_end_date,
         v_fs_absence_end_date,
         v_absence_end_date_chk,
         v_return_to_work,
         v_fs_return_to_work,
         v_return_to_work_chk
         /*,
		 v_location_code,
         v_fs_location_code,
         v_location_code_chk*/
		 ;
		
     /*exiting loop when no records found*/
		IF finished = 1 THEN 
			LEAVE getDetails;
		END IF;

		IF v_admin_notes =''
        THEN
         set v_admin_notes =null;
        END IF;
        
        IF v_fs_admin_notes =''
        THEN
         set v_fs_admin_notes =null;
        END IF;

        
        IF v_fs_status =''
        THEN
			set v_fs_status =null;
        END IF;
        
        IF v_old_fs_status =''
        THEN 
			set v_old_fs_status =null;
        END IF;
        
        IF v_hr_status=''
        THEN
			set v_hr_status = null;
        END IF;
        
        IF v_old_hr_status=''
        THEN
			set v_old_hr_status = null;
        END IF;
		
        IF v_region=''
        THEN
         set v_region = null;
        END IF;
        
        IF v_fs_region=''
        THEN
         set v_fs_region = null;
        END IF;
        
        IF v_manager_flag=''
        THEN
          set v_manager_flag = NULL;
		END IF;
        
        IF v_fs_manager_flag=''
        THEN
          set v_fs_manager_flag = NULL;
		END IF;
        
        IF v_area_short_name=''
        THEN
          set v_area_short_name = NULL;
		END IF;
        
        IF v_fs_area_short_name=''
        THEN
          set v_fs_area_short_name = NULL;
		END IF;
        
        IF v_manager_id=''
        THEN
          set v_manager_id = NULL;
		END IF;
        
        IF v_fs_manager_id=''
        THEN
          set v_fs_manager_id = NULL;
		END IF;
        
        IF v_job_adp=''
        THEN
          set v_job_adp = NULL;
		END IF;
        
        IF v_fs_job_adp=''
        THEN
          set v_fs_job_adp = NULL;
		END IF;
        
        IF v_job_title=''
        THEN
          set v_job_title = NULL;
		END IF;
        
        IF v_fs_job_title=''
        THEN
          set v_fs_job_title = NULL;
		END IF;
        
        IF v_fs_employee_name=''
        THEN
          set v_fs_employee_name = NULL;
		END IF;
        
        IF v_employee_name=''
        THEN
          set v_employee_name = NULL;
		END IF;
        
        IF v_fs_alternate_email =''
        THEN
           set v_fs_alternate_email = NULL;
        END IF;
        
        IF v_alternate_email =''
        THEN
           set v_alternate_email = NULL;
        END IF;
        
        IF  v_absence_start_date = ''
        THEN 
          set v_absence_start_date = NULL;
        END IF;
        
         IF  v_absence_end_date = ''
        THEN 
          set v_absence_end_date = NULL;
        END IF;
        
		IF  v_fs_absence_start_date = ''
        THEN 
          set v_fs_absence_start_date = NULL;
        END IF;
        
        IF  v_fs_absence_end_date = ''
        THEN 
          set v_fs_absence_end_date = NULL;
        END IF;
        
        IF  v_absence_start_date_chk = ''
        THEN 
          set v_absence_start_date_chk = NULL;
        END IF;
        
        IF  v_return_to_work = ''
        THEN 
          set v_return_to_work = NULL;
        END IF;
        
        IF  v_fs_return_to_work = ''
        THEN 
          set v_fs_return_to_work = NULL;
        END IF;
        
        IF  v_absence_end_date_chk = ''
        THEN 
          set v_absence_end_date_chk = NULL;
        END IF;
        
        IF  v_return_to_work_chk = ''
        THEN 
          set v_return_to_work_chk = NULL;
        END IF;
        
       
        
    #If new employee is added to tech master the approval_flag will be Y for the change request		
	IF /*(v_change_type ='ADD') OR */
	(COALESCE(v_region,'X') != COALESCE(v_fs_region,'X') AND v_region_chk='Y') 
	 OR (COALESCE(v_employee_name,'X') != COALESCE(v_fs_employee_name,'X') AND v_employee_name_chk='Y') 
     OR (COALESCE(v_area_short_name,'X') != COALESCE(v_fs_area_short_name,'X')  AND v_area_short_chk ='Y')
     OR (COALESCE(v_manager_id,'X') != COALESCE(v_fs_manager_id,'X') AND v_manager_chk ='Y') 
	 OR (COALESCE(v_job_adp,'X') != COALESCE(v_fs_job_adp,'X')  AND v_job_adp_chk ='Y')
     OR (COALESCE(v_job_title,'X') != COALESCE(v_fs_job_title,'X') AND (v_job_title IS NOT NULL OR v_job_title !='') AND v_job_title_chk ='Y') 
     OR (COALESCE(v_fs_status,'X') != COALESCE(v_old_fs_status,'X')  AND v_fs_status_chk ='Y')
	 OR (COALESCE(v_hr_status,'X') != COALESCE(v_old_hr_status,'X') AND v_hr_status_chk ='Y') 
     OR (COALESCE(v_manager_flag,'X') != COALESCE(v_fs_manager_flag,'X') AND v_manager_flag_chk ='Y') 
     OR ((v_review_date IS NOT NULL OR v_review_date !='0000-00-00 00:00:00' OR v_review_date!='') AND v_review_date_chk ='Y')
     OR (COALESCE(v_fs_alternate_email,'X') != COALESCE(v_alternate_email,'X') AND v_alternate_email_chk ='Y')
	 OR ((COALESCE(v_admin_notes,'X') != COALESCE(v_fs_admin_notes,'X')) AND v_admin_notes_chk ='Y')
	 OR ((COALESCE(v_absence_start_date,'X') != COALESCE(v_fs_absence_start_date,'X')) AND v_absence_start_date_chk ='Y')
     OR ((COALESCE(v_absence_end_date,'X') != COALESCE(v_fs_absence_end_date,'X')) AND v_absence_end_date_chk ='Y')
	 OR ((COALESCE(v_return_to_work,'X') != COALESCE(v_fs_return_to_work,'X')) AND v_return_to_work_chk ='Y')
    THEN 
	
	  UPDATE RAC_FS_TM_EMPLOYEE_UPD
	     SET APPROVAL_REQUIRED = 'Y'
	   WHERE CHANGE_ID = P_IN_CHANGE_ID;
	   
      COMMIT;	  
	  
	  ITERATE getDetails;
	  
	END IF;

    
	
	
    END LOOP getDetails;
	CLOSE changeRecord;
    
	UPDATE RAC_FS_TM_EMPLOYEE_UPD
	     SET APPROVAL_REQUIRED = 'N',Change_status='Approved'
	   WHERE CHANGE_ID = P_IN_CHANGE_ID
	     AND APPROVAL_REQUIRED != 'Y' OR APPROVAL_REQUIRED IS NULL ;
	
    COMMIT;	


END
//
DELIMITER ;
