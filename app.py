from flask import Flask,render_template,request,session
from flask_bootstrap import Bootstrap
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plot
import os
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor


app=Flask(__name__)
bootstrap=Bootstrap(app)

app.config['SECRET_KEY']="MY_KEY"

@app.route('/')
def login():
    return render_template('index.html')

@app.route('/data',methods=['GET','POST'])
def data():
    if(request.method=='POST'):
        filename=request.form
        data=pd.read_csv(filename['path'])
        session['path']=filename['path']
        attr=[col for col in data.columns]
        attrtype=[typ for typ in data.dtypes]
        return render_template('parameters.html',paramters=[attr,attrtype])
    else:
        return render_template('parameters.html')

@app.route('/result',methods=['GET','POST'])
def result():
    if(request.method=='POST'):
        X,Y=request.form.getlist('X'),request.form.getlist('Y')
        data=pd.read_csv(session['path'])
        x,y=data[X],data[Y]
        x_train,x_test,y_train,y_test=train_test_split(x,y)
        return render_template('result.html',paramters=[linear_regressor(x_train,y_train),random_forest(x_train,y_train),decision_tree(x_train,y_train)])
    else:
        return render_template('parameters.html')

def linear_regressor(x_train,y_train):
    regressor=LinearRegression()
    regressor.fit(x_train,y_train)
    score=regressor.score(x_train,y_train)
    plot_graph(x_train,y_train,regressor,"linear")
    return score

def random_forest(x_train,y_train):
    regressor = RandomForestRegressor(n_estimators = 10, random_state = 0)
    regressor.fit(x_train,y_train)
    score=regressor.score(x_train,y_train)
    plot_graph(x_train,y_train,regressor,"random_forest")
    return score

def decision_tree(x_train,y_train):
    regressor = DecisionTreeRegressor(random_state = 0)
    regressor.fit(x_train, y_train)
    score=regressor.score(x_train,y_train)
    plot_graph(x_train,y_train,regressor,"decision_tree")
    return score


def plot_graph(x_train,y_train,regressor,name):
    plot.clf()
    plot.scatter(x_train,y_train,color="red")
    plot.plot(x_train,regressor.predict(x_train),color="blue")
    if(os.path.exists('static/plots/'+name+'.png')):
        os.remove('static/plots/'+name+'.png')
    plot.savefig('static/plots/'+name+'.png')


if(__name__=='__main__'):
	app.run()
