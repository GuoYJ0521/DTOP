from flask import request
from .forms import PropertyForm
import time

def k_predict():
    property1, property2, property3, property4 = None, None, None, None
    operation = None
    properties = None
    status = 0

    # model = load_model("app/static/test0217.h5")
    form = PropertyForm()
    form.property1.data = 1
    form.property2.data = 2 
    form.property3.data = 3
    form.property4.data = 4

    data = {
        "form": form,
        "operation": operation,
        "properties": properties,
        "status": status
    }

    if form.validate_on_submit():
        property1 = form.property1.data
        property2 = form.property2.data
        property3 = form.property3.data
        property4 = form.property4.data
        properties = [property1,property2,property3,property4]
        form.property1.data = ''
        form.property2.data = '' 
        form.property3.data = ''
        form.property4.data = ''

        # operation = str(model.predict([[int(property1)/10,int(property2)/10,int(property3)/10,int(property4)/10]])[0])
        operation = {"k1": 10, "k2": 5}
        # operation = json.dumps(operation)
        # requests.post("http://localhost:5000/run-abaqus", json=operation)
        status = 1

        data["form"] = form
        data["operation"] = operation
        data["properties"] = properties
        data["status"] = status
    return data

def abaqus_sumit():
    # 获取 POST 请求中的参数
    k1 = request.json.get('k1')
    k2 = request.json.get('k2')

    cwd = r"D:\kevin\DTOP-Kevin\app\static\abaqus"
    inp = "test.inp"
    inp_folder = "inp"
    odb_folder = "odb"

    # try:
    #     os.chdir(os.path.join(cwd,odb_folder))
    #     subprocess.run(f"abaqus job=simulation int input={os.path.join(cwd,inp_folder,inp)} ask_delete=OFF",shell=True)

    # except subprocess.CalledProcessError as e:
    #     print("abaqus error：", e)
    time.sleep(1)
    data = {
        "k1": float(k1-2)*0.8+2,
        "k2": float(k2-2)*0.8+2
    }
    return data