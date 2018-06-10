import requests,json
url = "http://localhost:9000/api"
data  = json.dumps({'Gender':'Male','Married':'Yes','Dependents':0,'Education':'Graduate',
                   'Self_Employed':'No','ApplicantIncome':5720,'CoapplicantIncome':0,
                    'LoanAmount':110,'Loan_Amount_Term':360,'Credit_History':1,
                    'Property_Area':'Urban'})
r = requests.post(url,data)
print(r.json())