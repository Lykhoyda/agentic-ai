import asyncio
from agents import Runner, trace, gen_trace_id

from search_agent import search_agent
from planner_agent import planner_agent, WebSearchItem, WebSearchPlan
from writer_agent import writer_agent, ReportData
from email_agent import email_agent

class ResearchManager:
    async def run(self, query: str):
        """ Run the deep research process, yielding the status updates and the final report """
        trace_id = gen_trace_id()
        with trace("Research trace", trace_id=trace_id):
            print(f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}")
            yield f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}"
            print("Starting research...")
            search_plan = await self.plan_searches(query)
            yield "Searches planned, starting searches..."
            search_results = await self.perform_searches(search_plan)
            yield "Searches completed, starting report..."
            report = await self.write_report(query, search_results)
            yield "Report written, sending email..."
            await self.send_email(report)
            yield "Email sent, research complete!"
            yield report.markdown_report

    async def plan_searches(self, query) -> WebSearchPlan:
        """  Plan the searches to be performed """
        print("Planning searches...")
        result = await Runner.run(
            starting_agent=planner_agent,
            input=f"Query: {query}",
        )
        print(f"Will perform {len(result.final_output.searches)} searches")
        return result.final_output_as(WebSearchPlan)

    async def perform_searches(self, search_plan) -> list[str]:
        """ Perform the searches to perform for the query """
        print("Performing searches...")

        num_completed = 0
        tasks = [asyncio.create_task(self.search(item)) for item in search_plan.searches]
        results = []

        for task in asyncio.as_completed(tasks):
            result = await task
            if result is not None:
                results.append(result)
            num_completed += 1
            print(f"Completed {num_completed} of {len(search_plan.searches)} searches")

        print("All searches completed")
        return results

    async def search(self, item: WebSearchItem) -> str | None:
        """ Perform a search for the query """
        input = f"Search: term: {item.query}, reason: {item.reason}"
        try:
            result = await Runner.run(
                starting_agent=search_agent,
                input=input,
            )
            return str(result.final_output)
        except Exception:
            return None

    async def write_report(self, query: str, search_results: list[str]) -> ReportData:
        """ Write the report for the query """
        print("Writing report...")
        input = f"Original query: {query}\n Summarized Search results: {search_results}"
        result = await Runner.run(
            starting_agent=writer_agent,
            input=input,
        )

        print("Finished writing report")
        return result.final_output_as(ReportData)

    async def send_email(self, report: ReportData) -> None:
        print("Sending email...")
        await Runner.run(
            starting_agent=email_agent,
            input=report.markdown_report,
        )
        print("Email sent")
        return report
