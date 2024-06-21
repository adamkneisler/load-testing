import os
from locust import HttpLocust, TaskSet, task
import requests
from bs4 import BeautifulSoup
import dryscrape
import webkit_server

class IFrame(TaskSet):
    """
    Class to handle simulating requests to MSL iFrame
    """
    
    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        self.BASE_URL = "https://example.com"
        self.start_session()
    
    def start_session(self):
        """
        Start headless browser session
        """
        dryscrape.start_xvfb()
        self.server = webkit_server.Server()
        server_conn = webkit_server.ServerConnection(server=self.server)
        driver = dryscrape.driver.webkit.Driver(connection=server_conn)
        self.session = dryscrape.Session(driver=driver)
        
    
    @task(1)
    def get_locations(self):
        """
        Task to simulate page render for locations
        """
        self.start_session()
        
        path = "/example?path=locations"
        url = self.BASE_URL + path

        # Load url in headless browser
        self.session.visit(url)
        self.session.reset()

        # Get rendered page
        page = BeautifulSoup(self.session.body(), 'lxml')

        # Kill server for task
        self.server.kill()

        # Make base request to path in locust client
        self.client.get(path)
    