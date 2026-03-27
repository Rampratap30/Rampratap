DROP PROCEDURE `RAC_FS_TM_BULK_IMPORT_PROCEDURE`;
DELIMITER //
CREATE PROCEDURE RAC_FS_TM_BULK_IMPORT_PROCEDURE(IN P_IN_REQUEST_ID BIGINT(20))
BEGIN
DECLARE finished                	INTEGER DEFAULT 0;
DECLARE flag                        VARCHAR(10) DEFAULT 'N';
DECLARE v_change_id                	BIGINT(10) DEFAULT 0;
DECLARE v_employee_id               BIGINT(60) DEFAULT 0;
DECLARE v_employee_name             VARCHAR(200) DEFAULT NULL;
DECLARE v_employee_chk              VARCHAR(10) DEFAULT 'N';
DECLARE v_effective_date_chk        TIMESTAMP DEFAULT NULL;
DECLARE v_change_notes_chk          VARCHAR(4000) DEFAULT NULL;
DECLARE v_BULK_IMPORT_ID            BIGINT(60) DEFAULT 0;
DECLARE v_MANAGER_FLAG              VARCHAR(10) DEFAULT NULL;
DECLARE v_job_type                  VARCHAR(400) DEFAULT NULL;
DECLARE v_JOB_ADP                   VARCHAR(400) DEFAULT NULL;
DECLARE v_JOB_TITLE                 VARCHAR(400) DEFAULT NULL;
DECLARE v_LOCATION_CODE 			VARCHAR(400) DEFAULT NULL;
#DECLARE v_AREA 						VARCHAR(400) DEFAULT NULL;
DECLARE v_AREA_SHORT 				VARCHAR(400) DEFAULT NULL;
DECLARE v_REGION_NAME 				VARCHAR(400) DEFAULT NULL;
DECLARE v_MANAGER_ID 				BIGINT(60) DEFAULT 0;
DECLARE v_TEAM_TYPE_NAME   			VARCHAR(400) DEFAULT NULL;
DECLARE v_SERVICE_START_DATE 		TIMESTAMP DEFAULT NULL;
DECLARE v_SERVICE_END_DATE			TIMESTAMP DEFAULT NULL;
DECLARE v_tm_SERVICE_START_DATE     TIMESTAMP DEFAULT NULL;
DECLARE v_tm_SERVICE_END_DATE		TIMESTAMP DEFAULT NULL;
DECLARE v_WORK_SHIFT 				VARCHAR(400) DEFAULT '';
DECLARE v_FS_STATUS 				VARCHAR(400) DEFAULT 'INACTIVE';
DECLARE v_CIP 						VARCHAR(400) DEFAULT '';
DECLARE v_ON_CALL 					VARCHAR(400) DEFAULT '';
DECLARE v_ON_SITE 					VARCHAR(400) DEFAULT '';
DECLARE v_DEDICATED 				VARCHAR(400) DEFAULT '';
DECLARE v_DEDICATED_TO 				VARCHAR(400) DEFAULT '';
DECLARE v_SERVICE_ADVANTAGE 		VARCHAR(400) DEFAULT '';
DECLARE v_PRODUCTION_TYPE 			VARCHAR(400) DEFAULT '';
DECLARE v_RECORD_COMPLETE 			VARCHAR(10) DEFAULT NULL;
DECLARE v_EFFECTIVE_DATE 			TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
DECLARE v_REQUESTED_BY 				VARCHAR(400) DEFAULT 'AWS';
DECLARE v_LAST_EDITED_DATE 			TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
DECLARE v_CHANGE_NOTES 				VARCHAR(4000) DEFAULT NULL;
DECLARE v_ADMIN_NOTES 				VARCHAR(4000) DEFAULT NULL;
DECLARE v_REVIEW_DATE 				TIMESTAMP DEFAULT NULL;
DECLARE v_area_id                   BIGINT(60) DEFAULT 0;
DECLARE v_location_id               BIGINT(60) DEFAULT 0;
DECLARE v_region_id                 BIGINT(60) DEFAULT 0;
DECLARE v_job_id                    BIGINT(60) DEFAULT 0;
DECLARE v_team_type_id              BIGINT(60) DEFAULT 0;
DECLARE v_approval_required         VARCHAR(10) DEFAULT 'N';
DECLARE v_chk_job_active            VARCHAR(100) DEFAULT 'ACTIVE';
DECLARE v_chk_area_active           VARCHAR(100) DEFAULT 'ACTIVE';
DECLARE v_chk_region_active         VARCHAR(100) DEFAULT 'ACTIVE';
DECLARE v_region_area_chk           VARCHAR(10) DEFAULT 'N';
DECLARE v_location_chk              VARCHAR(10) DEFAULT 'N';
DECLARE v_job_title_chk             VARCHAR(10) DEFAULT 'N';
DECLARE v_manager_chk               VARCHAR(10) DEFAULT 'N';
DECLARE v_team_chk                  VARCHAR(10) DEFAULT 'N';
DECLARE v_team_id_chk               VARCHAR(10) DEFAULT 'N';
DECLARE v_csa_notification_flag     VARCHAR(10) DEFAULT 'N';
DECLARE v_HR_STATUS                 VARCHAR(150);
DECLARE v_OFSC_LAST_LOGIN           TIMESTAMP;
DECLARE v_PRODUCTION_PRINT          VARCHAR(150);
DECLARE v_OFSC_STATUS               VARCHAR(50);
DECLARE v_ALTERNATE_EMAIL           VARCHAR(400);
DECLARE v_ABSENCE_START_DATE        TIMESTAMP;
DECLARE v_ABSENCE_END_DATE          TIMESTAMP;
DECLARE v_ACTUAL_RETURN_TO_WORK     TIMESTAMP;
DECLARE v_tm_ABSENCE_START_DATE     TIMESTAMP;
DECLARE v_tm_ABSENCE_END_DATE       TIMESTAMP;
DECLARE v_tm_ACTUAL_RETURN_TO_WORK  TIMESTAMP;
DECLARE v_BUSINESS_ORG              VARCHAR(150);


#fetch employee records from RAC_FS_TM_BULK_IMPORT table
DECLARE employeeRecord
   CURSOR FOR 
          SELECT 
		  rftbi.BULK_IMPORT_ID,
		  rftbi.employee_id
	  FROM  RAC_FS_TM_BULK_IMPORT rftbi
	  WHERE rftbi.update_record ='Y'
		AND rftbi.request_id=P_IN_REQUEST_ID;
		
	DECLARE CONTINUE HANDLER 
        FOR NOT FOUND SET finished = 1;
        
	/*DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
    BEGIN
      UPDATE RAC_FS_TM_BULK_IMPORT
	     SET update_record = 'E',
	         UPDATE_MSG = 'Unexpected Exception in procedure'
	   WHERE REQUEST_ID = P_IN_REQUEST_ID
	     AND update_record ='Y';
	
	   COMMIT;
    END;*/


	
	
	
    /*Purging log tables*/
	DELETE FROM RAC_FS_TM_LOGS
	WHERE creation_date <= DATE_ADD(CURRENT_DATE, INTERVAL -180 DAY);

	DELETE FROM RAC_FS_TM_SYNC_LOGS
	WHERE creation_date <= DATE_ADD(CURRENT_DATE, INTERVAL -180 DAY);
    
    DELETE FROM RAC_FS_TM_BULK_IMPORT
	WHERE creation_date <= DATE_ADD(CURRENT_DATE, INTERVAL -180 DAY);
	
	
	/*opening cursor of  employees*/
	OPEN employeeRecord;
    
    

	/*looping cursor of input employees*/
    getEmployeeDetails: LOOP

		/*fetching records for input employees*/
		FETCH employeeRecord 
		 INTO v_BULK_IMPORT_ID,
		  v_EMPLOYEE_ID;
	    

		/*exiting loop when no records found*/
		IF finished = 1 THEN 
			LEAVE getEmployeeDetails;
		END IF;
		
       /*  set flag='N';
        
		BEGIN
		DECLARE CONTINUE HANDLER FOR SQLEXCEPTION 
		BEGIN
		UPDATE RAC_FS_TM_BULK_IMPORT
			SET update_record = 'E',
			UPDATE_MSG = 'Unexpected Exception'
			WHERE EMPLOYEE_ID = v_EMPLOYEE_ID
			AND REQUEST_ID = P_IN_REQUEST_ID
			AND BULK_IMPORT_ID = v_BULK_IMPORT_ID
			AND update_record ='Y';
            
		    COMMIT;
            ITERATE getEmployeeDetails;
		END;*/
        
            


				/*Setting date columns to NULL where date is like 0000-00-00 00:00:00 */
				update RAC_FS_TM_BULK_IMPORT
				set service_start_date= NULL
				where service_start_date='0000-00-00 00:00:00'
				and EMPLOYEE_ID = v_EMPLOYEE_ID
				and BULK_IMPORT_ID = v_BULK_IMPORT_ID
				and request_id= P_IN_REQUEST_ID;

				update RAC_FS_TM_BULK_IMPORT
				set service_end_date= NULL
				where service_end_date='0000-00-00 00:00:00'
				and EMPLOYEE_ID = v_EMPLOYEE_ID
				and BULK_IMPORT_ID = v_BULK_IMPORT_ID
				and request_id= P_IN_REQUEST_ID;

				update RAC_FS_TM_BULK_IMPORT
				set ofsc_last_login= NULL
				where ofsc_last_login='0000-00-00 00:00:00'
				and EMPLOYEE_ID = v_EMPLOYEE_ID
				and BULK_IMPORT_ID = v_BULK_IMPORT_ID
				and request_id= P_IN_REQUEST_ID;

				update RAC_FS_TM_BULK_IMPORT
				set effective_date= null
				where effective_date='0000-00-00 00:00:00'
				and EMPLOYEE_ID = v_EMPLOYEE_ID
				and BULK_IMPORT_ID = v_BULK_IMPORT_ID
				and request_id= P_IN_REQUEST_ID;

				update RAC_FS_TM_BULK_IMPORT
				set review_date= NULL
				where review_date='0000-00-00 00:00:00'
				and EMPLOYEE_ID = v_EMPLOYEE_ID
				and BULK_IMPORT_ID = v_BULK_IMPORT_ID
				and request_id= P_IN_REQUEST_ID;
				
				update RAC_FS_TM_BULK_IMPORT
				set absence_start_date= null
				where absence_start_date='0000-00-00 00:00:00'
				and EMPLOYEE_ID = v_EMPLOYEE_ID
				and BULK_IMPORT_ID = v_BULK_IMPORT_ID
				and request_id= P_IN_REQUEST_ID;
				
				update RAC_FS_TM_BULK_IMPORT
				set absence_end_date= null
				where absence_end_date='0000-00-00 00:00:00'
				and EMPLOYEE_ID = v_EMPLOYEE_ID
				and BULK_IMPORT_ID = v_BULK_IMPORT_ID
				and request_id= P_IN_REQUEST_ID;
				
				update RAC_FS_TM_BULK_IMPORT
				set actual_return_to_work= null
				where actual_return_to_work='0000-00-00 00:00:00'
				and EMPLOYEE_ID = v_EMPLOYEE_ID
				and BULK_IMPORT_ID = v_BULK_IMPORT_ID
				and request_id= P_IN_REQUEST_ID;
				
				COMMIT;
				
                
				/****Begin Validating input parameters****/
                IF v_EMPLOYEE_ID is null or v_EMPLOYEE_ID =''
				THEN
					UPDATE RAC_FS_TM_BULK_IMPORT
					SET UPDATE_RECORD = 'E',
						UPDATE_MSG = 'Employee_id is mandatory'
					WHERE BULK_IMPORT_ID = v_BULK_IMPORT_ID
					and BULK_IMPORT_ID = v_BULK_IMPORT_ID
					AND REQUEST_ID = P_IN_REQUEST_ID
					AND UPDATE_RECORD ='Y';
					
					COMMIT;
					/*skipping remaining statements below in the loop*/
					ITERATE getEmployeeDetails;
				END IF;	

                BEGIN
				DECLARE CONTINUE HANDLER FOR NOT FOUND set v_employee_chk ='N';
				SELECT 'Y' INTO v_employee_chk
				FROM RAC_FS_TM_EMPLOYEE_DTLS
				WHERE EMPLOYEE_ID = v_EMPLOYEE_ID;
				END;
				
				IF v_employee_chk!='Y'
				THEN
					UPDATE RAC_FS_TM_BULK_IMPORT
					SET UPDATE_RECORD = 'E',
						UPDATE_MSG = 'Not a valid Tech Master Employee'
					WHERE EMPLOYEE_ID = v_EMPLOYEE_ID
					and BULK_IMPORT_ID = v_BULK_IMPORT_ID
					AND REQUEST_ID = P_IN_REQUEST_ID
					AND UPDATE_RECORD ='Y';
					
					COMMIT;
					/*skipping remaining statements below in the loop*/
					ITERATE getEmployeeDetails;
				END IF;
					
                
				
				SELECT 
				  /*start tm and hr fields*/
				  tm.EMPLOYEE_NAME,
				  rftbi.MANAGER_FLAG,
				  rftbi.JOB_TYPE,
				  rftbi.JOB_ADP,
				  rftbi.JOB_TITLE,
				  #rftbi.LOCATION_CODE,
				  rftbi.AREA_SHORT,
				  rftbi.REGION,
				  rftbi.MANAGER_ID,
				  tm.HR_STATUS,
				  tm.ofsc_last_login,
				  tm.production_print,
				  tm.ofsc_status,
				  tm.alternate_email,
				  /*end tm and hr fields*/
				  /*start tm fields*/
				  rftbi.ABSENCE_START_DATE,
				  tm.ABSENCE_START_DATE,
				  rftbi.ABSENCE_END_DATE,
				  tm.ABSENCE_END_DATE,
				  rftbi.ACTUAL_RETURN_TO_WORK,
				  tm.ACTUAL_RETURN_TO_WORK,
				  rftbi.TEAM_TYPE_NAME,
				  rftbi.SERVICE_START_DATE,
				  tm.SERVICE_START_DATE,
				  rftbi.SERVICE_END_DATE,
				  tm.SERVICE_END_DATE,
				  rftbi.WORK_SHIFT,
				  rftbi.FS_STATUS,
				  rftbi.CIP,
				  rftbi.ON_CALL,
				  rftbi.ON_SITE,
				  rftbi.DEDICATED,
				  rftbi.DEDICATED_TO,
				  rftbi.SERVICE_ADVANTAGE,
				  rftbi.PRODUCTION_TYPE,
				  rftbi.RECORD_COMPLETE,
				  rftbi.BUSINESS_ORG,
				  /*end tm fields*/
				  /*start change request fields*/
				  rftbi.EFFECTIVE_DATE,
				  rftbi.REQUESTED_BY,
				  rftbi.LAST_EDITED_DATE,
				  rftbi.CHANGE_NOTES,
				  rftbi.ADMIN_NOTES,
				  rftbi.REVIEW_DATE,
				  rftbi.bulk_import_id
				  /*end change request fields*/
				  INTO 
				  v_employee_name,
				  v_MANAGER_FLAG,
				  v_JOB_TYPE,
				  v_JOB_ADP,
				  v_JOB_TITLE,
				  #v_LOCATION_CODE,
				  #v_AREA,
				  v_AREA_SHORT,
				  v_REGION_NAME,
				  v_MANAGER_ID,
				  v_HR_STATUS,
				  v_OFSC_LAST_LOGIN,
				  v_PRODUCTION_PRINT,
				  v_OFSC_STATUS,
				  v_ALTERNATE_EMAIL,
				  v_ABSENCE_START_DATE,
				  v_tm_ABSENCE_START_DATE,
				  v_ABSENCE_END_DATE,
				  v_tm_ABSENCE_END_DATE,
				  v_ACTUAL_RETURN_TO_WORK,
				  v_tm_ACTUAL_RETURN_TO_WORK,
				  v_TEAM_TYPE_NAME,
				  v_SERVICE_START_DATE,
				  v_tm_SERVICE_START_DATE,
				  v_SERVICE_END_DATE,
				  v_tm_SERVICE_END_DATE,
				  v_WORK_SHIFT,
				  v_FS_STATUS,
				  v_CIP,
				  v_ON_CALL,
				  v_ON_SITE,
				  v_DEDICATED,
				  v_DEDICATED_TO,
				  v_SERVICE_ADVANTAGE,
				  v_PRODUCTION_TYPE,
				  v_RECORD_COMPLETE,
				  v_BUSINESS_ORG,
				  v_EFFECTIVE_DATE,
				  v_REQUESTED_BY,
				  v_LAST_EDITED_DATE,
				  v_CHANGE_NOTES,
				  v_ADMIN_NOTES,
				  v_REVIEW_DATE,
				  v_BULK_IMPORT_ID
			  FROM  RAC_FS_TM_BULK_IMPORT rftbi,
					RAC_FS_TM_EMPLOYEE_DTLS tm
			  WHERE rftbi.employee_id = tm.employee_id
				AND rftbi.update_record ='Y'
				AND rftbi.employee_id=v_EMPLOYEE_ID
				and rftbi.BULK_IMPORT_ID = v_BULK_IMPORT_ID
				AND rftbi.request_id=P_IN_REQUEST_ID;
				
				
				IF v_EFFECTIVE_DATE IS NULL OR v_CHANGE_NOTES IS NULL OR v_EFFECTIVE_DATE ='' OR v_CHANGE_NOTES=''
				THEN
					UPDATE RAC_FS_TM_BULK_IMPORT
					SET update_record = 'E',
						UPDATE_MSG = 'effective_date and change_notes is mandatory'
					WHERE EMPLOYEE_ID = v_EMPLOYEE_ID
					and BULK_IMPORT_ID = v_BULK_IMPORT_ID
					AND REQUEST_ID = P_IN_REQUEST_ID
					AND update_record ='Y';
					
					COMMIT;
					/*skipping remaining statements below in the loop*/
					ITERATE getEmployeeDetails;
				END IF;		
				
				IF  DATE_FORMAT(v_EFFECTIVE_DATE,"%Y-%m-%d")<DATE_FORMAT(current_timestamp(),"%Y-%m-%d")
				THEN
				   UPDATE RAC_FS_TM_BULK_IMPORT
					SET update_record = 'E',
						UPDATE_MSG = 'Change effective date cannot be past date'
					WHERE EMPLOYEE_ID = v_EMPLOYEE_ID
					and BULK_IMPORT_ID = v_BULK_IMPORT_ID
					AND REQUEST_ID = P_IN_REQUEST_ID
					AND update_record ='Y';
					
					COMMIT;
					/*skipping remaining statements below in the loop*/
					ITERATE getEmployeeDetails;
				END IF;

                

				IF v_AREA_SHORT is null or v_AREA_SHORT='' or v_REGION_NAME is null or v_REGION_NAME='' 
				THEN
				   UPDATE RAC_FS_TM_BULK_IMPORT
					   SET update_record = 'E',
						   UPDATE_MSG = 'Area_short and  region name  are manadatory fields'
					 WHERE EMPLOYEE_ID = v_EMPLOYEE_ID
					   AND REQUEST_ID = P_IN_REQUEST_ID
					   AND BULK_IMPORT_ID = v_BULK_IMPORT_ID
					   AND update_record ='Y';
					COMMIT;
					
					/*skipping remaining statements below in the loop*/
					ITERATE getEmployeeDetails;
				END IF;
				
				/*IF v_LOCATION_CODE is null or v_LOCATION_CODE =''
				THEN
				   UPDATE RAC_FS_TM_BULK_IMPORT
					   SET update_record = 'E',
						   UPDATE_MSG = 'Location code is manadatory field'
					 WHERE EMPLOYEE_ID = v_EMPLOYEE_ID
					   AND REQUEST_ID = P_IN_REQUEST_ID
					   AND BULK_IMPORT_ID = v_BULK_IMPORT_ID
					   AND update_record ='Y';
					COMMIT;
					
					ITERATE getEmployeeDetails;
				END IF;*/
				
				
				IF v_MANAGER_ID is null or v_MANAGER_ID ='' or v_MANAGER_ID =0
				THEN
				   UPDATE RAC_FS_TM_BULK_IMPORT
					   SET update_record = 'E',
						   UPDATE_MSG = 'Manager_employee_id is manadatory field'
					 WHERE EMPLOYEE_ID = v_EMPLOYEE_ID
					   AND REQUEST_ID = P_IN_REQUEST_ID
					   AND BULK_IMPORT_ID = v_BULK_IMPORT_ID
					   AND update_record ='Y';
					COMMIT;
					
					/*skipping remaining statements below in the loop*/
					ITERATE getEmployeeDetails;
				ELSE
							  BEGIN
							  DECLARE CONTINUE HANDLER FOR NOT FOUND set v_manager_chk ='N';
								  SELECT 'Y' INTO v_manager_chk
								   FROM RAC_FS_TM_EMPLOYEE_DTLS
								  WHERE employee_id=v_manager_id
								   AND manager_flag='Y';	
                              END;
							  
							  IF upper(v_manager_chk) ='N'
							   THEN
									UPDATE RAC_FS_TM_BULK_IMPORT
									   SET update_record = 'E',
										   UPDATE_MSG = 'Not a valid manager in Tech Master'
									 WHERE EMPLOYEE_ID = v_EMPLOYEE_ID
									   AND REQUEST_ID = P_IN_REQUEST_ID
									   AND BULK_IMPORT_ID = v_BULK_IMPORT_ID
									   AND update_record ='Y';
									COMMIT;
									
									/*skipping remaining statements below in the loop*/
									ITERATE getEmployeeDetails;	
							  END IF;
				END IF;
				
				IF v_MANAGER_FLAG is null or v_MANAGER_FLAG =''
				THEN
					UPDATE RAC_FS_TM_BULK_IMPORT
					SET update_record = 'E',
						UPDATE_MSG = 'Manager Flag is mandatory'
					WHERE BULK_IMPORT_ID = v_BULK_IMPORT_ID
					AND REQUEST_ID = P_IN_REQUEST_ID
					AND EMPLOYEE_ID = v_EMPLOYEE_ID
					AND update_record ='Y';
					
					COMMIT;
					/*skipping remaining statements below in the loop*/
					ITERATE getEmployeeDetails;
				ELSE
				   IF upper(v_MANAGER_FLAG) !='Y' AND upper(v_MANAGER_FLAG) !='N'
				   THEN
						 UPDATE RAC_FS_TM_BULK_IMPORT
						SET update_record = 'E',
							UPDATE_MSG = 'Manager Flag can be Y/N'
						WHERE BULK_IMPORT_ID = v_BULK_IMPORT_ID
						AND REQUEST_ID = P_IN_REQUEST_ID
						AND EMPLOYEE_ID = v_EMPLOYEE_ID
						AND update_record ='Y';
					
						COMMIT;
						/*skipping remaining statements below in the loop*/
						ITERATE getEmployeeDetails;
					END IF;
				END IF;	
				
				/*IF v_BUSINESS_ORG is null or v_BUSINESS_ORG =''
				THEN
				   UPDATE RAC_FS_TM_BULK_IMPORT
					   SET update_record = 'E',
						   UPDATE_MSG = 'Business_Org is manadatory field'
					 WHERE EMPLOYEE_ID = v_EMPLOYEE_ID
					   AND REQUEST_ID = P_IN_REQUEST_ID
					   AND BULK_IMPORT_ID = v_BULK_IMPORT_ID
					   AND update_record ='Y';
					COMMIT;
					
					ITERATE getEmployeeDetails;
				END IF;*/
				
				IF v_BUSINESS_ORG != 'TS' AND  v_BUSINESS_ORG != 'MS' AND v_BUSINESS_ORG != 'RPPS' and v_BUSINESS_ORG is not null and v_BUSINESS_ORG !=''
				THEN
				   UPDATE RAC_FS_TM_BULK_IMPORT
					   SET update_record = 'E',
						   UPDATE_MSG = 'Business_Org value can only be TS, MS or RPPS'
					 WHERE EMPLOYEE_ID = v_EMPLOYEE_ID
					   AND REQUEST_ID = P_IN_REQUEST_ID
					   AND BULK_IMPORT_ID = v_BULK_IMPORT_ID
					   AND update_record ='Y';
					COMMIT;
					
					ITERATE getEmployeeDetails;
				END IF;
				
			

				IF (v_WORK_SHIFT != '1st'  AND v_WORK_SHIFT != '2nd' AND v_WORK_SHIFT != '3rd' AND v_WORK_SHIFT !='' and v_WORK_SHIFT IS NOT NULL)
				   THEN
						UPDATE RAC_FS_TM_BULK_IMPORT
						   SET update_record = 'E',
							   UPDATE_MSG = 'Work shift value can only be 1st,2nd or 3rd'
						 WHERE EMPLOYEE_ID = v_EMPLOYEE_ID
						   AND REQUEST_ID = P_IN_REQUEST_ID
						   AND BULK_IMPORT_ID = v_BULK_IMPORT_ID
						   AND update_record ='Y';
						COMMIT;
						
						/*skipping remaining statements below in the loop*/
						ITERATE getEmployeeDetails;	
				END IF;
				
				
				IF (v_ON_CALL!= 'Y' AND v_ON_CALL!= 'N' AND v_ON_CALL != '' AND v_ON_CALL IS NOT NULL)
				   THEN
						UPDATE RAC_FS_TM_BULK_IMPORT
						   SET update_record = 'E',
							   UPDATE_MSG = 'On Call value can be Y or N'
						 WHERE EMPLOYEE_ID = v_EMPLOYEE_ID
						   AND REQUEST_ID = P_IN_REQUEST_ID
						   AND BULK_IMPORT_ID = v_BULK_IMPORT_ID
						   AND update_record ='Y';
						COMMIT;
						
						/*skipping remaining statements below in the loop*/
						ITERATE getEmployeeDetails;	
				END IF;
				
				IF (v_ON_SITE != 'Y' AND v_ON_SITE != 'N' AND v_ON_SITE IS NOT NULL AND v_ON_SITE != '')
				   THEN
						UPDATE RAC_FS_TM_BULK_IMPORT
						   SET update_record = 'E',
							   UPDATE_MSG = 'On Site value can be Y or N or NULL'
						 WHERE EMPLOYEE_ID = v_EMPLOYEE_ID
						   AND REQUEST_ID = P_IN_REQUEST_ID
						   AND BULK_IMPORT_ID = v_BULK_IMPORT_ID
						   AND update_record ='Y';
						COMMIT;
						
						/*skipping remaining statements below in the loop*/
						ITERATE getEmployeeDetails;	
				END IF;
				
				IF (v_DEDICATED != 'Y' AND v_DEDICATED != 'N' AND v_DEDICATED != '' AND v_DEDICATED IS NOT NULL)
				   THEN
						UPDATE RAC_FS_TM_BULK_IMPORT
						   SET update_record = 'E',
							   UPDATE_MSG = 'Dedicated value can be Y or N'
						 WHERE EMPLOYEE_ID = v_EMPLOYEE_ID
						   AND REQUEST_ID = P_IN_REQUEST_ID
						   AND BULK_IMPORT_ID = v_BULK_IMPORT_ID
						   AND update_record ='Y';
						COMMIT;
						
						/*skipping remaining statements below in the loop*/
						ITERATE getEmployeeDetails;	
				END IF;
				
				IF (v_SERVICE_ADVANTAGE != 'Y' AND v_SERVICE_ADVANTAGE != 'N' AND v_SERVICE_ADVANTAGE != '' AND v_SERVICE_ADVANTAGE IS NOT NULL)
				   THEN
						UPDATE RAC_FS_TM_BULK_IMPORT
						   SET update_record = 'E',
							   UPDATE_MSG = 'Service Advantage can be Y or N'
						 WHERE EMPLOYEE_ID = v_EMPLOYEE_ID
						   AND REQUEST_ID = P_IN_REQUEST_ID
						   AND BULK_IMPORT_ID = v_BULK_IMPORT_ID
						   AND update_record ='Y';
						COMMIT;
						
						/*skipping remaining statements below in the loop*/
						ITERATE getEmployeeDetails;	
				END IF;
				
				IF v_DEDICATED = 'Y'
				THEN
				   IF v_DEDICATED_TO ='' OR v_DEDICATED_TO IS NULL 
				   THEN
				       UPDATE RAC_FS_TM_BULK_IMPORT
						   SET update_record = 'E',
							   UPDATE_MSG = 'Dedicated to is mandatory if dedicated is Y'
						 WHERE EMPLOYEE_ID = v_EMPLOYEE_ID
						   AND REQUEST_ID = P_IN_REQUEST_ID
						   AND BULK_IMPORT_ID = v_BULK_IMPORT_ID
						   AND update_record ='Y';
						COMMIT;
						
						/*skipping remaining statements below in the loop*/
						ITERATE getEmployeeDetails;	
				   END IF;
				END IF;
				
				
				IF v_TEAM_TYPE_NAME is null or v_TEAM_TYPE_NAME =''
				THEN
					UPDATE RAC_FS_TM_BULK_IMPORT
					SET update_record = 'E',
						UPDATE_MSG = 'Team_type_name is manadatory'
					WHERE BULK_IMPORT_ID = v_BULK_IMPORT_ID
					AND REQUEST_ID = P_IN_REQUEST_ID
					AND EMPLOYEE_ID = v_EMPLOYEE_ID
					AND update_record ='Y';
					
					COMMIT;
					/*skipping remaining statements below in the loop*/
					ITERATE getEmployeeDetails;
				ELSE
				         
							  BEGIN
							  DECLARE CONTINUE HANDLER FOR NOT FOUND set v_team_chk ='N';
								  SELECT 'Y',team_type_id INTO v_team_chk,v_team_type_id
								   FROM RAC_FS_TM_TEAM_TYPE
								  WHERE team_type_name= v_TEAM_TYPE_NAME
								   AND upper(status)='ACTIVE';	
                              END;
							  
							  IF upper(v_team_chk) !='Y'
							   THEN
									UPDATE RAC_FS_TM_BULK_IMPORT
									   SET update_record = 'E',
										   UPDATE_MSG = 'Not an ACTIVE or valid team type'
									 WHERE EMPLOYEE_ID = v_EMPLOYEE_ID
									   AND REQUEST_ID = P_IN_REQUEST_ID
									   AND BULK_IMPORT_ID = v_BULK_IMPORT_ID
									   AND update_record ='Y';
									COMMIT;
									
									/*skipping remaining statements below in the loop*/
									ITERATE getEmployeeDetails;	
							  END IF;
				END IF;	
				
				BEGIN
				  DECLARE CONTINUE HANDLER FOR NOT FOUND set v_team_id_chk ='N';
					  SELECT 'Y' INTO v_team_id_chk
					   FROM RAC_FS_TM_TEAM_TYPE
					  WHERE team_type_name= v_TEAM_TYPE_NAME;	
				 END;
				 
				 IF v_team_id_chk !='Y'
				 THEN
				    UPDATE RAC_FS_TM_BULK_IMPORT
					SET update_record = 'E',
					UPDATE_MSG = 'Not a valid Team type in Tech master'
					WHERE BULK_IMPORT_ID = v_BULK_IMPORT_ID
						AND REQUEST_ID = P_IN_REQUEST_ID
						AND EMPLOYEE_ID = v_EMPLOYEE_ID
						AND update_record ='Y';
					
					COMMIT;
					/*skipping remaining statements below in the loop*/
					ITERATE getEmployeeDetails;
				 END IF;
				
				IF v_FS_STATUS is null or v_FS_STATUS =''
				THEN
					UPDATE RAC_FS_TM_BULK_IMPORT
					SET update_record = 'E',
						UPDATE_MSG = 'FS_STATUS flag is manadatory'
					WHERE BULK_IMPORT_ID = v_BULK_IMPORT_ID
					AND REQUEST_ID = P_IN_REQUEST_ID
					AND EMPLOYEE_ID = v_EMPLOYEE_ID
					AND update_record ='Y';
					
					COMMIT;
					/*skipping remaining statements below in the loop*/
					ITERATE getEmployeeDetails;
				ELSE
				   IF upper(v_FS_STATUS) !='ACTIVE' AND upper(v_FS_STATUS) !='INACTIVE' AND upper(v_FS_STATUS) !='LOA'
				   THEN
						 UPDATE RAC_FS_TM_BULK_IMPORT
						SET update_record = 'E',
							UPDATE_MSG = 'FS_STATUS can be ACTIVE/INACTIVE'
						WHERE BULK_IMPORT_ID = v_BULK_IMPORT_ID
						AND REQUEST_ID = P_IN_REQUEST_ID
						AND EMPLOYEE_ID = v_EMPLOYEE_ID
						AND update_record ='Y';
					
					COMMIT;
					/*skipping remaining statements below in the loop*/
					ITERATE getEmployeeDetails;
				   END IF;
				END IF;	
				
				IF v_RECORD_COMPLETE is null or v_RECORD_COMPLETE =''
				THEN
					UPDATE RAC_FS_TM_BULK_IMPORT
					SET update_record = 'E',
						UPDATE_MSG = 'RECORD_COMPLETE flag is manadatory'
					WHERE BULK_IMPORT_ID = v_BULK_IMPORT_ID
					AND REQUEST_ID = P_IN_REQUEST_ID
					AND EMPLOYEE_ID = v_EMPLOYEE_ID
					AND update_record ='Y';
					
					COMMIT;
					/*skipping remaining statements below in the loop*/
					ITERATE getEmployeeDetails;
				ELSE
				   IF v_RECORD_COMPLETE  !='Y' AND v_RECORD_COMPLETE !='N' 
				   THEN
						 UPDATE RAC_FS_TM_BULK_IMPORT
						SET update_record = 'E',
							UPDATE_MSG = 'RECORD_COMPLETE can be Y/N'
						WHERE BULK_IMPORT_ID = v_BULK_IMPORT_ID
						AND REQUEST_ID = P_IN_REQUEST_ID
						AND EMPLOYEE_ID = v_EMPLOYEE_ID
						AND update_record ='Y';
					
					COMMIT;
					/*skipping remaining statements below in the loop*/
					ITERATE getEmployeeDetails;
				   END IF;
				END IF;	
				
				IF v_SERVICE_START_DATE is null or v_SERVICE_START_DATE =''
				THEN
					UPDATE RAC_FS_TM_BULK_IMPORT
					   SET update_record = 'E',
							UPDATE_MSG = 'Service start date is mandatory'
					 WHERE BULK_IMPORT_ID = v_BULK_IMPORT_ID
				       AND REQUEST_ID = P_IN_REQUEST_ID
					   AND EMPLOYEE_ID = v_EMPLOYEE_ID
					   AND update_record ='Y';
					COMMIT;
					/*skipping remaining statements below in the loop*/
					ITERATE getEmployeeDetails;
				END IF;
				
				IF COALESCE(DATE_FORMAT(v_tm_SERVICE_START_DATE,"%Y-%m-%d"),'X') != COALESCE(DATE_FORMAT(v_SERVICE_START_DATE,"%Y-%m-%d"),'X') AND v_SERVICE_START_DATE IS NOT NULL
				THEN
					IF DATE_FORMAT(v_SERVICE_START_DATE,"%Y-%m-%d") < DATE_FORMAT(CURRENT_TIMESTAMP(),"%Y-%m-%d")
					THEN
						UPDATE RAC_FS_TM_BULK_IMPORT
					   SET update_record = 'E',
							UPDATE_MSG = 'Service Start Date cannot be past date'
					 WHERE BULK_IMPORT_ID = v_BULK_IMPORT_ID
				       AND REQUEST_ID = P_IN_REQUEST_ID
					   AND EMPLOYEE_ID = v_EMPLOYEE_ID
					   AND update_record ='Y';
					COMMIT;
					/*skipping remaining statements below in the loop*/
					ITERATE getEmployeeDetails;
					END IF;
				END IF;
				
				
				IF COALESCE(DATE_FORMAT(v_tm_SERVICE_END_DATE,"%Y-%m-%d"),'X') != COALESCE(DATE_FORMAT(v_SERVICE_END_DATE,"%Y-%m-%d"),'X') AND v_SERVICE_END_DATE IS NOT NULL
				THEN
					IF DATE_FORMAT(v_SERVICE_END_DATE,"%Y-%m-%d") < DATE_FORMAT(CURRENT_TIMESTAMP(),"%Y-%m-%d")
					THEN
						UPDATE RAC_FS_TM_BULK_IMPORT
					   SET update_record = 'E',
							UPDATE_MSG = 'Service End Date cannot be past date'
					 WHERE BULK_IMPORT_ID = v_BULK_IMPORT_ID
				       AND REQUEST_ID = P_IN_REQUEST_ID
					   AND EMPLOYEE_ID = v_EMPLOYEE_ID
					   AND update_record ='Y';
					COMMIT;
					/*skipping remaining statements below in the loop*/
					ITERATE getEmployeeDetails;
					END IF;
				END IF;
				
				IF COALESCE(DATE_FORMAT(v_tm_ABSENCE_START_DATE,"%Y-%m-%d"),'X') != COALESCE(DATE_FORMAT(v_ABSENCE_START_DATE,"%Y-%m-%d"),'X') AND v_ABSENCE_START_DATE IS NOT NULL
				THEN
					IF DATE_FORMAT(v_ABSENCE_START_DATE,"%Y-%m-%d") < DATE_FORMAT(CURRENT_TIMESTAMP(),"%Y-%m-%d")
					THEN
						UPDATE RAC_FS_TM_BULK_IMPORT
					   SET update_record = 'E',
							UPDATE_MSG = 'Absence Start Date cannot be past date'
					 WHERE BULK_IMPORT_ID = v_BULK_IMPORT_ID
				       AND REQUEST_ID = P_IN_REQUEST_ID
					   AND EMPLOYEE_ID = v_EMPLOYEE_ID
					   AND update_record ='Y';
					COMMIT;
					/*skipping remaining statements below in the loop*/
					ITERATE getEmployeeDetails;
					END IF;
				END IF;
				
				IF COALESCE(DATE_FORMAT(v_tm_ABSENCE_END_DATE,"%Y-%m-%d"),'X') != COALESCE(DATE_FORMAT(v_ABSENCE_END_DATE,"%Y-%m-%d"),'X') AND v_ABSENCE_END_DATE IS NOT NULL
				THEN
					IF DATE_FORMAT(v_ABSENCE_END_DATE,"%Y-%m-%d") < DATE_FORMAT(CURRENT_TIMESTAMP(),"%Y-%m-%d")
					THEN
						UPDATE RAC_FS_TM_BULK_IMPORT
					   SET update_record = 'E',
							UPDATE_MSG = 'Absence End Date cannot be past date'
					 WHERE BULK_IMPORT_ID = v_BULK_IMPORT_ID
				       AND REQUEST_ID = P_IN_REQUEST_ID
					   AND EMPLOYEE_ID = v_EMPLOYEE_ID
					   AND update_record ='Y';
					COMMIT;
					/*skipping remaining statements below in the loop*/
					ITERATE getEmployeeDetails;
					END IF;
				END IF;
				
				IF COALESCE(DATE_FORMAT(v_tm_ACTUAL_RETURN_TO_WORK,"%Y-%m-%d"),'X')  != COALESCE(DATE_FORMAT(v_ACTUAL_RETURN_TO_WORK,"%Y-%m-%d"),'X') AND v_ACTUAL_RETURN_TO_WORK IS NOT NULL
				THEN
					IF DATE_FORMAT(v_ACTUAL_RETURN_TO_WORK,"%Y-%m-%d") < DATE_FORMAT(CURRENT_TIMESTAMP(),"%Y-%m-%d")
					THEN
						UPDATE RAC_FS_TM_BULK_IMPORT
					   SET update_record = 'E',
							UPDATE_MSG = 'Actual Return to Work cannot be past date'
					 WHERE BULK_IMPORT_ID = v_BULK_IMPORT_ID
				       AND REQUEST_ID = P_IN_REQUEST_ID
					   AND EMPLOYEE_ID = v_EMPLOYEE_ID
					   AND update_record ='Y';
					COMMIT;
					/*skipping remaining statements below in the loop*/
					ITERATE getEmployeeDetails;
					END IF;
				END IF;
				
				
			
				
				IF v_JOB_ADP is null or v_JOB_ADP ='' or v_JOB_TITLE is null or v_JOB_TITLE =''
				THEN
					UPDATE RAC_FS_TM_BULK_IMPORT
					SET update_record = 'E',
						UPDATE_MSG = 'Job ADP and Job Title is mandatory'
					WHERE BULK_IMPORT_ID = v_BULK_IMPORT_ID
					AND REQUEST_ID = P_IN_REQUEST_ID
					AND EMPLOYEE_ID = v_EMPLOYEE_ID
					AND update_record ='Y';
					
					COMMIT;
					/*skipping remaining statements below in the loop*/
					ITERATE getEmployeeDetails;
				END IF;	
				
				BEGIN
				DECLARE CONTINUE HANDLER FOR NOT FOUND set v_job_id =0;
				SELECT JOB_ID INTO v_job_id
				 FROM RAC_FS_TM_JOB_CODE
				 WHERE JOB_ADP_code = v_JOB_ADP
				   and v_JOB_ADP is not null and v_JOB_ADP !='';
				END;

				IF v_job_id = 0
				THEN  
					UPDATE RAC_FS_TM_BULK_IMPORT
					   SET update_record = 'E',
						   UPDATE_MSG = 'The entered job_adp does not exist in tech master'
					 WHERE EMPLOYEE_ID = v_EMPLOYEE_ID
					   AND REQUEST_ID = P_IN_REQUEST_ID
					   AND BULK_IMPORT_ID = v_BULK_IMPORT_ID
					   AND update_record ='Y';
					COMMIT;
					
					/*skipping remaining statements below in the loop*/
					ITERATE getEmployeeDetails;
				ELSE
				
				  BEGIN
				  DECLARE CONTINUE HANDLER FOR NOT FOUND set v_chk_job_active ='INACTIVE';
				  SELECT upper(STATUS)
					INTO v_chk_job_active
					FROM RAC_FS_TM_JOB_CODE
				   WHERE job_id = v_job_id
                     AND upper(status) = 'ACTIVE';
				  END;
				  
				  IF (
				  upper(v_chk_job_active) = 'INACTIVE'
				  AND
				  upper(v_FS_STATUS) ='ACTIVE'
				  )
				  THEN
				  
					UPDATE RAC_FS_TM_BULK_IMPORT
					   SET update_record = 'E',
						   UPDATE_MSG = 'The Job code used is INACTIVE'
					 WHERE EMPLOYEE_ID = v_EMPLOYEE_ID
					   AND REQUEST_ID = P_IN_REQUEST_ID
					   AND BULK_IMPORT_ID = v_BULK_IMPORT_ID
					   AND update_record ='Y';
					COMMIT;
					/*skipping remaining statements below in the loop*/
					ITERATE getEmployeeDetails;
				
				  ELSE 
				  
				    BEGIN
				    DECLARE CONTINUE HANDLER FOR NOT FOUND set v_job_title_chk ='N';
						SELECT 'Y' INTO v_job_title_chk
						 FROM RAC_FS_TM_JOB_CODE
						WHERE job_id = v_job_id
						  AND job_title = v_JOB_TITLE;					
				    END;
					
				    IF v_job_title_chk != 'Y'
					THEN
					   UPDATE RAC_FS_TM_BULK_IMPORT
					   SET update_record = 'E',
						   UPDATE_MSG = 'The Job ADP and Job Title combination does not exist'
					 WHERE EMPLOYEE_ID = v_EMPLOYEE_ID
					   AND REQUEST_ID = P_IN_REQUEST_ID
					   AND BULK_IMPORT_ID = v_BULK_IMPORT_ID
					   AND update_record ='Y';
					   COMMIT;
					/*skipping remaining statements below in the loop*/
					ITERATE getEmployeeDetails;
					END IF;
				  END IF;
				
				END IF;


                BEGIN
				DECLARE CONTINUE HANDLER FOR NOT FOUND set v_area_id =0;
					SELECT AREA_ID INTO v_area_id
					  FROM RAC_FS_TM_AREA ar
					 WHERE  ar.area_short_name = v_AREA_SHORT
					   AND v_AREA_SHORT!=''
					   AND v_AREA_SHORT IS NOT NULL;
				END;
				

				IF v_area_id = 0  
				THEN  
					UPDATE RAC_FS_TM_BULK_IMPORT
					   SET update_record = 'E',
						   UPDATE_MSG = 'The  entered area_short not exist'
					 WHERE EMPLOYEE_ID = v_EMPLOYEE_ID
					   AND REQUEST_ID = P_IN_REQUEST_ID
					   AND update_record ='Y'
					   AND BULK_IMPORT_ID = v_BULK_IMPORT_ID;
					   
					COMMIT;
					/*skipping remaining statements below in the loop*/
					ITERATE getEmployeeDetails;
					
				ELSE
				
				  BEGIN
				  DECLARE CONTINUE HANDLER FOR NOT FOUND set v_chk_area_active ='INACTIVE';
					  SELECT upper(STATUS)
						INTO v_chk_area_active
						FROM RAC_FS_TM_AREA
					   WHERE area_id = v_area_id
                       AND upper(status) = 'ACTIVE';
				  END;
				  
				  IF v_chk_area_active = 'INACTIVE'
				  THEN
				  
					UPDATE RAC_FS_TM_BULK_IMPORT
					   SET update_record = 'E',
						   UPDATE_MSG = 'The Area used is INACTIVE'
					 WHERE EMPLOYEE_ID = v_EMPLOYEE_ID
					   AND REQUEST_ID = P_IN_REQUEST_ID
					   AND BULK_IMPORT_ID = v_BULK_IMPORT_ID
					   AND update_record ='Y';
					COMMIT;
					/*skipping remaining statements below in the loop*/
					ITERATE getEmployeeDetails;
				  ELSE
				        BEGIN
						DECLARE CONTINUE HANDLER FOR NOT FOUND set v_region_id =0;
							SELECT REGION_ID INTO v_region_id
							  FROM RAC_FS_TM_REGION ar
							 WHERE  ar.region_name = v_region_name
							   AND v_region_name!=''
							   AND v_region_name IS NOT NULL;
						END;

						IF v_region_id = 0  
						THEN  
							UPDATE RAC_FS_TM_BULK_IMPORT
							   SET update_record = 'E',
								   UPDATE_MSG = 'The  entered region does not exist'
							 WHERE EMPLOYEE_ID = v_EMPLOYEE_ID
							   AND REQUEST_ID = P_IN_REQUEST_ID
							   AND update_record ='Y'
							   AND BULK_IMPORT_ID = v_BULK_IMPORT_ID;
							   
							COMMIT;
							/*skipping remaining statements below in the loop*/
							ITERATE getEmployeeDetails;
							
						ELSE
						
						      BEGIN
							  DECLARE CONTINUE HANDLER FOR NOT FOUND set v_chk_region_active ='INACTIVE';
								  SELECT upper(STATUS) 
									INTO v_chk_region_active
									FROM RAC_FS_TM_REGION
								   WHERE region_id = v_region_id
                                   AND upper(status) = 'ACTIVE';
							  END;
							  
							  IF v_chk_region_active = 'INACTIVE'
							  THEN
							  
								UPDATE RAC_FS_TM_BULK_IMPORT
								   SET update_record = 'E',
									   UPDATE_MSG = 'The Region used is INACTIVE'
								 WHERE EMPLOYEE_ID = v_EMPLOYEE_ID
								   AND REQUEST_ID = P_IN_REQUEST_ID
								   AND BULK_IMPORT_ID = v_BULK_IMPORT_ID
								   AND update_record ='Y';
								COMMIT;
								/*skipping remaining statements below in the loop*/
								ITERATE getEmployeeDetails;
								
							  ELSE
							  
							  /*If region and area both are active*/
							  BEGIN
							  DECLARE CONTINUE HANDLER FOR NOT FOUND set v_region_area_chk ='N';
								  SELECT 'Y' INTO v_region_area_chk
								   FROM RAC_FS_TM_AREA
								  WHERE area_id=v_area_id
								   AND region_id =v_region_id;	
                              END;
							  
							  IF v_region_area_chk != 'Y'
							   THEN
								  UPDATE RAC_FS_TM_BULK_IMPORT
								   SET update_record = 'E',
									   UPDATE_MSG = 'The Region Area combination used is INACTIVE'
								 WHERE EMPLOYEE_ID = v_EMPLOYEE_ID
								   AND REQUEST_ID = P_IN_REQUEST_ID
								   AND BULK_IMPORT_ID = v_BULK_IMPORT_ID
								   AND update_record ='Y';
								COMMIT;
								/*skipping remaining statements below in the loop*/
								ITERATE getEmployeeDetails;
							   END IF;
					  
							 END IF; #end of region inactive
				        END IF; #end of region id not null
				  END IF; #end of area inactive
				END IF; #end of area id null
				/*BEGIN
				  DECLARE CONTINUE HANDLER FOR NOT FOUND set v_chk_area_active ='INACTIVE';
			    SELECT 'Y' INTO v_location_chk
				  FROM RAC_FS_TM_LOC loc
				 WHERE  loc.location_code = v_LOCATION_CODE
				   AND INACTIVE_DATE IS NULL;
				   
				IF v_location_chk != 'Y'
				THEN
					  UPDATE RAC_FS_TM_BULK_IMPORT
					   SET update_record = 'E',
						   UPDATE_MSG = 'The Location_code is either not present in Tech Master or is inactive'
					 WHERE EMPLOYEE_ID = v_EMPLOYEE_ID
					   AND REQUEST_ID = P_IN_REQUEST_ID
					   AND BULK_IMPORT_ID = v_BULK_IMPORT_ID
					   AND update_record ='Y';
					COMMIT;
					ITERATE getEmployeeDetails;
				END IF; */
					

				IF v_area_id = 0  
				THEN  
					UPDATE RAC_FS_TM_BULK_IMPORT
					   SET update_record = 'E',
						   UPDATE_MSG = 'The  entered area_short not exist'
					 WHERE EMPLOYEE_ID = v_EMPLOYEE_ID
					   AND REQUEST_ID = P_IN_REQUEST_ID
					   AND update_record ='Y'
					   AND BULK_IMPORT_ID = v_BULK_IMPORT_ID;
					   
					COMMIT;
					/*skipping remaining statements below in the loop*/
					ITERATE getEmployeeDetails;
				END IF;	
			/****End Validating input parameters****/
		#END; 
        
		/*IF (flag='Y')
        THEN
			UPDATE RAC_FS_TM_BULK_IMPORT
			SET update_record = 'E',
			UPDATE_MSG = 'Unexpected Exception'
			WHERE EMPLOYEE_ID = v_EMPLOYEE_ID
			AND REQUEST_ID = P_IN_REQUEST_ID
			AND BULK_IMPORT_ID = v_BULK_IMPORT_ID
			AND update_record ='Y';
            
		    COMMIT;
            ITERATE getEmployeeDetails;
		END IF;		
		*/
		
		/*fetching new change id for new change request*/
		SELECT IF (max(change_id) IS NULL,1,max(change_id)+1)  
		  INTO v_change_id
		  FROM RAC_FS_TM_EMPLOYEE_UPD;

		/*creating new change request by inserting in RAC_FS_TM_EMPLOYEE_UPD table */
        INSERT INTO RAC_FS_TM_EMPLOYEE_UPD
        	(CHANGE_ID,
			 CHANGE_EFFECTIVE_DATE ,
			 EMPLOYEE_ID,
			 EMPLOYEE_NAME,
			 --
			 MANAGER_FLAG,
		     JOB_ADP,
			 JOB_TYPE,
		     JOB_TITLE,
		    # LOC_CODE,
		     #AREA,
		     AREA,
		     REGION,
		     MANAGER_ID,
			 TEAM_TYPE,
			 SERVICE_START_DATE,
			 SERVICE_END_DATE,
			 WORK_SHIFT,
			 FS_STATUS,
			 HR_STATUS,
			 OFSC_STATUS,
			 PRODUCTION_PRINT,
			 ALTERNATE_EMAIL,
			 ABSENCE_START_DATE,
			 ABSENCE_END_DATE,
			 ACTUAL_RETURN_TO_WORK,
			 CIP,
			 ON_CALL,
			 ON_SITE,
			 DEDICATED,
			 DEDICATED_TO,
			 SERVICE_ADVANTAGE,
			 PRODUCTION_TYPE,
			 RECORD_COMPLETE,
			 REQUESTED_BY,
			 LAST_EDITED_DATE,
			 CHANGE_NOTE,
			 ADMIN_NOTES,
			 REVIEW_DATE,
			 --
             LAST_EDITED_BY,
			 APPROVAL_REQUIRED,
			 APPROVED,
			 CHANGE_TYPE,
			 CHANGE_STATUS,
			 ATTRIBUTE5,
			 BUSINESS_ORG
			 )
			 VALUES
			 (v_change_id,
			  v_EFFECTIVE_DATE,
			  v_employee_id,
			  v_employee_name,
			 --
			  v_MANAGER_FLAG,
		      v_JOB_ADP,
			  v_JOB_TYPE,
		      v_JOB_TITLE,
		      #v_LOCATION_CODE,
		      #v_AREA,
		      v_AREA_SHORT,
		      v_REGION_NAME,
		      v_MANAGER_ID,
			  v_TEAM_TYPE_NAME,
			  v_SERVICE_START_DATE,
			  v_SERVICE_END_DATE,
			  v_WORK_SHIFT,
			  v_FS_STATUS,
			  v_HR_STATUS,
			  v_OFSC_STATUS,
			  v_PRODUCTION_PRINT,
			  v_ALTERNATE_EMAIL,
			  v_ABSENCE_START_DATE,
			  v_ABSENCE_END_DATE,
			  v_ACTUAL_RETURN_TO_WORK,
			  v_CIP,
			  v_ON_CALL,
			  v_ON_SITE,
			  v_DEDICATED,
			  v_DEDICATED_TO,
			  v_SERVICE_ADVANTAGE,
			  v_PRODUCTION_TYPE,
			  v_RECORD_COMPLETE,
			  v_REQUESTED_BY,
			  v_LAST_EDITED_DATE,
			  v_CHANGE_NOTES,
			  v_ADMIN_NOTES,
			  v_REVIEW_DATE,
			 --
			  v_requested_by,
			  'N',
			  'N',
			  'UPDATE',
			  'Pending',
			  P_IN_REQUEST_ID,
			  v_BUSINESS_ORG
			 );
	
			UPDATE RAC_FS_TM_BULK_IMPORT
			   SET update_record = 'S',
				   UPDATE_MSG = concat('The change request created successfully.Change id',v_change_id)
			 WHERE EMPLOYEE_ID = v_EMPLOYEE_ID
			   AND REQUEST_ID = P_IN_REQUEST_ID
               AND update_record ='Y'
			   AND BULK_IMPORT_ID = v_BULK_IMPORT_ID;
			   
	
    COMMIT;
	
	
	
    /****Calling procedure to set approval flag****/
	CALL RAC_FS_TM_APPROVAL_FLAG_PROCEDURE(v_change_id);
	
	/****Calling procedure to set csa flag****/
	CALL RAC_FS_TM_CSA_FLAG_PROCEDURE(v_change_id);
	
	#CALL RAC_FS_TM_WRITE_LOG_MESSAGES('RAC_FS_TM_BULK_IMPORT_PROCEDURE',concat('Before Updating data into RAC_FS_TM_EMPLOYEE_DTLS for employee:',v_employee_id));
    
	BEGIN
	DECLARE CONTINUE HANDLER FOR NOT FOUND set v_approval_required ='Y';
		SELECT APPROVAL_REQUIRED INTO v_approval_required 
		 FROM RAC_FS_TM_EMPLOYEE_UPD
		 WHERE CHANGE_ID = v_change_id;
	END;
	
	BEGIN
	DECLARE CONTINUE HANDLER FOR NOT FOUND set v_csa_notification_flag ='N';
		SELECT CSA_NOTIFICATION_REQUIRED INTO v_csa_notification_flag 
		 FROM RAC_FS_TM_EMPLOYEE_UPD
		 WHERE CHANGE_ID = v_change_id;
	END;
	
	IF v_approval_required = 'N' AND   DATE_FORMAT(v_EFFECTIVE_DATE,"%Y-%m-%d")=DATE_FORMAT(current_timestamp(),"%Y-%m-%d") and v_csa_notification_flag ='N'
	THEN
		
		UPDATE  RAC_FS_TM_EMPLOYEE_DTLS
		Set   MANAGER_FLAG= IF (v_MANAGER_FLAG=NULL,MANAGER_FLAG,v_MANAGER_FLAG),
			  job_id = v_job_id ,
			  AREA_ID = v_area_id ,
			  #LOCATION_CODE = v_LOCATION_CODE,
			  #REGION_ID = v_region_id,
			  MANAGER_ID = IF (v_MANAGER_ID=NULL,MANAGER_ID,v_MANAGER_ID),
			  TEAM_TYPE_ID = IF (v_team_type_id=NULL,TEAM_TYPE_ID,v_team_type_id),
			  SERVICE_START_DATE = IF (v_SERVICE_START_DATE=NULL,SERVICE_START_DATE,v_SERVICE_START_DATE),
			  SERVICE_END_DATE = IF (v_SERVICE_END_DATE=NULL,SERVICE_END_DATE,v_SERVICE_END_DATE),
			  WORK_SHIFT = IF (v_WORK_SHIFT=NULL,WORK_SHIFT,v_WORK_SHIFT),
			  FS_STATUS = IF (v_FS_STATUS=NULL,FS_STATUS,v_FS_STATUS),
			  ABSENCE_START_DATE = IF (v_ABSENCE_START_DATE=NULL,ABSENCE_START_DATE,v_ABSENCE_START_DATE),
			  ABSENCE_END_DATE = IF (v_ABSENCE_END_DATE=NULL,ABSENCE_END_DATE,v_ABSENCE_END_DATE),
			  ACTUAL_RETURN_TO_WORK = IF (v_ACTUAL_RETURN_TO_WORK=NULL,ACTUAL_RETURN_TO_WORK,v_ACTUAL_RETURN_TO_WORK),
			  CIP = IF (v_CIP=NULL,CIP,v_CIP),
              REVIEW_DATE = IF (v_REVIEW_DATE = NULL,REVIEW_DATE,v_REVIEW_DATE),
			  ON_CALL = IF (v_ON_CALL=NULL,ON_CALL,v_ON_CALL),
			  ON_SITE = IF (v_ON_SITE=NULL,ON_SITE,v_ON_SITE),
			  DEDICATED = IF (v_DEDICATED=NULL,DEDICATED,v_DEDICATED),
			  DEDICATED_TO = IF (v_DEDICATED_TO=NULL,DEDICATED_TO,v_DEDICATED_TO),
			  SERVICE_ADVANTAGE = IF (v_SERVICE_ADVANTAGE=NULL,SERVICE_ADVANTAGE,v_SERVICE_ADVANTAGE),
			  PRODUCTION_TYPE = IF (v_PRODUCTION_TYPE=NULL,PRODUCTION_TYPE,v_PRODUCTION_TYPE),
			  RECORD_COMPLETE = IF (v_RECORD_COMPLETE=NULL,RECORD_COMPLETE,v_RECORD_COMPLETE),
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
		WHERE change_id=v_change_id;
		
		COMMIT;
	elseif (v_approval_required = 'N' AND DATE_FORMAT(v_EFFECTIVE_DATE,"%Y-%m-%d")>DATE_FORMAT(current_timestamp(),"%Y-%m-%d"))
    THEN
	     UPDATE RAC_FS_TM_EMPLOYEE_UPD
		SET CHANGE_STATUS = 'Approved',
		    Approved ='Y',
			last_update_date = CURRENT_TIMESTAMP,
			#processed_date = CURRENT_TIMESTAMP,
			last_updated_by = v_requested_by
		WHERE change_id=v_change_id;
		
		COMMIT;
	END IF;
	
    END LOOP getEmployeeDetails;
	CLOSE employeeRecord;

END
//
DELIMITER ;
