

# def check_age():
#     attempts = 1
#     entry = int(input('Enter age: '))
#     while entry < 1 or entry > 100:
#         attempts += 1
#         entry = int(input('Enter age: '))

#     print('Number of attempts = {}'.format(attempts))


# def check_age_rec(attempts = 1):
#     entry = int(input('Enter age: '))
#     while entry < 1 or entry > 100:
#         attempts += 1
#         entry = check_age_rec(attempts)
#     print('Number of attempts = {}'.format(attempts))

#     return entry


# check_age_rec()


def filtered_list():
    list = [567, 789, 123]
    filtered_list = [num for num in list if '7' in str(num)]
    print(filtered_list)

filtered_list()