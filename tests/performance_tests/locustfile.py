from locust import HttpUser, task


class PorjectperfTest(HttpUser):
    
    @task
    def home(self):
        self.client.get('/')

    @task
    def showSummary(self):
        self.client.post('/showSummary', {"email": "club1@test.com"})

    @task
    def showClubs(self):
        self.client.post('/showClubs', {"email": "club1@test.com"})

    @task
    def book(self):
        self.client.get('book/competition1/club1')

    @task
    def logout(self):
        self.client.get('/logout')
