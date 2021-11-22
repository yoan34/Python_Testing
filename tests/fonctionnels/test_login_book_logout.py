import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox import service
from selenium.webdriver.firefox.service import Service


service = Service(rf"{os.path.dirname(os.path.realpath(__file__))}/geckodriver")
browser = webdriver.Firefox(service=service)

def test_login_booking_logout():
    """
    - test la connection avec une adresse email
    - test d'affichage de la liste des clubs.
    - test d'affichage de la liste des compétitions.
    - test de réservation de 10 places.
    - test logout.
    """
    browser.get('http://0.0.0.0:5000')
    email = browser.find_element(By.NAME, 'email')
    email.send_keys('club1@test.com')
    assert browser.find_element(By.TAG_NAME, "h1").text == 'Welcome to the GUDLFT Registration Portal!'

    enter_btn = browser.find_element(By.TAG_NAME, 'button')
    enter_btn.click()
    assert browser.current_url == 'http://0.0.0.0:5000/showSummary'
    assert browser.find_element(By.TAG_NAME, "h2").text == 'Welcome, club1@test.com'

    show_clubs = browser.find_element(By.TAG_NAME, 'button')
    show_clubs.click()
    assert browser.current_url == 'http://0.0.0.0:5000/showClubs'
    assert browser.find_element(By.TAG_NAME, 'h3').text == 'Clubs:'

    show_competitions = browser.find_element(By.TAG_NAME, 'button')
    show_competitions.click()
    assert browser.find_element(By.TAG_NAME, 'h3').text == 'Competitions:'

    link_competition = browser.find_element(By.CLASS_NAME, 'competition1')
    link_competition.click()
    assert browser.find_element(By.TAG_NAME, 'h2').text == 'competition1'

    places = browser.find_element(By.NAME, 'places')
    places.send_keys(10)
    book = browser.find_element(By.TAG_NAME, 'button')
    book.click()
    assert 'Great-booking complete!' in browser.find_element(By.CSS_SELECTOR, 'ul li').text

    logout = browser.find_element(By.CLASS_NAME, 'logout')
    logout.click()
    assert browser.find_element(By.TAG_NAME, "h1").text == 'Welcome to the GUDLFT Registration Portal!'
    browser.quit()



    
