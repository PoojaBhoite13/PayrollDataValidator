
import csv
import os
from datetime import datetime
from collections import Counter

INPUT_FILE = "employees.csv"
OUTPUT_FOLDER = "output"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

REQUIRED_FIELDS = [
    "Employee_id",
    "Employee_name",
    "Department",
    "AttendanceDate",
    "Status",
    "WorkingDays",
    "BasicSalary",
    "Bonus",
    "Deductions",
    "NetPay"
]

STATUS_MAP = {
    "p": "Present",
    "present": "Present",
    "a": "Absent",
    "absent": "Absent",
    "leave": "Leave",
    "on leave": "Leave"
}


def validate_payroll():
    # Read the CSV file
    with open(INPUT_FILE, "r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        records = list(reader)

    # Find duplicate employee ID and attendance date combinations
    duplicate_counts = Counter(
        (
            (row.get("Employee_id") or "").strip(),
            (row.get("AttendanceDate") or "").strip()
        )
        for row in records
        if (row.get("Employee_id") or "").strip()
        and (row.get("AttendanceDate") or "").strip()
    )

    valid_records = []
    issue_records = []
    issue_counts = Counter()

    for row_number, row in enumerate(records, start=2):
        issues = []

        # Rule 1: Check required fields
        for field in REQUIRED_FIELDS:
            if not (row.get(field) or "").strip():
                issues.append(f"Missing {field}")

        employee_id = (row.get("Employee_id") or "").strip()
        attendance_date = (row.get("AttendanceDate") or "").strip()

        # Rule 2: Check duplicates
        if (
            employee_id
            and attendance_date
            and duplicate_counts[(employee_id, attendance_date)] > 1
        ):
            issues.append("Duplicate employee ID and attendance date")

        # Rule 3: Validate attendance date
        if attendance_date:
            try:
                datetime.strptime(attendance_date, "%d-%m-%Y")
            except ValueError:
                issues.append("Invalid date; expected DD-MM-YYYY")

        # Rule 4: Standardize department
        department = (row.get("Department") or "").strip()

        if department:
            row["Department"] = department.upper()

        # Rule 5: Standardize employee status
        status = (row.get("Status") or "").strip().lower()

        if status:
            if status in STATUS_MAP:
                row["Status"] = STATUS_MAP[status]
            else:
                issues.append("Invalid employee status")

        # Rule 6: Validate working days
        working_days_text = (row.get("WorkingDays") or "").strip()

        if working_days_text:
            try:
                working_days = int(working_days_text)

                if working_days < 0 or working_days > 31:
                    issues.append("WorkingDays must be between 0 and 31")

            except ValueError:
                issues.append("WorkingDays must be a whole number")

        # Rule 7: Validate salary and payroll amounts
        amounts = {}
        amount_fields = [
            "BasicSalary",
            "Bonus",
            "Deductions",
            "NetPay"
        ]

        for field in amount_fields:
            value = (row.get(field) or "").strip()

            if value:
                try:
                    amounts[field] = float(value)

                    if amounts[field] < 0:
                        issues.append(f"{field} cannot be negative")

                except ValueError:
                    issues.append(f"{field} must be numeric")

        # Rule 8: Check deductions against salary
        if (
            "BasicSalary" in amounts
            and "Deductions" in amounts
            and amounts["BasicSalary"] >= 0
            and amounts["Deductions"] >= 0
            and amounts["Deductions"] >
                amounts["BasicSalary"] + amounts.get("Bonus", 0)
        ):
            issues.append("Deductions exceed salary plus bonus")

        # Rule 9: Check net pay calculation
        required_amounts = [
            "BasicSalary", "Bonus", "Deductions", "NetPay"
        ]

        if all(field in amounts for field in required_amounts):
            if all(amounts[field] >= 0 for field in required_amounts):
                expected_net_pay = (
                    amounts["BasicSalary"]
                    + amounts["Bonus"]
                    - amounts["Deductions"]
                )

                if abs(amounts["NetPay"] - expected_net_pay) > 0.01:
                    issues.append("NetPay calculation is incorrect")

        # Save valid records or issue details
        if issues:
            issue_counts.update(issues)

            issue_records.append({
                "Row_Number": row_number,
                "Employee_id": employee_id,
                "Employee_name": row.get("Employee_name", ""),
                "Issues": "; ".join(issues)
            })

        else:
            valid_records.append(row)

    # Report 1: Valid records
    with open(
        os.path.join(OUTPUT_FOLDER, "valid_records.csv"),
        "w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(file, fieldnames=REQUIRED_FIELDS)
        writer.writeheader()
        writer.writerows(valid_records)

    # Report 2: Validation issues
    issue_fields = [
        "Row_Number",
        "Employee_id",
        "Employee_name",
        "Issues"
    ]

    with open(
        os.path.join(OUTPUT_FOLDER, "validation_issues.csv"),
        "w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(file, fieldnames=issue_fields)
        writer.writeheader()
        writer.writerows(issue_records)

    # Report 3: HR summary
    with open(
        os.path.join(OUTPUT_FOLDER, "summary_report.txt"),
        "w", encoding="utf-8"
    ) as file:
        file.write("PAYROLL DATA VALIDATION REPORT\n")
        file.write("=" * 35 + "\n")
        file.write(f"Total records: {len(records)}\n")
        file.write(f"Valid records: {len(valid_records)}\n")
        file.write(f"Records with issues: {len(issue_records)}\n")
        file.write(
            f"Total issue occurrences: {sum(issue_counts.values())}\n"
        )
        file.write("\nISSUE BREAKDOWN\n")

        for issue, count in issue_counts.most_common():
            file.write(f"{issue}: {count}\n")

    print("Payroll validation completed!")
    print(f"Total records: {len(records)}")
    print(f"Valid records: {len(valid_records)}")
    print(f"Records with issues: {len(issue_records)}")
    print("Check the output folder for reports.")


if __name__ == "__main__":
    validate_payroll()
