from utils import vars
import traceback


def printError(driver, error, max_errors=1000):
    vars.error_cnt += 1
    print('exception nr ' + str(vars.error_cnt) + ' :(')
    print(error)
    traceback.print_exc()
    if vars.error_cnt > max_errors:
        print("error count of " + str(max_errors) + " reached!")
        driver.close()
        exit()  # failsafe in case of infinite error
