DELIMITER //
CREATE PROCEDURE `RAC_FS_TM_EMP_CHANGE_SUBMIT_PROCEDURE`(IN P_IN_CHANGE_ID BIGINT(20))
BEGIN

DECLARE v_change_id                	INTEGER DEFAULT 0;
DECLARE v_CHANGE_EFFECTIVE_DATE     TIMESTAMP;
DECLARE v_EMPLOYEE_ID               BIGINT (10);
DECLARE v_employee_name             VARCHAR (450);
DECLARE v_JOB_TYPE                  VARCHAR (150);
DECLARE v_JOB_TITLE                 VARCHAR (150);
DECLARE v_JOB_FAMILY                VARCHAR (150);
DECLARE v_JOB_ADP                   VARCHAR (150);
DECLARE v_TEAM_TYPE                 VARCHAR (150);
DECLARE v_MANAGER_ID                BIGINT (10);
DECLARE v_MANAGER_FLAG              VARCHAR (30);
DECLARE v_SERVICE_START_DATE        TIMESTAMP;
DECLARE v_SERVICE_END_DATE          TIMESTAMP;
DECLARE v_WORK_SHIFT                VARCHAR (30);
DECLARE v_ON_CALL                   VARCHAR (30);
DECLARE v_CIP                       VARCHAR (30);
DECLARE v_ON_SITE                   VARCHAR (30);
DECLARE v_SERVICE_ADVANTAGE         VARCHAR (150);
DECLARE v_PRODUCTION_TYPE           VARCHAR (150);
DECLARE v_RECORD_COMPLETE           VARCHAR (150);
DECLARE v_DEDICATED                 VARCHAR (30);
DECLARE v_DEDICATED_TO              VARCHAR (150);
DECLARE v_LOC_CODE                  VARCHAR (150);
DECLARE v_AREA                      VARCHAR (150);
DECLARE v_REGION                    VARCHAR (150);
DECLARE v_PRODUCTION_PRINT          VARCHAR (10);
DECLARE v_OFSC_STATUS               VARCHAR (100);
DECLARE v_ALTERNATE_EMAIL           VARCHAR (400);
DECLARE v_CHANGE_NOTE               VARCHAR(2000);
DECLARE v_CHANGE_TYPE               VARCHAR (30);
DECLARE v_CHANGE_STATUS             VARCHAR (30);
DECLARE v_FS_STATUS                 VARCHAR (30);
DECLARE v_HR_STATUS                 VARCHAR (30);
DECLARE v_REVIEW_DATE               TIMESTAMP;
DECLARE v_REQUESTED_BY              VARCHAR (30);
DECLARE v_APPROVAL_REQUIRED         VARCHAR (30);
DECLARE v_CSA_NOTIFICATION_REQUIRED VARCHAR (30);
DECLARE v_job_id                    BIGINT (10);
DECLARE v_area_id                   BIGINT (10);
DECLARE v_team_type_id              BIGINT (10);
DECLARE v_BUSINESS_ORG              VARCHAR(150);
DECLARE v_ADMIN_NOTES               VARCHAR (4000);
DECLARE v_team_id_chk               VARCHAR (30) DEFAULT 'Y';
DECLARE v_area_id_chk               VARCHAR (30) DEFAULT 'Y';
DECLARE v_job_id_chk                VARCHAR (30) DEFAULT 'Y';
DECLARE v_Attribute1                VARCHAR (400);


    set v_team_id_chk = 'Y';
	set v_area_id_chk = 'Y';
	set v_job_id_chk ='Y';
    /*Purging log tables*/
	DELETE FROM RAC_FS_TM_LOGS
	WHERE creation_date <= DATE_ADD(CURRENT_DATE, INTERVAL -180 DAY);

	DELETE FROM RAC_FS_TM_SYNC_LOGS
	WHERE creation_date <= DATE_ADD(CURRENT_DATE, INTERVAL -180 DAY);
	

	
		SELECT CHANGE_EFFECTIVE_DATE,
	       EMPLOYEE_ID,
           EMPLOYEE_NAME,
           HR_STATUS,
		   JOB_TYPE,
		   JOB_TITLE,
		   JOB_ADP,
		   TEAM_TYPE,
		   MANAGER_ID,
		   MANAGER_FLAG,
		   ADMIN_NOTES,
		   SERVICE_START_DATE,
		   SERVICE_END_DATE,
		   WORK_SHIFT,
		   ON_CALL,
		   ON_SITE,
		   SERVICE_ADVANTAGE,
		   PRODUCTION_TYPE,
		   RECORD_COMPLETE,
		   DEDICATED,
		   DEDICATED_TO,
		   LOC_CODE,
		   AREA,
		   REGION,
		   REVIEW_DATE,
		   CHANGE_NOTE,
		   CHANGE_TYPE,
		   CHANGE_STATUS,
		   FS_STATUS,
		   REQUESTED_BY,
		   APPROVAL_REQUIRED,
		   CSA_NOTIFICATION_REQUIRED,
		   CIP,
		   ADMIN_NOTES,
           ATTRIBUTE1,
           BUSINESS_ORG
	  INTO v_CHANGE_EFFECTIVE_DATE,
	       v_EMPLOYEE_ID,
           v_EMPLOYEE_NAME,
           v_HR_STATUS,
		   v_JOB_TYPE,
		   v_JOB_TITLE,
		   v_JOB_ADP,
		   v_TEAM_TYPE,
		   v_MANAGER_ID,
		   v_MANAGER_FLAG,
		   v_ADMIN_NOTES,
		   v_SERVICE_START_DATE,
		   v_SERVICE_END_DATE,
		   v_WORK_SHIFT,
		   v_ON_CALL,
		   v_ON_SITE,
		   v_SERVICE_ADVANTAGE,
		   v_PRODUCTION_TYPE,
		   v_RECORD_COMPLETE,
		   v_DEDICATED,
		   v_DEDICATED_TO,
		   v_LOC_CODE,
		   v_AREA,
		   v_REGION,
		   v_REVIEW_DATE,
		   v_CHANGE_NOTE,
		   v_CHANGE_TYPE,
		   v_CHANGE_STATUS,
		   v_FS_STATUS,
		   v_REQUESTED_BY,
		   v_APPROVAL_REQUIRED,
		   v_CSA_NOTIFICATION_REQUIRED,
		   v_CIP,
		   v_ADMIN_NOTES,
           v_Attribute1,
           v_BUSINESS_ORG
	FROM RAC_FS_TM_EMPLOYEE_UPD
	WHERE CHANGE_ID = P_IN_CHANGE_ID
	  AND CHANGE_STATUS = 'Pending';


	/****Calling procedure to set approval flag****/
	CALL RAC_FS_TM_APPROVAL_FLAG_PROCEDURE(P_IN_CHANGE_ID);
	
	/****Calling procedure to set csa flag****/
	CALL RAC_FS_TM_CSA_FLAG_PROCEDURE(P_IN_CHANGE_ID);
	
	
   /* IF v_APPROVAL_REQUIRED = 'N' #AND   DATE_FORMAT(v_CHANGE_EFFECTIVE_DATE,"%Y-%m-%d")<=DATE_FORMAT(current_timestamp(),"%Y-%m-%d") 
	THEN
	
		UPDATE RAC_FS_TM_EMPLOYEE_UPD
		SET CHANGE_STATUS = 'Approved',
            approved = 'Y',
            approved_by = v_REQUESTED_BY,
		    #processed_date = CURRENT_DATE,
			last_update_date = CURRENT_TIMESTAMP,
			last_updated_by = v_REQUESTED_BY
		WHERE change_id=P_IN_CHANGE_ID;
		
		COMMIT;
	END IF;	*/
	IF  v_Attribute1 is null or v_Attribute1 ='' or v_Attribute1='Manager_Transfer' or( v_Attribute1 !='manager' AND v_Attribute1!='job' AND v_Attribute1!='hierarchy')
    THEN
		-- Get Job id
		BEGIN
		DECLARE CONTINUE HANDLER FOR NOT FOUND set v_job_id_chk ='N';
			SELECT JOB_ID INTO v_job_id
			 FROM RAC_FS_TM_JOB_CODE
			 WHERE JOB_ADP_code = v_JOB_ADP
			 AND upper(status) = 'ACTIVE';
		END;

		IF v_job_id_chk = 'N'
			THEN  
				UPDATE RAC_FS_TM_EMPLOYEE_UPD
				   SET Change_Note = concat(Change_Note,'The entered job_adp does not exist or inactive in tech master')
				 WHERE change_id=P_IN_CHANGE_ID;
				COMMIT;
		END IF;	
		
		-- Get area id
		BEGIN
		DECLARE CONTINUE HANDLER FOR NOT FOUND set v_area_id_chk ='N';
			SELECT AREA_ID INTO v_area_id
			 FROM RAC_FS_TM_AREA
			 WHERE area_short_name = v_AREA
			 AND upper(status) = 'ACTIVE';
		END;

		IF v_area_id_chk = 'N'
			THEN  
				UPDATE RAC_FS_TM_EMPLOYEE_UPD
				   SET Change_Note = concat(Change_Note,'The entered area does not exist or inactive in tech master')
				 WHERE change_id=P_IN_CHANGE_ID;
				COMMIT;
		END IF;


		-- Get team id
		BEGIN
		DECLARE CONTINUE HANDLER FOR NOT FOUND set v_team_id_chk ='N';
			SELECT TEAM_TYPE_ID INTO v_team_type_id
			 FROM RAC_FS_TM_TEAM_TYPE
			 WHERE team_type_name = v_TEAM_TYPE
			 AND upper(status) = 'ACTIVE';
		END;
		


		IF v_team_id_chk = 'N'
			THEN  
				UPDATE RAC_FS_TM_EMPLOYEE_UPD
				   SET Change_Note = concat(Change_Note,'The entered team type name does not exist or inactive in tech master')
				 WHERE change_id=P_IN_CHANGE_ID;
				COMMIT;
		END IF;
		
		
		BEGIN
		DECLARE CONTINUE HANDLER FOR NOT FOUND 
		BEGIN
			set v_APPROVAL_REQUIRED ='N';
		END;
			SELECT APPROVAL_REQUIRED INTO v_APPROVAL_REQUIRED
			 FROM RAC_FS_TM_EMPLOYEE_UPD
			 WHERE change_id=P_IN_CHANGE_ID;
			 COMMIT;
		END;
		
 
		BEGIN
		DECLARE CONTINUE HANDLER FOR NOT FOUND 
	  
								  
	 
												   
							  
								  
		  
	 
 
		BEGIN
										
	  
			set v_CSA_NOTIFICATION_REQUIRED ='N';
		END;
			SELECT CSA_NOTIFICATION_REQUIRED INTO v_CSA_NOTIFICATION_REQUIRED
			 FROM RAC_FS_TM_EMPLOYEE_UPD
			 WHERE change_id=P_IN_CHANGE_ID;
			 COMMIT;
		END;
		
		
		IF v_team_id_chk!='N' and v_area_id_chk!='N' and v_job_id_chk != 'N'
		THEN
            
					
			IF v_APPROVAL_REQUIRED = 'N' AND   DATE_FORMAT(v_CHANGE_EFFECTIVE_DATE,"%Y-%m-%d")=DATE_FORMAT(current_timestamp(),"%Y-%m-%d") and v_CSA_NOTIFICATION_REQUIRED ='N'
			THEN

				UPDATE  RAC_FS_TM_EMPLOYEE_DTLS
				Set   MANAGER_FLAG= IF (v_MANAGER_FLAG=NULL,MANAGER_FLAG,v_MANAGER_FLAG),
					  job_id = v_job_id ,
					  AREA_ID = v_area_id ,
					  MANAGER_ID = IF (v_MANAGER_ID=NULL,MANAGER_ID,v_MANAGER_ID),
					  TEAM_TYPE_ID = IF (v_team_type_id=NULL,TEAM_TYPE_ID,v_team_type_id),
					  SERVICE_START_DATE = IF (v_SERVICE_START_DATE=NULL,SERVICE_START_DATE,v_SERVICE_START_DATE),
					  SERVICE_END_DATE = IF (v_SERVICE_END_DATE=NULL,SERVICE_END_DATE,v_SERVICE_END_DATE),
					  WORK_SHIFT = IF (v_WORK_SHIFT=NULL,WORK_SHIFT,v_WORK_SHIFT),
					  FS_STATUS = IF (v_FS_STATUS=NULL,FS_STATUS,v_FS_STATUS),
					  CIP = IF (v_CIP=NULL,CIP,v_CIP),
					  ON_CALL = IF (v_ON_CALL=NULL,ON_CALL,v_ON_CALL),
					  ON_SITE = IF (v_ON_SITE=NULL,ON_SITE,v_ON_SITE),
					  EMPLOYEE_NAME = IF (v_EMPLOYEE_NAME=NULL,EMPLOYEE_NAME,v_EMPLOYEE_NAME),
					  HR_STATUS = IF (v_HR_STATUS=NULL,HR_STATUS,v_HR_STATUS),
					  REVIEW_DATE = IF (v_REVIEW_DATE=NULL,REVIEW_DATE,v_REVIEW_DATE),
					  DEDICATED = IF (v_DEDICATED=NULL,DEDICATED,v_DEDICATED),
					  DEDICATED_TO = IF (v_DEDICATED_TO=NULL,DEDICATED_TO,v_DEDICATED_TO),
					  SERVICE_ADVANTAGE = IF (v_SERVICE_ADVANTAGE=NULL,SERVICE_ADVANTAGE,v_SERVICE_ADVANTAGE),
					  PRODUCTION_TYPE = IF (v_PRODUCTION_TYPE=NULL,PRODUCTION_TYPE,v_PRODUCTION_TYPE),
					  RECORD_COMPLETE = IF (v_RECORD_COMPLETE=NULL,RECORD_COMPLETE,v_RECORD_COMPLETE),
					  ADMIN_NOTES = IF (v_ADMIN_NOTES=NULL,ADMIN_NOTES,v_ADMIN_NOTES),
                      BUSINESS_ORG = IF (v_BUSINESS_ORG=NULL,BUSINESS_ORG,v_BUSINESS_ORG),
					  last_update_date = CURRENT_TIMESTAMP,
					  last_updated_by = v_REQUESTED_BY
				Where employee_id=v_employee_id;

				UPDATE RAC_FS_TM_EMPLOYEE_UPD
				SET CHANGE_STATUS = 'Processed',
					Approved='Y',
					Processed_date=CURRENT_TIMESTAMP,
					last_update_date = CURRENT_TIMESTAMP,
					processed_date = CURRENT_TIMESTAMP,
					last_updated_by = v_requested_by
				WHERE change_id=P_IN_CHANGE_ID;
				
				COMMIT;
			elseif (v_APPROVAL_REQUIRED = 'N' AND DATE_FORMAT(v_CHANGE_EFFECTIVE_DATE,"%Y-%m-%d")>DATE_FORMAT(current_timestamp(),"%Y-%m-%d"))
			THEN
				 UPDATE RAC_FS_TM_EMPLOYEE_UPD
				SET CHANGE_STATUS = 'Approved',
					Approved ='Y',
					last_update_date = CURRENT_TIMESTAMP,
					#processed_date = CURRENT_TIMESTAMP,
					last_updated_by = v_requested_by
				WHERE change_id=P_IN_CHANGE_ID;
				
				COMMIT;
			END IF;
		END IF;
END IF; -- end of v_attribute1 check

END
//
DELIMITER ;
