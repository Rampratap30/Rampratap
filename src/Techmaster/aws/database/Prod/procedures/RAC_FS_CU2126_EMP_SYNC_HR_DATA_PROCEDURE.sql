DROP PROCEDURE `RAC_FS_TM_EMP_SYNC_HR_DATA_PROCEDURE`;
DELIMITER //
CREATE PROCEDURE `RAC_FS_TM_EMP_SYNC_HR_DATA_PROCEDURE`()
BEGIN
DECLARE finished                	INTEGER DEFAULT 0;
DECLARE v_change_id                	INTEGER DEFAULT 0;
DECLARE v_change_id1                INTEGER DEFAULT 0;
DECLARE v_service_start_date        TIMESTAMP;
DECLARE v_service_end_date          TIMESTAMP;
DECLARE v_absence_start_date        TIMESTAMP;
DECLARE v_absence_end_date          TIMESTAMP;
DECLARE v_actual_return_to_work     TIMESTAMP;
DECLARE v_manager_flag              VARCHAR(10) DEFAULT NULL;
DECLARE v_approval_flag             VARCHAR(10) DEFAULT NULL;
DECLARE v_csa_flag                  VARCHAR(10) DEFAULT 'N';
DECLARE v_employee_id           	BIGINT(60)  DEFAULT 0;
DECLARE	v_employee_name         	VARCHAR(400);
DECLARE v_hr_status                 VARCHAR(150);
DECLARE v_tm_review_date1           TIMESTAMP;
DECLARE v_resource_number           VARCHAR(150);
DECLARE v_hr_resource_number1       VARCHAR(150);
DECLARE	v_email                 	VARCHAR(150);
DECLARE v_job_adp                   VARCHAR(2000);
DECLARE v_job_type                  VARCHAR(150);
DECLARE v_auto_add                  VARCHAR(150);
DECLARE v_job_type1                 VARCHAR(150);
DECLARE	v_job_title					VARCHAR(1000);
DECLARE	v_job_family 				VARCHAR(150);
DECLARE	v_manager_employee_id   	BIGINT(60) DEFAULT 0;
DECLARE	v_manager_name				VARCHAR(150);
DECLARE	v_location_code         	VARCHAR(150) DEFAULT NULL;
DECLARE	v_area						VARCHAR(150) DEFAULT NULL;
DECLARE	v_area_short				VARCHAR(150) DEFAULT NULL;
DECLARE	v_region					VARCHAR(150) DEFAULT NULL;
DECLARE v_employee_id1           	BIGINT(60) DEFAULT 0;
DECLARE	v_employee_name1         	VARCHAR(150);
DECLARE	v_fs_employee_name1         VARCHAR(150);
DECLARE	v_email1                 	VARCHAR(150);
DECLARE v_job_adp1                  VARCHAR(150);
DECLARE v_hr_job_adp1               VARCHAR(150);
DECLARE v_job_chk                   VARCHAR(10) DEFAULT NULL;
DECLARE v_manager_chk               VARCHAR(10) DEFAULT NULL;
DECLARE v_manager_chk1              VARCHAR(10) DEFAULT NULL;
DECLARE	v_job_title1       			VARCHAR(150);
DECLARE	v_hr_job_title1				VARCHAR(150);
DECLARE	v_job_family1 				VARCHAR(150);
DECLARE	v_hr_job_family1 			VARCHAR(150);
DECLARE	v_manager_employee_id1   	BIGINT(60) DEFAULT 0;
DECLARE	v_hr_manager_employee_id1   BIGINT(60) DEFAULT 0;
DECLARE	v_manager_name1				VARCHAR(150);
DECLARE	v_hr_manager_name1			VARCHAR(150);
DECLARE	v_location_code1         	VARCHAR(150);
DECLARE	v_hr_location_code1         VARCHAR(150);
DECLARE	v_area1						VARCHAR(150);
DECLARE	v_hr_area1					VARCHAR(150);
DECLARE	v_area_short1				VARCHAR(150);
DECLARE	v_hr_area_short1			VARCHAR(150);
DECLARE	v_region1					VARCHAR(150);
DECLARE	v_hr_region1				VARCHAR(150);
DECLARE v_tm_job_adp                VARCHAR(150);
DECLARE	v_tm_job_type              	VARCHAR(150);
DECLARE	v_tm_job_title				VARCHAR(150);
DECLARE	v_tm_job_family 			VARCHAR(150);
DECLARE	v_tm_manager_employee_id   	BIGINT(60) DEFAULT 0;
DECLARE	v_tm_manager_name			VARCHAR(150);
DECLARE v_alternate_email1          VARCHAR(350);
DECLARE	v_tm_location_code         	VARCHAR(150);
DECLARE	v_tm_area					VARCHAR(150);
DECLARE	v_tm_area_short				VARCHAR(150);
DECLARE	v_tm_region					VARCHAR(150);
DECLARE v_csa_notification_required VARCHAR(10);
DECLARE v_approval_required         VARCHAR(10);
DECLARE v_record_complete			VARCHAR(10);
DECLARE v_csa_notification_required1 VARCHAR(10);
DECLARE v_approval_required1         VARCHAR(10) DEFAULT 'N';
DECLARE v_record_complete1			VARCHAR(10);
DECLARE v_job_id 	                BIGINT(60);
DECLARE v_job_id1 	                BIGINT(60);
DECLARE v_area_id 	                BIGINT(60);
DECLARE v_area_id1 	                BIGINT(60);
DECLARE v_team_type_id 	            BIGINT(60);
DECLARE v_team_type_id1 	        BIGINT(60);
DECLARE v_hr_service_start_date1    TIMESTAMP;
DECLARE v_hr_service_end_date1      TIMESTAMP;
DECLARE v_tm_service_end_date1      TIMESTAMP;
DECLARE v_hr_absence_start_date1    TIMESTAMP;
DECLARE v_hr_absence_end_date1      TIMESTAMP;
DECLARE v_hr_actual_return_to_work1	TIMESTAMP;
DECLARE v_tm_fs_status              VARCHAR(100);
DECLARE v_tm_hr_status1              VARCHAR(100);
DECLARE v_hr_status1                 VARCHAR(100);
DECLARE v_tm_manager_flag           VARCHAR(100);
DECLARE v_tm_record_complete        VARCHAR(100);
DECLARE v_tm_team_type              VARCHAR(100);
DECLARE v_tm_work_shift1            VARCHAR(10);
DECLARE v_tm_CIP1                   VARCHAR(10);
DECLARE v_tm_Business_Org1          VARCHAR(10);
DECLARE v_tm_On_call1               VARCHAR(10);
DECLARE v_tm_On_site1               VARCHAR(10);
DECLARE v_tm_service_advantage1     VARCHAR(10);
DECLARE v_tm_production_type1       VARCHAR(10);
DECLARE v_tm_dedicated1             VARCHAR(240);
DECLARE v_tm_dedicated_to1          VARCHAR(240);
DECLARE v_count                     BIGINT(10) DEFAULT 0;	
DECLARE	v_ins_change_note    		VARCHAR(2000) DEFAULT NULL;
DECLARE	v_upd_change_note    		VARCHAR(2000) DEFAULT NULL;
DECLARE v_tm_ofsc_status1           VARCHAR(100);
-- DECLARE v_ALTERNATE_EMAIL1          VARCHAR(400);
DECLARE v_PRODUCTION_PRINT1	        VARCHAR(100);

/*fetching new employees which exist in hr table and does not exist in tech master table */
DECLARE newEmployee 
   CURSOR FOR 
	  SELECT distinct  
		hr.employee_id,
		hr.employee_name,
		hr.hr_status,
		hr.email,
		hr.resource_number,
		hr.job_title,
		hr.job_adp,
		hr.manager_employee_id,
		hr.manager_name,
        'Y' csa_notification_required,
		'N' record_complete,
		hr.last_hire_date service_start_date,
		hr.actual_termination_date SERVICE_END_DATE,
		hr.absence_start_date ABSENCE_START_DATE,
		hr.absence_end_date	ABSENCE_END_DATE,
		hr.actual_return_to_work ACTUAL_RETURN_TO_WORK
	FROM  RAC_HR_TM_EMPLOYEE_DTLS hr
	WHERE  hr.oic_flag = 'N'
	AND not exists (select 1 from RAC_FS_TM_EMPLOYEE_DTLS tm where hr.employee_id=tm.employee_id);

/*fetching existing employees whose field is updated*/		
DECLARE updExistingEmployee 
   CURSOR FOR 
      SELECT 
		hr.employee_id,
		hr.employee_name,
		tm.employee_name,
        tm.alternate_email,
		tm.review_date,
		hr.email, 
		hr.job_title,
		(select distinct job.job_title from RAC_FS_TM_JOB_CODE job where tm.job_id=job.job_id) tm_job_title,
		hr.job_adp,
		(select distinct job.job_adp_code from RAC_FS_TM_JOB_CODE job where tm.job_id=job.job_id ) tm_job_adp,
		(select distinct job.job_type from RAC_FS_TM_JOB_CODE job where tm.job_id=job.job_id ) tm_job_type,
        hr.manager_employee_id,
		tm.manager_id,
		/*hr.area,
		(select area.area_name from RAC_FS_TM_LOC loc,RAC_FS_TM_AREA area 
		where loc.loc_id=tm.loc_id
		and area.area_id=loc.area_id) tm_area,*/
		hr.area_short,
		(select area.area_short_name from RAC_FS_TM_AREA area 
		where area.area_id=tm.area_id) tm_area_short,
		hr.region,
		(select distinct region.region_name from RAC_FS_TM_AREA area,RAC_FS_TM_REGION region
		where area.area_id=tm.area_id
		and area.region_id=region.region_id) tm_region,
        hr.absence_start_date,
        hr.absence_end_date,
        hr.actual_return_to_work	,
        hr.resource_number,		
		tm.fs_status,
        hr.hr_status,
        tm.hr_status,
        tm.manager_flag,
        hr.LAST_HIRE_DATE,
		hr.actual_termination_date,
		tm.service_end_date,		  
        tm.record_complete,
        (select distinct team.team_type_name from RAC_FS_TM_TEAM_TYPE team
		where team.team_type_id=tm.team_type_id) tm_team_type,
		tm.work_shift,
		tm.CIP,
		tm.Business_Org,
		tm.On_call,
		tm.On_site,
		tm.service_advantage,
		tm.production_type,
		tm.dedicated,
		tm.dedicated_to	,
        tm.ofsc_status,
       -- tm.ALTERNATE_EMAIL,
        tm.PRODUCTION_PRINT		
	 FROM  RAC_HR_TM_EMPLOYEE_DTLS hr,RAC_FS_TM_EMPLOYEE_DTLS tm
		WHERE tm.employee_id = hr.employee_id
		AND (  
				COALESCE(hr.job_adp,'X')  != COALESCE((select distinct job.job_adp_code from RAC_FS_TM_JOB_CODE job where tm.job_id=job.job_id  ),'X') 
			   or 
				(
					COALESCE(hr.manager_employee_id,'X')  != COALESCE(tm.manager_id,'X') 
					AND
					COALESCE(tm.MANAGER_FLAG,'X') != 'Y'
				)
               or 
				COALESCE(hr.hr_status,'X')  != COALESCE(tm.hr_status,'X') 
			   or 
				COALESCE(hr.actual_termination_date,'X')  != COALESCE(tm.service_end_date,'X')	
			   or 
				tm.employee_name != hr.employee_name
			   )
		 AND hr.oic_flag = 'N'
		 AND (
				COALESCE(tm.FS_STATUS,'X') != 'Inactive'
				OR
				(
					COALESCE(tm.FS_STATUS,'X') = 'Inactive'
					AND 
					COALESCE(tm.hr_status,'X') = 'Terminated'
					AND
					COALESCE(hr.hr_status,'X') = 'Active'
				)
			 )
		 ;

DECLARE unProcessedRec 
   CURSOR FOR 
	  SELECT distinct  
		hr.employee_id
	FROM  RAC_HR_TM_EMPLOYEE_DTLS hr
	WHERE  hr.oic_flag = 'N';
		 
	DECLARE CONTINUE HANDLER 
			FOR NOT FOUND SET finished = 1;


	/*Purging log tables*/
	DELETE FROM RAC_FS_TM_LOGS 
	WHERE
    creation_date <= DATE_ADD(CURRENT_DATE,
    INTERVAL - 180 DAY);

	DELETE FROM RAC_FS_TM_SYNC_LOGS 
	WHERE
    creation_date <= DATE_ADD(CURRENT_DATE,
    INTERVAL - 180 DAY);
		
	/*opening cursor of new employees*/
	OPEN newEmployee;
    
    
	/*looping cursor of new employees*/
    getNewEmployeeDetails: LOOP

		/*fetching new employees data in variables*/
		FETCH newEmployee 
		INTO v_employee_id,
		v_employee_name,
		v_hr_status,
		v_email,
		v_resource_number,
		v_job_title,
		v_job_adp,
		v_manager_employee_id,
		v_manager_name,
		v_csa_notification_required,
		v_record_complete,
		v_service_start_date,
		v_service_end_date,
		v_absence_start_date,
		v_absence_end_date,
		v_actual_return_to_work;
		
        
		/*exiting loop when no records found*/
		IF finished = 1 THEN 
			LEAVE getNewEmployeeDetails;
		END IF;
		
		SET v_auto_add ='N';
		SET v_manager_chk='N';
		SET v_job_chk=NULL;
		SET v_approval_required='Y';
		SET v_manager_flag='N';
		SET v_job_type=NULL;
		SET v_ins_change_note='HRMS - New Hire. ';
        
        BEGIN
		DECLARE CONTINUE HANDLER FOR NOT FOUND set v_count=0;
		
			SELECT 
				COUNT(*)
				INTO v_count FROM
			RAC_FS_TM_EMPLOYEE_UPD
			WHERE
			employee_id = v_employee_id
			AND change_type = 'ADD'
			AND change_status IN ('Pending' , 'Rejected','Approved');
		END;
		
		IF v_count>0
		THEN 
		   UPDATE RAC_HR_TM_EMPLOYEE_DTLS
			   SET OIC_FLAG = 'Y'
			WHERE EMPLOYEE_ID=v_employee_id;
		   
		   ITERATE getNewEmployeeDetails;
		END IF;
		/******Checking if job adp does not exist in tech master*******/
		BEGIN
			DECLARE CONTINUE HANDLER FOR NOT FOUND 
				BEGIN
					SET v_auto_add='N';
					SET v_job_chk=NULL;
                    set v_job_type =null;
				END;
				
			SELECT 
				'Y', approval_required, manager_flag, job_type, auto_add
			INTO v_job_chk , v_approval_required , v_manager_flag , v_job_type , v_auto_add 
			FROM
				RAC_FS_TM_JOB_CODE
			WHERE
				job_adp_code = v_job_adp
					AND upper(status) = 'ACTIVE';
						
		END;
		
		IF v_job_chk IS NULL 
		THEN
			INSERT INTO RAC_FS_TM_SYNC_LOGS (employee_id,resource_number,err_msg,sync_process) 
					VALUES (v_employee_id,v_resource_number,concat('HRMS - New Hire. ',v_job_adp,' - Job ADP not present in Tech Master or ADP status Inactive'),'HRMS');
		 	UPDATE RAC_HR_TM_EMPLOYEE_DTLS
			   SET OIC_FLAG = 'Y'
			WHERE EMPLOYEE_ID=v_employee_id;
			COMMIT;
		 ITERATE getNewEmployeeDetails;
		END IF;
		
		IF v_auto_add='Y'
		THEN
			SET v_ins_change_note=concat(v_ins_change_note,'Job Adp : ' ,v_job_adp,' valid. ');
		ELSE
			SET v_ins_change_note=concat(v_ins_change_note,'Job Adp : ' ,v_job_adp,' Auto_Add = ',v_auto_add,'. ');
		END IF;
		
		/***fetching area and region based on manager info***/
		IF v_manager_employee_id is not null and v_manager_employee_id !=''
		THEN
		    
			/******Checking if manager does not exist in tech master*******/
			BEGIN
				DECLARE CONTINUE HANDLER FOR NOT FOUND 
				BEGIN
					SET v_manager_chk = 'N';
				END;
				
				SELECT 
					manager_flag
				INTO v_manager_chk 
				FROM
					RAC_FS_TM_EMPLOYEE_DTLS
				WHERE
					employee_id = v_manager_employee_id;
					
			END;
		ELSE
			INSERT INTO RAC_FS_TM_SYNC_LOGS (employee_id,resource_number,err_msg,sync_process) 
					VALUES (v_employee_id,v_resource_number,concat('HRMS - New Hire. ',v_manager_employee_id,' - Manager is empty in HRMS'),'HRMS');
			
			UPDATE RAC_HR_TM_EMPLOYEE_DTLS 
			SET 
				OIC_FLAG = 'Y'
			WHERE
				EMPLOYEE_ID = v_employee_id;
			COMMIT;
			ITERATE getNewEmployeeDetails;
		END IF;
		
		IF ((v_manager_chk = 'N' OR v_manager_chk is NULL or v_manager_chk='') AND v_auto_add = 'N')
			THEN
			  	UPDATE RAC_HR_TM_EMPLOYEE_DTLS
				  SET OIC_FLAG = 'Y'
				WHERE EMPLOYEE_ID=v_employee_id;
				
				INSERT INTO RAC_FS_TM_SYNC_LOGS (employee_id,resource_number,err_msg,sync_process) 
					VALUES (v_employee_id,v_resource_number,concat('HRMS - New Hire. ',v_manager_employee_id,' and ',v_job_adp,' - Manager/job adp is not valid in Tech Master for new employee'),'HRMS');
				COMMIT;
			    ITERATE getNewEmployeeDetails;
		END IF;
		
		IF v_manager_chk='Y'
		THEN
			SET v_ins_change_note=concat(v_ins_change_note,'Manager : ' ,v_manager_employee_id,' valid. ');
		ELSE
			SET v_ins_change_note=concat(v_ins_change_note,'Manager : ' ,v_manager_employee_id,' not in TM.',' No valid Region or Area as per manager employee id. ');
		END IF;
		    
		IF (v_manager_chk='Y')
		THEN	
			BEGIN
				DECLARE CONTINUE HANDLER FOR NOT FOUND 
					BEGIN
						set v_area_id =null;	 
						set v_area_short =null;
						set v_region =null;
					
					END;
				SELECT 
					ar.AREA_ID, ar.area_short_name, re.region_name
				INTO v_area_id , v_area_short , v_region
				FROM
					RAC_FS_TM_EMPLOYEE_DTLS dt,
					RAC_FS_TM_AREA ar,
					RAC_FS_TM_REGION re
				WHERE
					employee_id = v_manager_employee_id
						AND ar.area_id = dt.area_id
						AND ar.region_id = re.region_id
						AND UPPER(ar.STATUS) = 'ACTIVE';
			END;
		END IF;
		
		
		IF v_service_end_date ='0000-00-00 00:00:00'
		THEN 
		   set v_service_end_date =null;
		END IF;
		
		/*fetching new change id for new change request*/
		SELECT 
			IF(MAX(change_id) IS NULL,
			1,
			MAX(change_id) + 1)
			INTO v_change_id 
		FROM
			RAC_FS_TM_EMPLOYEE_UPD;

		/*creating new change request by inserting in RAC_FS_TM_EMPLOYEE_UPD table */
		/*since record for new employee added the change type will be ADD type*/
        INSERT INTO RAC_FS_TM_EMPLOYEE_UPD
        	(CHANGE_ID,
			 CHANGE_NOTE,
			 CHANGE_EFFECTIVE_DATE ,
			 EMPLOYEE_ID,
			 EMPLOYEE_NAME,
			 HR_STATUS,
			 JOB_TITLE,
			 JOB_ADP,
             JOB_TYPE,
			 MANAGER_ID,
			 AREA,
			 REGION,
			 CSA_NOTIFICATION_REQUIRED,
			 APPROVAL_REQUIRED,
			 MANAGER_FLAG,
			 APPROVED,
			 CHANGE_TYPE,
			 CHANGE_STATUS,
			 TEAM_TYPE,
			 REQUESTED_BY,
			 FS_STATUS,
			 RECORD_COMPLETE,
			 SERVICE_START_DATE,
			 SERVICE_END_DATE,
			 ABSENCE_START_DATE,
			 ABSENCE_END_DATE,
			 ACTUAL_RETURN_TO_WORK,
			 CSA_CHANGE_COMMENT
			 )
			 VALUES
			 (v_change_id,
			 v_ins_change_note,
			 CURRENT_TIMESTAMP,
			 v_employee_id,
			 v_employee_name,
			 v_hr_status,
			 v_job_title,			
             v_job_adp,
             v_job_type,
			 v_manager_employee_id, 						
			 v_area_short,				
			 v_region,					
			 v_csa_notification_required,
			 v_approval_required,
			 v_manager_flag,
			 'N',
			 'ADD',
			 'Pending',
			 'Commercial',
			 'HR',
			 'Inactive',
			 v_record_complete,
			 v_service_start_date,
			 v_service_end_date,
			 v_absence_start_date,
			 v_absence_end_date,
			 v_actual_return_to_work,
			 'New Hire'
			 );
		COMMIT;

	/****Calling procedure to set csa flag****/
	CALL RAC_FS_TM_CSA_FLAG_PROCEDURE(v_change_id);

   /*Validations before inserting in tech master table*/
	BEGIN
		DECLARE CONTINUE HANDLER FOR NOT FOUND set v_job_id =null;
			SELECT 
				JOB_ID
			INTO v_job_id FROM
				RAC_FS_TM_JOB_CODE
			WHERE
				JOB_ADP_code = v_JOB_ADP
			AND v_JOB_ADP IS NOT NULL
			AND UPPER(status) = 'ACTIVE';
    END;
		
	IF v_job_id IS NULL 
		THEN  
			UPDATE RAC_FS_TM_EMPLOYEE_UPD
			   SET Change_status = 'Pending',
				   Change_note = concat(Change_note,' The entered job_adp does not exist in tech master')
			 WHERE CHANGE_ID = v_change_id;
			
			UPDATE RAC_HR_TM_EMPLOYEE_DTLS 
			SET 
				OIC_FLAG = 'Y'
			WHERE
				EMPLOYEE_ID = v_employee_id;
				
			COMMIT;

			ITERATE getNewEmployeeDetails;
	END IF;
		
	BEGIN
		DECLARE CONTINUE HANDLER FOR NOT FOUND set v_area_id =null;
			SELECT 
				AREA_ID
			INTO v_area_id FROM
				RAC_FS_TM_AREA ar,
				RAC_FS_TM_REGION reg
			WHERE
				ar.area_short_name = v_AREA_SHORT
					AND reg.region_name = v_region
					AND reg.region_id = ar.region_id
					AND v_AREA_SHORT IS NOT NULL
					AND v_region IS NOT NULL
					AND UPPER(ar.status) = 'ACTIVE'
					AND UPPER(reg.status) = 'ACTIVE';
					END;
		
		IF v_area_id IS NULL /*or v_LOCATION_CODE  IS NULL*/
		THEN  
		    UPDATE RAC_FS_TM_EMPLOYEE_UPD
			   SET Change_status = 'Pending',
				   Change_note = concat(Change_note,'The combination of entered area and region does not exist or region/area inactive')
			 WHERE CHANGE_ID = v_change_id;
			

			UPDATE RAC_HR_TM_EMPLOYEE_DTLS 
			SET 
				OIC_FLAG = 'Y'
			WHERE
				EMPLOYEE_ID = v_employee_id;
						
			COMMIT;
		
			ITERATE getNewEmployeeDetails;
			
		END IF;
		
		BEGIN
		DECLARE CONTINUE HANDLER FOR NOT FOUND set v_team_type_id =null;
			SELECT 
				TEAM_TYPE_ID
			INTO v_team_type_id FROM
				RAC_FS_TM_TEAM_TYPE
			WHERE
				team_type_name = 'Commercial';
		END;
		
		IF v_team_type_id IS NULL
		THEN  
		    UPDATE RAC_FS_TM_EMPLOYEE_UPD
			   SET Change_status = 'Pending',
				   Change_note = concat(Change_note,'The team does not exist in tech master')
			 WHERE CHANGE_ID = v_change_id;

			UPDATE RAC_HR_TM_EMPLOYEE_DTLS 
			SET 
				OIC_FLAG = 'Y'
			WHERE
				EMPLOYEE_ID = v_employee_id;
			 
			COMMIT;

			ITERATE getNewEmployeeDetails;
			
		END IF;
		
      	IF COALESCE(v_approval_required,'Y') = 'N'
		THEN
			/*The approval required is N then the record after inseeting in tech master table the change request is Processed*/	
			UPDATE RAC_FS_TM_EMPLOYEE_UPD
			SET CHANGE_STATUS = 'Approved',
				Approved = 'Y',
			# Processed_Date=CURRENT_TIMESTAMP,
				last_update_date = CURRENT_TIMESTAMP,
				last_updated_by = 'HR',
				Approved_by='HR'
			WHERE change_id=v_change_id;
		
			COMMIT;
		END IF;
	

		UPDATE RAC_HR_TM_EMPLOYEE_DTLS 
		SET 
			OIC_FLAG = 'Y'
		WHERE
			EMPLOYEE_ID = v_employee_id;
	
    END LOOP getNewEmployeeDetails;
	CLOSE newEmployee;
	
	/***Resetting value for finished***/
    SET finished =0;
	/************************************Existing************************/
	OPEN updExistingEmployee;
    
    
    updEmployee: LOOP
	
		
		FETCH updExistingEmployee 
		INTO v_employee_id1,
		v_employee_name1,
		v_fs_employee_name1,
		v_alternate_email1,
		v_tm_review_date1,
		v_email1,
		v_hr_job_title1,
		v_job_title1,
		v_hr_job_adp1,
		v_job_adp1,
        v_job_type1,
		v_hr_manager_employee_id1,
		v_manager_employee_id1,
		v_hr_area_short1,
		v_area_short1,
		v_hr_region1,
		v_region1,
		v_hr_absence_start_date1,
		v_hr_absence_end_date1,
		v_hr_actual_return_to_work1,
		v_hr_resource_number1,
		v_tm_fs_status ,
        v_hr_status1,
        v_tm_hr_status1,
        v_tm_manager_flag ,
		v_hr_service_start_date1,
		v_hr_service_end_date1,
		v_tm_service_end_date1,			 
        v_tm_record_complete,
        v_tm_team_type,
		v_tm_work_shift1,
		v_tm_CIP1,
        v_tm_Business_Org1,
        v_tm_On_call1,
        v_tm_On_site1,
		v_tm_service_advantage1,
		v_tm_production_type1,
		v_tm_dedicated1,
		v_tm_dedicated_to1,
        v_tm_ofsc_status1,
       -- v_ALTERNATE_EMAIL1,
        v_PRODUCTION_PRINT1	; 
		
        
		IF finished = 1 THEN 
			LEAVE updEmployee;
		END IF;
		
		SET v_upd_change_note='HRMS - Update. ';
		SET v_manager_chk1 = NULL;
		set v_job_id1 = NULL;
		#set v_approval_required1 = 'Y';
		
		IF (
			(
				COALESCE(v_hr_manager_employee_id1,'X') != COALESCE(v_manager_employee_id1,'X') -- and v_hr_manager_employee_id1 is not null
				AND
				COALESCE(v_tm_manager_flag,'X') != 'Y'
			)
			AND 
			(
				COALESCE(v_hr_manager_employee_id1,'X') != COALESCE(v_manager_employee_id1,'X') -- and v_hr_manager_employee_id1 is not null
				AND
				COALESCE(v_tm_Business_Org1,'X') != 'MS'
			)
		)
		THEN
			SET v_upd_change_note=concat(v_upd_change_note,'Manager Mismatch. ');
		    BEGIN
				DECLARE CONTINUE HANDLER FOR NOT FOUND 
				BEGIN
					IF v_hr_manager_employee_id1 IS NULL
					THEN
					  SET v_upd_change_note = concat(v_upd_change_note,'Manager ID: ','Manager from HRMS is NULL. ');
                    ELSE
					  SET v_upd_change_note = concat(v_upd_change_note,'Manager ID: ',v_hr_manager_employee_id1,' Employee-Manager from HRMS does not exist in TM or Manager Flag = N or Manager from HRMS is NULL. ');

					END IF;
					SET v_manager_chk1 = 'N';
					SET v_hr_manager_employee_id1 := v_manager_employee_id1;
				END;
				
				SELECT 
					'Y'
				INTO v_manager_chk1 FROM
					RAC_FS_TM_EMPLOYEE_DTLS dt
				WHERE
					employee_id = v_hr_manager_employee_id1
						AND manager_flag = 'Y';
			END;
		    
			IF (v_manager_chk1 = 'N' OR v_manager_chk1 is NULL or v_manager_chk1='')
			THEN 
				SET v_hr_manager_employee_id1=NULL;
				SET v_upd_change_note = concat(v_upd_change_note, 'Area/Region Set to null as manager not exists in TM. ');
				SET v_hr_area_short1 =null;
				SET v_hr_region1 =null;
				
				SET v_area_short1 =null; 
				SET v_region1 =null;
			ELSE
				BEGIN
					DECLARE CONTINUE HANDLER FOR NOT FOUND 
					BEGIN
						SET v_upd_change_note = concat(v_upd_change_note, 'Area/Region Set to null as not exists in TM. ');
						SET v_hr_area_short1 =null;
						SET v_hr_region1 =null;
						
						SET v_area_short1 =null;
				        SET v_region1 =null;
					END;
					
					SELECT 
						ar.AREA_ID, ar.area_short_name, re.region_name,ar.area_short_name, re.region_name
					INTO v_area_id , v_hr_area_short1 , v_hr_region1,v_area_short1,v_region1
					FROM
						RAC_FS_TM_EMPLOYEE_DTLS dt,
						RAC_FS_TM_AREA ar,
						RAC_FS_TM_REGION re
					WHERE
						employee_id = v_hr_manager_employee_id1
							AND ar.area_id = dt.area_id
							AND ar.region_id = re.region_id
							AND UPPER(ar.STATUS) = 'ACTIVE';
				END;
			END IF;
		
		END IF;
		
		
		IF COALESCE(v_hr_job_adp1,'X') != COALESCE(v_job_adp1,'X') -- and v_hr_job_adp1 is not null
		THEN
			/*Validations before inserting in tech master table*/
			SET v_upd_change_note=concat(v_upd_change_note,'Job ADP mismatch. ');
			BEGIN
			DECLARE CONTINUE HANDLER FOR NOT FOUND 
				BEGIN
					set v_job_id1 =null;
                    set v_job_type1 =null;
					set v_approval_required1 = 'Y';
            

				END;
				SELECT 
					JOB_ID,JOB_TYPE
				INTO v_job_id1,v_job_type1
				FROM
					RAC_FS_TM_JOB_CODE
				WHERE
					JOB_ADP_code = v_hr_job_adp1
						AND UPPER(status) = 'ACTIVE';
			END;
			
			IF v_job_id1 IS NULL 
			THEN  
				IF v_hr_job_adp1 IS NULL
					THEN
					  SET v_upd_change_note = concat(v_upd_change_note,'Manager ID: ','Job ADP is NULL. ');
                ELSE
				      SET v_upd_change_note = concat(v_upd_change_note,'Job ADP : ' ,v_hr_job_adp1, ' from HRMS does not exist in Tech Master.');

				END IF;
				
				set v_hr_job_title1 =NULL;					
				set v_hr_job_adp1 =NULL;
                set v_job_type1 =null;
			END IF;
		
		END IF;
		
       IF v_hr_service_end_date1 ='0000-00-00 00:00:00'
	   THEN 
	      set v_hr_service_end_date1 = null;
	   END IF;
	
	   IF v_tm_service_end_date1 ='0000-00-00 00:00:00'
	   THEN 
	      set v_tm_service_end_date1 = null;
	   END IF;
	  
	   IF COALESCE(v_hr_service_end_date1,'X') != COALESCE(v_tm_service_end_date1,'X')
	   THEN
	   
			IF v_hr_service_end_date1 IS NULL
			THEN
				SET v_upd_change_note=concat(v_upd_change_note,'Termination date is made NULL');
			ELSE
			
				IF v_hr_service_end_date1 is not null
				THEN
					SET v_upd_change_note=concat(v_upd_change_note,'Termed. Date: ',v_hr_service_end_date1);
				END IF;
		   END IF;
	   END IF;
	   
	
	   IF v_fs_employee_name1 != v_employee_name1
	   THEN
		SET v_upd_change_note=concat(v_upd_change_note,'Employee Name. Old value: ',v_fs_employee_name1,'. ');
	   END IF;
       
       IF v_tm_hr_status1 != v_hr_status1
	   THEN
		SET v_upd_change_note=concat(v_upd_change_note,'HR_Status. Old value: ',v_tm_hr_status1,'. ');
	   END IF;
	   
	    
		
		/*fetching new change id for new change request*/
		SELECT 
			IF(MAX(change_id) IS NULL,
				1,
				MAX(change_id) + 1)
		INTO v_change_id1 FROM
			RAC_FS_TM_EMPLOYEE_UPD;
		  
		/*creating new change request by inserting in RAC_FS_TM_EMPLOYEE_UPD table */
		/*since record is for update of existing employee, the change type will be Update type*/  

        INSERT INTO RAC_FS_TM_EMPLOYEE_UPD
        	(CHANGE_ID,
			 CHANGE_NOTE,
			 CHANGE_EFFECTIVE_DATE ,
			 EMPLOYEE_ID,
			 EMPLOYEE_NAME,
             ALTERNATE_EMAIL,
			 REVIEW_DATE,
			 JOB_TITLE,
			 #JOB_FAMILY,
			 JOB_ADP,
             JOB_TYPE,
			 MANAGER_ID,
			 #LOC_CODE,
			 #AREA,
			 AREA,
			 REGION,
			 CSA_NOTIFICATION_REQUIRED,
			 APPROVAL_REQUIRED,
			 CHANGE_TYPE,
			 CHANGE_STATUS,
			 SERVICE_START_DATE,
			 SERVICE_END_DATE,
			 ABSENCE_START_DATE,
			 ABSENCE_END_DATE,
			 ACTUAL_RETURN_TO_WORK,
			 REQUESTED_BY,
			 FS_STATUS,
             HR_STATUS,
			 MANAGER_FLAG,
			 RECORD_COMPLETE,
			 TEAM_TYPE,
			 WORK_SHIFT,
             CIP,
             Business_Org,
             On_call,
             On_site,
             service_advantage,
             production_type,
             dedicated,
             dedicated_to,
			 OFSC_STATUS,
			-- ALTERNATE_EMAIL,
			 PRODUCTION_PRINT
			 )
			 VALUES
			 (v_change_id1,
			 v_upd_change_note,
			 CURRENT_TIMESTAMP,
			 v_employee_id1,  
			 v_employee_name1,	
             v_alternate_email1,
             v_tm_review_date1,			 
			 v_hr_job_title1,					
			 #v_hr_job_family1, 		
             v_hr_job_adp1,
             v_job_type1,
			 v_hr_manager_employee_id1,  				
			 #v_hr_location_code1,         	
			 #v_hr_area1,						
			 v_area_short1,				
			 v_region1,
			 'N',
			 v_approval_required1,
			 'UPDATE',
			 'Pending'	,
              v_hr_service_start_date1,
			  v_hr_service_end_date1,
			  v_hr_absence_start_date1,
			  v_hr_absence_end_date1,
			  v_hr_actual_return_to_work1,
              'HR',
			  v_tm_fs_status ,
              v_hr_status1,
			  v_tm_manager_flag ,
			  v_tm_record_complete,
			  v_tm_team_type ,
              v_tm_work_shift1,
			  v_tm_CIP1,
			  v_tm_Business_Org1,
			  v_tm_On_call1,
			  v_tm_On_site1,
			  v_tm_service_advantage1,
			  v_tm_production_type1,
			  v_tm_dedicated1,
			  v_tm_dedicated_to1,
              v_tm_ofsc_status1,
            --  v_ALTERNATE_EMAIL1,
              v_PRODUCTION_PRINT1			  
			 );

		/****Calling procedure to set approval flag****/
	CALL RAC_FS_TM_APPROVAL_FLAG_PROCEDURE(v_change_id1);
	
	/****Calling procedure to set csa flag****/
	CALL RAC_FS_TM_CSA_FLAG_PROCEDURE(v_change_id1);
	
	/*
   IF COALESCE(v_approval_required1,'N') = 'N'
	 THEN
		
		UPDATE RAC_FS_TM_EMPLOYEE_UPD
		SET CHANGE_STATUS = 'Approved',
           approval_required='Y',
			last_update_date = CURRENT_TIMESTAMP,
			last_updated_by = 'HR'
		WHERE change_id=v_change_id1;
		
		COMMIT;
	
	END IF;
	*/

	UPDATE RAC_HR_TM_EMPLOYEE_DTLS 
	SET 
		OIC_FLAG = 'Y'
	WHERE
		EMPLOYEE_ID = v_employee_id1;
	
    COMMIT;

              
    END LOOP updEmployee;
	CLOSE updExistingEmployee;
	
	/***Resetting value for finished***/
    SET finished =0;
	

	/*opening cursor of unProcessedRec*/
	OPEN unProcessedRec;
    
    
	/*looping cursor of new employees*/
    getunProcessedRec: LOOP
	
	FETCH unProcessedRec 
		INTO v_employee_id1;
	
	IF finished = 1 
	THEN 
			LEAVE getunProcessedRec;
	END IF;
	
	UPDATE RAC_HR_TM_EMPLOYEE_DTLS 
	SET 
		OIC_FLAG = 'Y',
		ATTRIBUTE1 = 'Not Eligible for Update'
	WHERE
		EMPLOYEE_ID = v_employee_id1;
	
	
	END LOOP getunProcessedRec;
	CLOSE unProcessedRec;

END
//
DELIMITER ;
