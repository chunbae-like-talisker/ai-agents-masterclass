from crewai.flow.flow import Flow, listen, start, router, and_, or_
from pydantic import BaseModel


class MyFirstFlowState(BaseModel):
    user_id: int = 1
    is_admin: bool = False


class MyFirstFlow(Flow[MyFirstFlowState]):
    @start()
    def first(self):
        print(self.state.user_id)
        print("Hello")

    @listen(first)
    def second(self):
        self.state.user_id = 2
        print("World")

    @listen(first)
    def third(self):
        print("!")

    @listen(and_(second, third))
    def final(self):
        print(":)")

    @router(final)
    def route(self):
        if self.state.is_admin:
            return "Even"
        else:
            return "Odd"

    @listen("Even")
    def handle_even(self):
        print("Handle even")

    @listen("Odd")
    def handle_odd(self):
        print("Handle odd")


flow = MyFirstFlow()

flow.plot()
flow.kickoff()
