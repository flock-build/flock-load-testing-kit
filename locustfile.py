from locust import FastHttpUser, task


class FlockLoadTestingKit(FastHttpUser):
    host = "https://api.deepinfra.com/v1"

    @task
    def Gryphe_MythoMax_L2_13b_turbo(self):
        self.client.post(
            url="/inference/microsoft/WizardLM-2-7B", json={"input": "Tell me a story."}
        )
