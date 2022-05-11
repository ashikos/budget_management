user_type_admin = 1
user_type_member = 2

user_type_choices = (
    (user_type_admin, 'admin'),
    (user_type_member, 'member')
)


account_type_savings = 1
account_type_current = 2


user_type_account = (
    (account_type_savings, 'savings'),
    (account_type_current, 'current'),

)


account_type_income = 1
account_type_expanse = 2

user_type_category = (
    (account_type_income, 'income'),
    (account_type_expanse, 'expanse'),
)