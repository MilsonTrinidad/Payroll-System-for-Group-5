from fpdf import FPDF

class Payslip(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 15)
        self.cell(50, 10, 'Salary Slip', 0, 0, 'L')
        self.cell(80, 10, 'XYZ Company', 0, 1, 'C')
        self.set_font('Helvetica', '', 12)
        self.cell(0, 5, '#1 Example St. Brgy xmple, San Mateo, Rizal', 0, 1, 'C')
        self.cell(0, 5, 'Var Reg. Tin: xxx-xxx-xxx', 0, 1, 'C')
    
    def employee_info(self, emp_id, emp_firstname, emp_surname, birthdate, gender, email, datehired, fromdate, todate, department, job):
        self.set_font('Helvetica', '', 12)
        self.set_y(10)
        self.cell(0, 10, f'From: {fromdate}', 0, 1, 'R')
        self.cell(0, 10, f'To: {todate}', 0, 1, 'R')

        self.set_y(40)
        self.set_x(10)
        self.cell(10, 10, f'Surname: {emp_surname}', 0, 0, 'L')
        self.set_x(135)
        self.cell(10, 10, f'Department: {department}', 0, 1, 'L')
        self.set_x(10)
        self.cell(10, 10, f'First Name: {emp_firstname}', 0, 0, 'L')
        self.set_x(135)
        self.cell(10, 10, f'Job Title: {job}', 0, 1, 'L')
        self.set_x(10)
        self.cell(10, 10, f'Birthdate: {birthdate}', 0, 0, 'L')
        self.set_x(135)
        self.cell(10, 10, f'E-mail: {email}', 0, 1, 'L')
        self.set_x(10)
        self.cell(10, 10, f'Gender: {gender}', 0, 0, 'L')
        self.set_x(135)
        self.cell(10, 10, f'Employee ID: {emp_id}', 0, 1, 'L')
        self.set_x(10)
        self.cell(10, 10, f'Date Hired: {datehired}', 0, 1, 'L')
        self.ln(10)

    def salary_comp(self, salary, taxes, deductions, sss, pagibig, philhealth, paydate,net_pay):
        # Default width of table is 190
        self.set_font('Helvetica', 'B', 12)

        self.cell(80, 10, 'Description', 1, 0, 'C')
        self.cell(55, 10, 'Earnings', 1, 0, 'C')
        self.cell(55, 10, 'Deductions', 1, 1, 'C')

        self.set_font('Helvetica', '', 12)
        self.cell(80, 10, 'Basic Salary:', 1, 0, 'C')
        self.cell(55, 10, f'{salary} php', 1, 0, 'C')
        self.cell(55, 10, '-----', 1, 1, 'C')
        self.cell(80, 10, 'Tax:', 1, 0, 'C')
        self.cell(55, 10, '-----', 1, 0, 'C')
        self.cell(55, 10, f'{taxes} php', 1, 1, 'C')
        self.cell(80, 10, 'SSS:', 1, 0, 'C')
        self.cell(55, 10, '-----', 1, 0, 'C')
        self.cell(55, 10, f'{sss} php', 1, 1, 'C')
        self.cell(80, 10, 'Pag-Ibig:', 1, 0, 'C')
        self.cell(55, 10, '-----', 1, 0, 'C')
        self.cell(55, 10, f'{pagibig} php', 1, 1, 'C')
        self.cell(80, 10, 'Philhealth:', 1, 0, 'C')
        self.cell(55, 10, '-----', 1, 0, 'C')
        self.cell(55, 10, f'{philhealth} php', 1, 1, 'C')

        self.cell(190, 10, '', 1, 1, 'C')

        self.cell(80, 10, 'Total:', 1, 0, 'C')
        self.cell(55, 10, '-----', 1, 0, 'C')
        self.cell(55, 10, f'{deductions} php', 1, 1, 'C')

        self.cell(190, 10, '', 1, 1, 'C')

        self.cell(40, 10, 'Payment Date:', 1, 0, 'C')
        self.cell(40, 10, f'{paydate}', 1, 0, 'C')
        self.cell(110, 10, f'Net Pay:', 1, 1, 'C')
        self.cell(80, 10, '', 1, 0, 'C')
        self.cell(110, 10, f'{net_pay} php', 1, 1, 'C')
