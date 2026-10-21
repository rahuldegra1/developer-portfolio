class Employee:
    nums_of_emps = 0
    raise_amt = 1.04

    def __init__(self, first, last, pay):
        self.first = first
        self.last = last
        self.pay = pay
        self.email = first + "" + last + "@company.com"

        Employee.nums_of_emps += 1

    def fullname(self):
        return "{} {}".format(self.first, self.last)

    def apply_raise(self):
        self.pay = int(self.pay * self.raise_amount)

    def __repr__(self):
        return "Employee('{}', '{}', {})".format(self.first, self.last, self.pay)

    def __str__(self):
        return "{} - {}".format(self.fullname(), self.email)

    def __add__(self, other):
        return self.pay + other.pay


emp_1 = Employee(
    "Haery",
    "Schafer",
    50000,
)
emp_2 = Employee(
    "Arthur",
    "morgan",
    60000,
)


print(emp_1 + emp_2)


# print(emp_1.__repr__())
# print(emp_1.__str__())


# mgr_1 = Manager('Sue', 'Smith', 90000, [emp_1])


# print(mgr_1.email)
# mgr_1.add_emp(emp_2)
# mgr_1.remove_emp(emp_1)
# mgr_1.print_emps()


# class Developer(Employee):
#     def __init__(self, first, last, pay, prog_lang):
#         super().__init__(first, last, pay)
#         self.prog_lang = prog_lang

# class Manager(Employee):
#     def __init__(self, first, last, pay, employees=None):
#             super().__init__(first, last, pay)
#             if employees is None:
#                  self.employees = []
#             else:
#                  self.employees = employees

#     def add_emp(self, emp):
#          if emp not in self.employees:
#               self.employees.append(emp)

#     def remove_emp(self, emp):
#          if emp in self.employees:
#               self.employees.remove(emp)

#     def print_emps(self):
#          for emp in self.employees:
#               print('-->', emp.fullname())

# print(emp_1.email)
# print(emp_1.prog_lang)
