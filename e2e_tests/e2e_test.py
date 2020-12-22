import os
from todo_app import app
import todo_app.data.trello_items as trello
from threading import Thread
import pytest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from dotenv import load_dotenv, find_dotenv

@pytest.fixture(scope='module')
def test_app():
    # Create the new board & update the board id environment variable
    file_path = find_dotenv('.env')
    load_dotenv(file_path, override=True)

    board_id = trello.create_board('e2e-test-board')
    os.environ['TRELLO_BOARD_ID'] = board_id

    # construct the new application
    application = app.create_app()
    
    # start the app in its own thread.
    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield app

    # Tear Down
    thread.join(1)
    trello.delete_board(board_id)


@pytest.fixture(scope="module")
def driver():
    with webdriver.Firefox() as driver:
        yield driver


def test_page_loads(driver, test_app):
    driver.get('http://localhost:5000/')
    assert driver.title == 'To-Do App'


def test_task_journey(driver, test_app):
    driver.get('http://localhost:5000/')
    task_name_input = driver.find_element_by_id('name-input')
    submit_button = driver.find_element_by_id('add-new-task-button')

    task_title = 'This is a test item generated by selenium driver'
    task_name_input.send_keys(task_title)
    submit_button.click()

    assert check_task_exists_with_status(driver, task_title, 'To do')
    assert not check_task_exists_with_status(driver, task_title, 'Doing')
    assert not check_task_exists_with_status(driver, task_title, 'Done')
    
    start_task_button = get_button_with_text_for_task(driver, task_title, 'Start')
    start_task_button.click()
    assert not check_task_exists_with_status(driver, task_title, 'To do')
    assert check_task_exists_with_status(driver, task_title, 'Doing')
    assert not check_task_exists_with_status(driver, task_title, 'Done')

    complete_task_button = get_button_with_text_for_task(driver, task_title, 'Complete')
    complete_task_button.click()
    assert not check_task_exists_with_status(driver, task_title, 'To do')
    assert not check_task_exists_with_status(driver, task_title, 'Doing')
    assert check_task_exists_with_status(driver, task_title, 'Done')

    delete_task_button = get_button_with_text_for_task(driver, task_title, 'Delete')
    delete_task_button.click()
    assert not check_task_exists_with_status(driver, task_title, 'To do')
    assert not check_task_exists_with_status(driver, task_title, 'Doing')
    assert not check_task_exists_with_status(driver, task_title, 'Done')


def get_button_with_text_for_task(driver, task_title, button_text):
    button = driver.find_element_by_xpath(f'//li[div/h5[text()="{task_title}"]]/a[text()="{button_text}"]')
    return button


def check_task_exists_with_status(driver, task_title, status):
    try:
        driver.find_element_by_xpath(f'//div[h2[text()="{status}"]]//h5[text()="{task_title}"]').is_displayed()
    except NoSuchElementException:
        return False
    return True