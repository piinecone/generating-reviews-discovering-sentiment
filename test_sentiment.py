from encoder import Model
mdl = Model()

text = ['it was a nice day','it was a great day','it was a bad day','It was a wonderful day','It was an excellent day','It was a super excellent day','It was such a bad bad day ','It was such a bad bad bad day']
text_features = mdl.transform(text)
for i in range(len(text)):
    sentiment = text_features[i, 2388]
    print(text[i],sentiment)
