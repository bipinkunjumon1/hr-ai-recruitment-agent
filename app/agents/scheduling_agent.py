from services.calendar_service import (
    CalendarService
)


class SchedulingAgent:

    def __init__(self):

        self.calendar = (
            CalendarService()
        )

    def schedule(

        self,

        candidate_name,

        candidate_email,

        start_time,

        end_time
    ):

        return (
            self.calendar
            .schedule_interview(

                candidate_name,

                candidate_email,

                start_time,

                end_time
            )
        )