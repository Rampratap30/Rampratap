DELIMITER //
CREATE FUNCTION `RAC_FS_TM_GET_USER_NAME`(V_IN_EMPLOYEE_ID VARCHAR(150)) RETURNS varchar(4000) CHARSET latin1
BEGIN
DECLARE v_employee_name                  VARCHAR(1000);
	set v_employee_name='';
	BEGIN
	DECLARE CONTINUE HANDLER FOR NOT FOUND 
				BEGIN
					set v_employee_name=null;
				END;
				SELECT 
					employee_name
				INTO v_employee_name FROM
				RAC_FS_TM_USER_DETAILS
				WHERE
				EMPLOYEE_ID = V_IN_EMPLOYEE_ID;
	END;
IF v_employee_name != '' 
THEN
	RETURN v_employee_name;
else
	RETURN V_IN_EMPLOYEE_ID;
END IF;
END
//
DELIMITER ;