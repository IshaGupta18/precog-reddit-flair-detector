import pickle

model = pickle.load(open("./titleModeldump.pkl"))
print(model)
model2 = pickle.load(open("./titleModeldump.pkl", "rb"))
print(model2)