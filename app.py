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
from sklearn.preprocessing import LabelEncoder, OneHotEncoder


app=Flask(__name__)
Bootstrap(app)

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
        data.dropna()
        x,y=data[X],data[Y]
        x,y=Encoder(x,y,X,Y)
        x_train,x_test,y_train,y_test=train_test_split(x,y)
        return render_template('result.html',paramters=[linear_regressor(x_train,y_train,x_test,y_test),random_forest(x_train,y_train,x_test,y_test),decision_tree(x_train,y_train,x_test,y_test),len(x_train.columns),len(y_train.columns)])
    else:
        return render_template('parameters.html')

def linear_regressor(x_train,y_train,x_test,y_test):
    regressor=LinearRegression()
    regressor.fit(x_test,y_test)
    score=regressor.score(x_test,y_test)
    if(len(x_train.columns)==1 and len(y_train.columns)==1):
        plot_graph(x_test,y_test,regressor,"linear")
    else:
        clear_graph("linear")
    return score

def random_forest(x_train,y_train,x_test,y_test):
    regressor = RandomForestRegressor(n_estimators = 10, random_state = 0)
    regressor.fit(x_train,y_train)
    score=regressor.score(x_test,y_test)
    if(len(x_train.columns)==1 and len(y_train.columns)==1):
        plot_graph(x_test,y_test,regressor,"random_forest")
    else:
        clear_graph("random_forest")
    return score

def decision_tree(x_train,y_train,x_test,y_test):
    regressor = DecisionTreeRegressor(random_state = 0)
    regressor.fit(x_train, y_train)
    score=regressor.score(x_test,y_test)
    if(len(x_train.columns)==1 and len(y_train.columns)==1):
        plot_graph(x_test,y_test,regressor,"decision_tree")
    else:
        clear_graph("decision_tree")
    return score


def plot_graph(x_test,y_test,regressor,name):
    plot.clf()
    plot.scatter(x_test,y_test,color="red")
    plot.plot(x_test,regressor.predict(x_test),color="blue")
    plot.title(name)
    if(os.path.exists('static/plots/'+name+'.png')):
        os.remove('static/plots/'+name+'.png')
    plot.savefig('static/plots/'+name+'.png')

def clear_graph(name):
    if(os.path.exists('static/plots/'+name+'.png')):
        os.remove('static/plots/'+name+'.png')

def Encoder(x,y,X,Y):
    for i,r in enumerate(x.dtypes):
        if(r!=np.int64):
            print(i)
            x[X[i]]=LabelEncoder().fit_transform(x[X[i]])

    for i,r in enumerate(y.dtypes):
        if(r!=np.int64):
            print(i)
            y[Y[i]]=LabelEncoder().fit_transform(y[Y[i]])
    return x,y




if(__name__=='__main__'):
	app.run()
