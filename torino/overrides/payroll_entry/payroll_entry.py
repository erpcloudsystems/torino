from hrms.payroll.doctype.payroll_entry.payroll_entry import PayrollEntry
import frappe
class CustomPayrollEntry(PayrollEntry):
    def get_salary_components(self, component_type):
        salary_slips = self.get_sal_slip_list(ss_status=1, as_dict=True)

        if salary_slips:
            ss = frappe.qb.DocType("Salary Slip")
            ssd = frappe.qb.DocType("Salary Detail")
            salary_components = (
                frappe.qb.from_(ss)
                .join(ssd)
                .on(ss.name == ssd.parent)
                .select(
                    ssd.salary_component,
                    ssd.amount,
                    ssd.parentfield,
                    ssd.additional_salary,
                    ssd.do_not_include_in_total,
                    ss.salary_structure,
                    ss.employee,
                )
                .where((ssd.parentfield == component_type) & (ss.name.isin([d.name for d in salary_slips])) & ssd.do_not_include_in_total == 0)
            ).run(as_dict=True)

            return salary_components
    def get_salary_slip_details(self):
        SalarySlip = frappe.qb.DocType("Salary Slip")
        SalaryDetail = frappe.qb.DocType("Salary Detail")

        return (
            frappe.qb.from_(SalarySlip)
            .join(SalaryDetail)
            .on(SalarySlip.name == SalaryDetail.parent)
            .select(
                SalarySlip.name,
                SalarySlip.employee,
                SalarySlip.salary_structure,
                SalaryDetail.salary_component,
                SalaryDetail.amount,
                SalaryDetail.parentfield,
                SalaryDetail.do_not_include_in_total,
            )
            .where(
                (SalarySlip.docstatus == 1)
                & (SalarySlip.start_date >= self.start_date)
                & (SalarySlip.end_date <= self.end_date)
                & (SalarySlip.payroll_entry == self.name)
                & (SalaryDetail.do_not_include_in_total == 0)
            )
        ).run(as_dict=True)