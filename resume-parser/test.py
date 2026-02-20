from parser import ResumeParser

parser = ResumeParser()
result = parser.parse_file("sample_resume.pdf")

print(result)