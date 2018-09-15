"""
    use of Redis to create customer db for assignment
"""

from random import choice as rc
import login_database
import utilities

log = utilities.configure_logger('default', '../logs/customerdb_redis.log')

log.info('Connect to Redis')
r = login_database.login_redis_cloud()


def create_random_phone():
    area = rc(['206-', '360-', '425-'])
    prefix = rc(['234-', '321-', '456-', '987-'])
    suffix = rc(['1212', '2789', '3767', '4123', '5555'])
    return area + prefix + suffix


def choose_random_zip():
    return rc(['98101', '98112', '98127', '98155'])


def get_customer_data():
    while True:
        response = input('Enter a customer name, or "q" to quit: ')
        if response.lower() == 'q':
            break
        customer = 'customer:' + response
        print('Here is the phone number for', response)
        print(r.get(customer + ':telephone'))
        print('And here is the zip for', response)
        print(r.get(customer + ':zip'))


def run_example():
    """
        recall that Redis is non-persistent
    """

    try:
        names = ['Andrew', 'Peter', 'Susan', 'Pam', 'Steven', 'Charlotte']

        log.info('Caching data for each customer one by one')
        customer = 'customer:' + 'Andrew'
        r.set(customer + ':telephone', create_random_phone())
        r.set(customer + ':zip', choose_random_zip())
        log.info('Data cached for Andrew')

        customer = 'customer:' + 'Peter'
        r.set(customer + ':telephone', create_random_phone())
        r.set(customer + ':zip', choose_random_zip())
        log.info('Data cached for Peter')

        # log.info('Caching data for six customers')
        # for name in names:
        #     customer = 'customer:' + name
        #     phone = create_random_phone()
        #     zip_code = choose_random_zip()
        #     r.set(customer + ':telephone', phone)
        #     r.set(customer + ':zip', zip_code)
        #     log.info('Data cached for ', name)

        get_customer_data()

    except Exception as e:
        print(f'Redis error: {e}')


if __name__ == '__main__':
    run_example()
