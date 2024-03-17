import json
value = """[{
"category": "Sports",
"prediction": {
"Developing Trend 1": "",
"Explanation": ".",
"Opportunities that may arise": "",
"Potential Pitfalls": ""
}
},
{
"category": "Crypto/Web3",
"prediction": {
"Developing Trend 1": "",
"Explanation": ".",
"Opportunities that may arise": "",
"Potential Pitfalls": ""
}
},
{
"category": "Entertainment",
"prediction": {
"Developing Trend 1": "",
"Explanation": ".",
"Opportunities that may arise": "",
"Potential Pitfalls": ""
}
}]"""
print(json.loads(value))
