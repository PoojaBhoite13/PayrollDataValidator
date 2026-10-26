# Business Rules for Payroll Data Validation

## 1. Employee ID Validation
- Employee ID cannot be blank or null.
- Employee ID must be available for every employee record.
- Employee ID must be checked along with Attendance Date to identify duplicate records.
- Records with missing Employee IDs will be reported as validation issues.

## 2. Employee Name Validation
- Employee Name cannot be blank or null.
- Employee Name must contain a value.
- Records with missing Employee Names will be reported for review.

## 3. Department Validation
- Department cannot be blank or null.
- Department names will be converted to uppercase to maintain consistency.
- For example, `IT`, `It`, and `it` will be standardized to `IT`.
- Records with missing Department values will be reported.

## 4. Attendance Date Validation
- Attendance Date cannot be blank or null.
- The date must follow the `DD-MM-YYYY` format.
- The date must be a valid calendar date.
- Invalid dates, such as `31-02-2025`, will be reported.
- Records with missing or invalid Attendance Dates will be excluded from accepted records.

## 5. Status Validation
- Status cannot be blank or null.
- Only the following standardized statuses are allowed:
  - Present
  - Absent
  - Leave
- The following alternative values will be standardized:
  - `P` or `Present` → `Present`
  - `A` or `Absent` → `Absent`
  - `Leave` or `On Leave` → `Leave`
- Status validation will be case-insensitive.
- Any status outside the accepted values will be reported as an issue.

## 6. Working Days Validation
- Working Days cannot be blank or null.
- Working Days must be a whole number.
- Working Days must be between 0 and 31.
- Negative values, decimal values, and values greater than 31 will be reported.
- Non-numeric values will be reported as validation issues.

## 7. Basic Salary Validation
- Basic Salary cannot be blank or null.
- Basic Salary must be a numeric value.
- Basic Salary cannot be negative.
- Zero salary is allowed by the current validation code, although HR may review whether it is appropriate.
- Invalid or negative salary values will be reported.

## 8. Bonus Validation
- Bonus cannot be blank or null.
- Bonus must be a numeric value.
- Bonus cannot be negative.
- Non-numeric or negative Bonus values will be reported.

## 9. Deductions Validation
- Deductions cannot be blank or null.
- Deductions must be a numeric value.
- Deductions cannot be negative.
- Deductions must not exceed Basic Salary plus Bonus.
- Records with invalid deductions will be reported for review.

## 10. Net Pay Validation
- Net Pay cannot be blank or null.
- Net Pay must be a numeric value.
- Net Pay cannot be negative.
- Net Pay must match the following formula:

**Net Pay = Basic Salary + Bonus − Deductions**

- The calculated Net Pay will be compared with the provided Net Pay.
- A difference greater than 0.01 will be reported as an incorrect Net Pay calculation.
- Records with incorrect or invalid Net Pay will be excluded from accepted records.

## 11. Required Fields and Missing Value Validation
The following columns are required and must not contain blank or null values:

1. Employee_id
2. Employee_name
3. Department
4. AttendanceDate
5. Status
6. WorkingDays
7. BasicSalary
8. Bonus
9. Deductions
10. NetPay

- Each required field will be checked for missing values.
- Every missing field will be reported with its corresponding validation issue.
- A record containing one or more missing required values will not be accepted.

## 12. Duplicate Record Validation
- The combination of Employee ID and Attendance Date must be unique.
- Records with the same Employee ID and Attendance Date will be treated as duplicates.
- All records belonging to a duplicate combination will be flagged for review.
- Records with missing Employee IDs or Attendance Dates cannot be reliably checked for duplicate combinations and will be reported under missing-value validation.

## 13. Data Type and Data Integrity Validation
- Working Days must contain a whole number.
- Basic Salary, Bonus, Deductions, and Net Pay must contain numeric values.
- Attendance Date must contain a valid date in the expected format.
- Incorrect financial values will be reported rather than automatically corrected.
- The program will standardize Department and recognized Status values.
- The original input file will not be overwritten by the validation process.

## 14. Validation Issue Reporting
- Each record will be checked against all applicable business rules.
- Multiple issues in a single record will be reported together.
- The issue report will include:
  - Original row number
  - Employee ID
  - Employee Name
  - Description of validation issues
- Issue counts will be maintained to show how frequently each type of validation problem occurs.

## 15. Accepted Records Validation
- A record will be accepted only when it passes all applicable validation rules.
- Records containing any validation issue will be excluded from the accepted records file.
- Accepted records will contain standardized Department and Status values where applicable.
- Records with validation issues must be reviewed and corrected by HR before they can be accepted.
- The program will not automatically change incorrect salary, bonus, deduction, or Net Pay amounts.

## 16. Reporting Requirements
The program will generate the following output files:

**1. Valid Records — `output/valid_records.csv`**
- Contains records that pass all validation rules.
- Includes standardized Department and Status values where applicable.

**2. Validation Issues — `output/validation_issues.csv`**
- Contains records that fail one or more validation rules.
- Includes row number, Employee ID, Employee Name, and issue descriptions.

**3. Summary Report — `output/summary_report.txt`**
- Displays the total number of input records.
- Displays the number of valid records.
- Displays the number of records containing issues.
- Displays the total number of issue occurrences.
- Provides a breakdown of issues by type.

## 17. Assumptions
- The input CSV file is named `employees.csv`.
- The input file contains the required column headers.
- The sample data represents a monthly payroll period.
- Attendance is measured in days.
- Attendance dates use the `DD-MM-YYYY` format.
- Employee ID and Attendance Date together identify a unique record.
- Working Days must be between 0 and 31.
- Net Pay is calculated as Basic Salary plus Bonus minus Deductions.
- A tolerance of 0.01 is allowed when comparing calculated and provided Net Pay.
- The program validates data quality but does not calculate attendance-based salary, taxes, or statutory deductions.
- The program does not approve, reject, or process actual payroll payments.
- Records with validation issues require HR review and correction before acceptance.

## 18. Final Objective
The objective of the Payroll Data Validator is to identify missing values, duplicate records, invalid dates, inconsistent attendance statuses, incorrect numeric values, negative payroll amounts, and Net Pay calculation errors.

The program separates valid records from records requiring review and generates a summary report to help HR maintain accurate, consistent, and reliable payroll data.