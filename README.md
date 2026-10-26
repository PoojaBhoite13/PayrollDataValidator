# Payroll Data Validator

## Project Overview
The Payroll Data Validator is a Python project that validates employee attendance and payroll information stored in CSV files. It identifies data errors and generates reports to help the HR department review employee records.

## Objectives
- Identify missing values.
- Detect duplicate employee attendance records.
- Standardize employee status and department names.
- Validate attendance dates and working days.
- Validate salary, bonus, deductions, and net pay.
- Generate reports for HR.

## Technologies Used
- Python 3
- CSV module
- Datetime module
- Git
- GitHub

## Project Files
- `employees.csv` — Sample employee data.
- `payroll_validator.py` — Python validation program.
- `business_rules.md` — Validation rules.
- `output/valid_records.csv` — Valid records.
- `output/validation_issues.csv` — Records with errors.
- `output/summary_report.txt` — Validation summary.

## How to Run
1. Install Python 3.
2. Open the project folder in VS Code.
3. Open Terminal → New Terminal.
4. Run `python payroll_validator.py`.
5. Open the output folder to view the reports.

On Windows, you can also run `py payroll_validator.py`.

## Validation Rules
The program validates required fields, duplicate records, attendance dates, employee status, working days, salary amounts, deductions, and net pay calculations.

## Expected Results
The sample CSV contains 10 employee records. The expected output is 8 valid records and 2 records requiring review.

## Limitations
This is a sample assignment using fictional data. The program identifies errors but does not automatically change incorrect salary values or make payroll decisions.


