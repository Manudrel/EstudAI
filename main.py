from agents import search_agent, summarize_agent, quiz_agent


theme = input("Qual o tema que você quer estudar? ")

search_response = search_agent(theme, [])


summarize_response = summarize_agent(theme, [])


quiz_response = quiz_agent(theme, [], None)


print("Search Response: ", search_response)
print("Summarize Response: ", summarize_response)
print("Quiz Response: ", quiz_response)
