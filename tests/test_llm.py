from app.llm import generate_answer


question = "Who is the CEO of Microsoft?"

evidence = """
Microsoft's official website states that Satya Nadella is
Chairman and Chief Executive Officer of Microsoft.
"""

answer = generate_answer(question, evidence)

print("\nVERITY ANSWER:")
print(answer)