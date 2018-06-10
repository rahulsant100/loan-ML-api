from flask import Flask,jsonify,abort,request,render_template
import pickle as pk
import numpy as np
import pandas as pd
import json,requests
from pandas.io.json import json_normalize

random_forest = pk.load(open("classifier1.pkl","rb"))

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('call1.html')

@app.route('/api',methods=['POST'])
def get_data():
    print("Hello")
    data = request.get_json(force=True)
    print(data)
    combined = pd.DataFrame.from_dict(json_normalize(data), orient='columns')
   # data_prep = [data['Gender'],data['Married'],data['Dependent'],data['Education'],
    #             data['Self_Employed'],data['ApplicantIncome'],data['CoapplicantIncome'],
     #            data['LoanAmount'],data['Loan_Amount_Term'],data['Credit_History'],data['Property_Area']]
    #combined = np.array(data_prep)
    combined['Gender'] = combined['Gender'].map({'Male': 1, 'Female': 0})
    combined['Married'] = combined['Married'].map({'Yes': 1, 'No': 0})
    combined['Singleton'] = combined['Dependents'].map(lambda d: 1 if d=='1' else 0)
    combined['Small_Family'] = combined['Dependents'].map(lambda d: 1 if d=='2' else 0)
    combined['Large_Family'] = combined['Dependents'].map(lambda d: 1 if d=='3+' else 0)
    combined.drop(['Dependents'], axis=1, inplace=True)
    combined['Education'] = combined['Education'].map({'Graduate': 1, 'Not Graduate': 0})
    combined['Self_Employed'] = combined['Self_Employed'].map({'Yes': 1, 'No': 0})
    combined['Total_Income'] = combined['ApplicantIncome'].astype(int) + combined['CoapplicantIncome'].astype(int)
    combined.drop(['ApplicantIncome','CoapplicantIncome'], axis=1, inplace=True)
    combined['LoanAmount'] = combined['LoanAmount'].astype(int)
    combined['Debt_Income_Ratio'] = combined['Total_Income'] / combined['LoanAmount']

    combined['Loan_Amount_Term'] = combined['Loan_Amount_Term'].astype(int)

    combined['Very_Short_Term'] = combined['Loan_Amount_Term'].map(lambda t: 1 if t<=60 else 0)
    combined['Short_Term'] = combined['Loan_Amount_Term'].map(lambda t: 1 if t>60 and t<180 else 0)
    combined['Long_Term'] = combined['Loan_Amount_Term'].map(lambda t: 1 if t>=180 and t<=300  else 0)
    combined['Very_Long_Term'] = combined['Loan_Amount_Term'].map(lambda t: 1 if t>300 else 0)
    combined.drop('Loan_Amount_Term', axis=1, inplace=True)

    combined['Credit_History'] = combined['Credit_History'].astype(int)
    combined['Credit_History_Bad'] = combined['Credit_History'].map(lambda c: 1 if c == 0 else 0)
    combined['Credit_History_Good'] = combined['Credit_History'].map(lambda c: 1 if c == 1 else 0)
    combined['Credit_History_Unknown'] = combined['Credit_History'].map(lambda c: 1 if c == 2 else 0)
    combined.drop('Credit_History', axis=1, inplace=True)

    combined['Property_Rural'] = combined['Property_Area'].map(lambda d: 1 if d=='Rural' else 0)
    combined['Property_Semiurban'] = combined['Property_Area'].map(lambda d: 1 if d=='Semiurban' else 0)
    combined['Property_Urban'] = combined['Property_Area'].map(lambda d: 1 if d=='Urban' else 0)
    combined.drop('Property_Area', axis=1, inplace=True)

    y_out = random_forest.predict(combined)
    print (combined)
    if y_out == 1:
        output = "Yes"
    else:
        output = "No"

    return jsonify(output)




if __name__ == '__main__':
    app.run(port = 9000,debug = True)
