DELIMITER //
CREATE PROCEDURE `RAC_FS_TM_EMP_SYNC_OFSC_DATA_PROCEDURE`()
BEGIN

DECLARE finished                	INTEGER DEFAULT 0;
DECLARE v_change_id                	INTEGER DEFAULT 0;
DECLARE v_employee_id               INTEGER DEFAULT 0;
DECLARE v_alternate_email           VARCHAR(400);
DECLARE v_status                    VARCHAR(100);
DECLARE v_production_print          VARCHAR(100);

#fetch ofsc records whose values for ofsc status,alternate email or print production is updated
DECLARE eligibleEmployee 
   CURSOR FOR 
      SELECT 
		fs.employee_id,
		ofsc.alternate_email,
		ofsc.status,
		ofsc.production_print
		FROM  RAC_FS_TM_OFSC_DTLS ofsc,RAC_FS_TM_EMPLOYEE_DTLS fs,RAC_HR_TM_EMPLOYEE_DTLS hr
		WHERE hr.employee_id = fs.employee_id
		AND ofsc.resource_number = hr.resource_number
		AND upper(FS_STATUS) = 'ACTIVE'
		and ofsc.RESOURCE_NUMBER not like '%_T'
        and ofsc.resource_number!='158807_T'
		AND (COALESCE(ofsc.alternate_email,'X') != COALESCE(fs.alternate_email,'X') 
		     OR COALESCE(ofsc.status,'INACTIVE') != COALESCE(fs.ofsc_status,'INACTIVE' )
			 OR COALESCE(ofsc.production_print,'N') != COALESCE(fs.production_print,'N'));
		
DECLARE CONTINUE HANDLER 
        FOR NOT FOUND SET finished = 1;

CALL RAC_FS_TM_WRITE_LOG_MESSAGES('RAC_FS_TM_EMP_SYNC_OFSC_DATA_PROCEDURE','Begin Procedure');
	
	/*opening cursor of new employees*/
	OPEN eligibleEmployee;
    
    CALL RAC_FS_TM_WRITE_LOG_MESSAGES('RAC_FS_TM_EMP_SYNC_OFSC_DATA_PROCEDURE','Cursor eligibleEmployee Opened');	
    
	/*looping cursor of new employees*/
    getEmployeeDetails: LOOP
		
		/*fetching new employees data in variables*/
		FETCH eligibleEmployee INTO v_employee_id,v_alternate_email,v_status,v_production_print;
        CALL RAC_FS_TM_WRITE_LOG_MESSAGES('RAC_FS_TM_EMP_SYNC_OFSC_DATA_PROCEDURE',concat('Before Insert of New Employees',v_employee_id));	
        
		/*exiting loop when no records found*/
		IF finished = 1 THEN 
        CALL RAC_FS_TM_WRITE_LOG_MESSAGES('RAC_FS_TM_EMP_SYNC_OFSC_DATA_PROCEDURE','Leaving getEmployeeDetails loop');
			LEAVE getEmployeeDetails;
		END IF;
        
		
		/*fetching new change id for new change request*/
		SELECT IF (max(change_id) IS NULL,1,max(change_id)+1)  
		  INTO v_change_id
		  FROM RAC_FS_TM_EMPLOYEE_UPD;

		/*creating new change request by inserting in RAC_FS_TM_EMPLOYEE_UPD table */
		/*since record for new employee added the change type will be ADD type*/
        INSERT INTO RAC_FS_TM_EMPLOYEE_UPD
        	(CHANGE_ID,
			 CHANGE_EFFECTIVE_DATE ,
			 EMPLOYEE_ID,
			 PRODUCTION_PRINT,
			 ALTERNATE_EMAIL,
			 OFSC_STATUS,
			 APPROVAL_REQUIRED,
			 APPROVED,
			 CHANGE_TYPE,
			 CHANGE_STATUS,
			 TEAM_TYPE,
			 REQUESTED_BY,
             CREATED_BY,
             LAST_UPDATED_BY
			 )
			 VALUES
			 (v_change_id,
			 CURRENT_TIMESTAMP,
			 v_employee_id,
			 v_production_print,
			 v_alternate_email,
			 v_status,
			 'N',
			 'Y',
			 'UPDATE',
			 'Pending',
			 'Commercial',
			 'OFSC',
             'OFSC',
             'OFSC'             
			 );
			 
    COMMIT;
	

	CALL RAC_FS_TM_WRITE_LOG_MESSAGES('RAC_FS_TM_EMP_SYNC_OFSC_DATA_PROCEDURE',concat('Before Updating data into RAC_FS_TM_EMPLOYEE_DTLS for employee:',v_employee_id));
	CALL RAC_FS_TM_WRITE_LOG_MESSAGES('RAC_FS_TM_EMP_SYNC_OFSC_DATA_PROCEDURE',concat('Before Updating data into RAC_FS_TM_EMPLOYEE_DTLS for v_alternate_email:',v_alternate_email));
	CALL RAC_FS_TM_WRITE_LOG_MESSAGES('RAC_FS_TM_EMP_SYNC_OFSC_DATA_PROCEDURE',concat('Before Updating data into RAC_FS_TM_EMPLOYEE_DTLS for v_status:',v_status));
	CALL RAC_FS_TM_WRITE_LOG_MESSAGES('RAC_FS_TM_EMP_SYNC_OFSC_DATA_PROCEDURE',concat('Before Updating data into RAC_FS_TM_EMPLOYEE_DTLS for v_production_print:',v_production_print));


	/*Inserting in main tech master table*/
	Update  RAC_FS_TM_EMPLOYEE_DTLS
	Set alternate_email = v_alternate_email,
		ofsc_status = v_status,
		production_print = v_production_print
	Where employee_id=v_employee_id;
	commit;

	UPDATE RAC_FS_TM_EMPLOYEE_UPD
	SET CHANGE_STATUS = 'Processed',
		last_update_date = CURRENT_TIMESTAMP,
		last_updated_by = 'OFSC'
	WHERE change_id=v_change_id;
	
	COMMIT;
	
	CALL RAC_FS_TM_WRITE_LOG_MESSAGES('RAC_FS_TM_EMP_SYNC_OFSC_DATA_PROCEDURE',concat('After Inserting data into RAC_FS_TM_EMPLOYEE_DTLS for new employee and approval required is N, employee:',v_employee_id));
                               
	CALL RAC_FS_TM_WRITE_LOG_MESSAGES('RAC_FS_TM_EMP_SYNC_OFSC_DATA_PROCEDURE','End of getEmployeeDetails Loop');	
	
    END LOOP getEmployeeDetails;
	CLOSE eligibleEmployee;

   update RAC_FS_TM_EMPLOYEE_DTLS fs
set ofsc_last_login = (select distinct last_login from RAC_FS_TM_OFSC_DTLS ofsc,RAC_HR_TM_EMPLOYEE_DTLS hr
 where ofsc.resource_number=hr.resource_number
 and ofsc.RESOURCE_NUMBER not like '%_T%'
 AND hr.employee_id=fs.employee_id);   

commit;
 CALL RAC_FS_TM_WRITE_LOG_MESSAGES('RAC_FS_TM_EMP_SYNC_OFSC_DATA_PROCEDURE','End of Procedure');	

END
//
DELIMITER ;
