DELIMITER //
CREATE PROCEDURE `RAC_FS_TM_EMP_UPD_PROCEUDRE`()
BEGIN

DECLARE finished                	INTEGER DEFAULT 0;
DECLARE v_change_id                	INTEGER DEFAULT 0;
DECLARE v_employee_id               BIGINT(60) DEFAULT 0;
DECLARE	v_region                    VARCHAR (150);
DECLARE	v_area_short                VARCHAR (150);
DECLARE	v_area                      VARCHAR (150);
DECLARE	v_loc_code                  VARCHAR (150);
DECLARE	v_manager_id                BIGINT(60) DEFAULT 0;
DECLARE	v_job_title                 VARCHAR (150);
DECLARE v_job_type                  VARCHAR (150);
DECLARE	v_job_adp                   VARCHAR (150);
DECLARE	v_team_type                 VARCHAR (150);
DECLARE	v_work_shift                VARCHAR (150);
DECLARE	v_on_site                   VARCHAR (150);
DECLARE	v_on_call                   VARCHAR (150);
DECLARE	v_dedicated                 VARCHAR (150);
DECLARE	v_dedicated_to              VARCHAR (150);
DECLARE	v_service_advantage         VARCHAR (150);
DECLARE	v_fs_status                 VARCHAR (150);
DECLARE	v_service_start_date        TIMESTAMP;
DECLARE	v_service_end_date          TIMESTAMP;
DECLARE	v_record_complete           VARCHAR (10);
DECLARE	v_manager_flag              VARCHAR (10);
DECLARE	v_admin_notes               VARCHAR (2000);
DECLARE	v_review_date               TIMESTAMP;
DECLARE	v_change_effective_date     TIMESTAMP;
DECLARE	v_change_status             VARCHAR (150);
DECLARE v_requested_by              VARCHAR(150);
DECLARE v_job_id                    INTEGER;
DECLARE	v_team_type_id              INTEGER;
DECLARE	v_area_id                   INTEGER;

/*fetching records from change table whose effective date is less than current date and status is approved */
DECLARE eligibleRecords 
   CURSOR FOR 
   SELECT change_id,
   employee_id,
   region,
   area,
   loc_code,
   manager_id,
   job_title,
   job_type,
   job_adp,
   team_type,
   work_shift,
   on_site,
   on_call,
   dedicated,
   dedicated_to,
   service_advantage,
   fs_status,
   service_start_date,
   service_end_date,
   record_complete,
   manager_flag,
   admin_notes,
   review_date,
   change_effective_date,
   change_status,
   requested_by
   FROM RAC_FS_TM_EMPLOYEE_UPD
   WHERE 1=1
   AND (change_effective_date <=CURRENT_DATE or change_effective_date is null)
     AND approval_required = 'Y'
     AND upper(change_status)='APPROVED'
	 ORDER BY change_effective_date asc;



	DECLARE CONTINUE HANDLER 
			FOR NOT FOUND SET finished = 1;

	DELETE FROM RAC_FS_TM_LOGS
		WHERE creation_date <= DATE_ADD(CURRENT_DATE, INTERVAL -180 DAY);
		
	COMMIT;
	CALL RAC_FS_TM_WRITE_LOG_MESSAGES('RAC_FS_TM_EMP_UPD_PROCEUDRE','Deleting record in RAC_FS_TM_LOGS table older than 180 days');

	
	/*opening cursor of new employees*/
	OPEN eligibleRecords;
    
    
	/*looping cursor of new employees*/
    allRecords: LOOP
		
		/*fetching change id of eligible records*/
		FETCH eligibleRecords INTO v_change_id,
		   v_employee_id,
		   v_region,
		   v_area,
		   v_loc_code,
		   v_manager_id,
		   v_job_title,
		   v_job_type,
		   v_job_adp,
		   v_team_type,
		   v_work_shift,
		   v_on_site,
		   v_on_call,
		   v_dedicated,
		   v_dedicated_to,
		   v_service_advantage,
		   v_fs_status,
		   v_service_start_date,
		   v_service_end_date,
		   v_record_complete,
		   v_manager_flag,
		   v_admin_notes,
		   v_review_date,
		   v_change_effective_date,
		   v_change_status,
		   v_requested_by;
        
		/*exiting loop when no records found*/
		IF finished = 1 THEN 
			LEAVE allRecords;
		END IF;
        
		SELECT JOB_ID INTO v_job_id
		 FROM RAC_FS_TM_JOB_CODE
		 WHERE  JOB_ADP_code = v_JOB_ADP
		   AND v_JOB_ADP IS NOT NULL
		   AND v_JOB_ADP != ''
		   AND upper(status)='ACTIVE';

		IF v_job_id = NULL AND (v_JOB_ADP !='' OR v_JOB_ADP IS NOT NULL) 
		THEN  
			UPDATE RAC_FS_TM_EMPLOYEE_UPD
			   SET change_status = 'E',
				   change_note = 'The entered job code does not exist in tech master'
			 WHERE change_id= v_change_id;
			   
			COMMIT;
			
            /*skipping remaining statements below in the loop*/
			ITERATE allRecords;
		END IF;
		
		SELECT AREA_ID INTO v_area_id
		 FROM RAC_FS_TM_AREA ar
		 WHERE  ar.area_short_name = v_AREA_SHORT
		   AND v_AREA_SHORT != ''
		   AND v_AREA_SHORT IS NOT NULL
		   AND UPPER(STATUS)='ACTIVE';

		IF (v_area_id = NULL ) AND (v_AREA_SHORT !='' OR v_AREA_SHORT IS NOT NULL)  
		THEN  
			UPDATE RAC_FS_TM_EMPLOYEE_UPD
			   SET change_status = 'E',
				   change_note = 'The combination of entered location_code,area,region does not exist'
			 WHERE change_id = v_change_id;
			   
			COMMIT;
			/*skipping remaining statements below in the loop*/
			ITERATE allRecords;
		END IF;
		
		SELECT team_type_id INTO v_team_type_id
		 FROM RAC_FS_TM_TEAM_TYPE
		 WHERE  team_type_name = v_team_type
		 AND v_team_type !=''
		 AND v_team_type IS NOT NULL
		 AND upper(status) = 'ACTIVE';

		IF (v_team_type_id = NULL ) AND (v_team_type!='' or v_team_type IS NOT NULL) 
		THEN  
			UPDATE RAC_FS_TM_EMPLOYEE_UPD
			   SET change_status = 'E',
				   change_note = 'The combination of entered location_code,area,region does not exist'
			 WHERE change_id = v_change_id;
			 
			COMMIT;
			/*skipping remaining statements below in the loop*/
			ITERATE allRecords;
		END IF;
		
		
		UPDATE RAC_FS_TM_EMPLOYEE_DTLS
		   SET  LOCATION_CODE= IF (v_loc_code=NULL,location_code,v_loc_code),
		   MANAGER_ID = IF (v_MANAGER_FLAG=NULL,MANAGER_FLAG,v_MANAGER_FLAG),
		   JOB_ID = IF (v_JOB_ID=NULL,JOB_ID,JOB_ID),
		   TEAM_TYPE_ID = IF (v_TEAM_TYPE_ID=NULL,TEAM_TYPE_ID,v_TEAM_TYPE_ID),
		   AREA_ID = IF (v_AREA_ID=NULL,AREA_ID,v_AREA_ID),
		   WORK_SHIFT = IF (v_WORK_SHIFT=NULL,WORK_SHIFT,v_WORK_SHIFT),
		   ON_SITE =IF (v_on_site=NULL,ON_SITE,v_on_site),
		   ON_CALL = IF (v_ON_CALL=NULL,ON_CALL,v_ON_CALL),
		   DEDICATED = IF (v_DEDICATED=NULL,DEDICATED,v_DEDICATED),
		   DEDICATED_TO = IF (v_DEDICATED_TO=NULL,DEDICATED_TO,v_DEDICATED_TO),
		   SERVICE_ADVANTAGE = IF (v_SERVICE_ADVANTAGE=NULL,SERVICE_ADVANTAGE,v_SERVICE_ADVANTAGE),
		   FS_STATUS = IF (v_FS_STATUS=NULL,FS_STATUS,v_FS_STATUS),
		   SERVICE_START_DATE =IF (v_SERVICE_START_DATE=NULL,SERVICE_START_DATE,v_SERVICE_START_DATE),
		   SERVICE_END_DATE = IF (v_SERVICE_END_DATE=NULL,SERVICE_END_DATE,v_SERVICE_END_DATE),
		   RECORD_COMPLETE = IF (v_RECORD_COMPLETE=NULL,RECORD_COMPLETE,v_RECORD_COMPLETE),
		   MANAGER_FLAG = IF (v_RECORD_COMPLETE=NULL,RECORD_COMPLETE,v_RECORD_COMPLETE),
		   ADMIN_NOTES =IF (v_ADMIN_NOTES=NULL,ADMIN_NOTES,v_ADMIN_NOTES),
		   last_update_date = CURRENT_TIMESTAMP,
		   last_updated_by = v_REQUESTED_BY
		WHERE EMPLOYEE_ID = v_employee_id;
		
		
		COMMIT;
	    

	    UPDATE RAC_FS_TM_EMPLOYEE_UPD
		   SET CHANGE_STATUS = 'Processed',
		   last_update_date = CURRENT_TIMESTAMP,
		   last_updated_by = v_REQUESTED_BY,
		   processed_date =CURRENT_TIMESTAMP
        WHERE CHANGE_ID = v_change_id;

        COMMIT;		
               
		
                
    END LOOP allRecords;
	CLOSE eligibleRecords;




END
//
DELIMITER ;
