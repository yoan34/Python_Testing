from locust import HttpUser, task


class PorjectperfTest(HttpUser):
    
    @task
    def home(self):
        self.client.get('/')

    @task
    def showSummary(self):
        self.client.post('/showSummary', {"email": "john@simplylift.co"})

    @task
    def showClubs(self):
        self.client.post('/showClubs', {"email": "john@simplylift.co"})

    @task
    def book(self):
        self.client.get('book/Spring Festival/Simply Lift')

    @task
    def logout(self):
        self.client.get('/logout')