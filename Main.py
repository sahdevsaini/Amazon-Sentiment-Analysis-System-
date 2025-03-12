import streamlit as st
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import plotly.express as px
st.set_page_config(page_title="Amazon Sentiment Analysis System",page_icon="data:image/png;base64,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")
st.title("SENTIMENT ANALYSIS")
#https://i.pinimg.com/originals/52/ad/6a/52ad6a11c1dcb1692ff9e321bd520167.gif
choice = st.sidebar.selectbox("My Menu",("Home","ANALYSIS","VISUALIZATIOM"))
if(choice == "Home"):
    st.image("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAWEAAACPCAMAAAAcGJqjAAABuVBMVEX///+h0w7lNwD/zwDjJgCa0ADsfGe932vrb1W43Vv/ywD/2lX/3GcAAAD/+2X/+Y/1pRX//t7/+qLkiwDhFgDt0AOZ1BD//cBGRkb3mgD/0jD/2TH/yi39rxb/3gH/0zD99O7//9n/5DP/xiz/uSf/wjn/1QD//LX/+63/+ZP/+IP/+Ev/6jvdfwBvJwDTbQD/4wD7+//+zUb8w036mQD43MT/+H7/4GD/zzv/2Uj/3TL/wCv/sxn/vTLPoAjTbwDrujrlvzOoZwDaeQDCwsJUVFSpqanf398VFRWRkZErLDqjpK7zxbDyj3rqcWb5tWW9tT7+6mLx3GbQ6ZDnVDmBZQvJqQf36N2tkgjW66X21MxSPw3vpJPmwQ/o9MTF5Hv1tE/4zIL6x2P31rj71aj/5YH1tXX3wIv+vgD4qlP4oSr0m0T1xaD/12P1pWf/7m7//onj01P0lziRYwy5nDB9RwjQuTRgGwD4igB/OAD16lCLVQ7l00GvjyZcAwCJXA+YUwCGTw3jr4jgnGLYgTvElR14Vjt+Y1mvfACTZEBmSEuzdUHZ6fStlnzWj1nTfC3cnADbmXXJVwCIdr1hAAAHbElEQVR4nO3b7VsTVxoGcFy0dQvK4EizSWaaITORl0yMDQnkZUII0dpttd2w26bb3W6tFBWhIkxAyIuGQFp2awn4F+9zJqD1A8KcZK9B9/7pdfklPNd97jlnMona1QUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKfIx04HeCdd/9MrN1Dx/8KNCy994nSWd9PNTw8LvuF0lHfVnw8bvul0knfWZ62CP3c6R1tu3X7PCV98me893l9aDZ/kpb0z7zvh+7/2v7nfb/92+awjLrs/+uB4175iBX99kpd+MPDhOWe8/6aCC2fP/sEZ1HD38a4MUMFfneSV3d0DH55xxrnvjy5YOe9UwSdsuPujby5cGLhyuhs+c+7vR98jLjtV8Ekb7r72j2+uneiFTjZ85siG/3n6G77y3cDJCnaw4TPnjny3e8+xm8SJGz45Jxv+11EN30bDnWl48C2+D78NDb/hPtz1xWl/lng7Gj76WaKrcPl0Pw+/FQ0f85Hj/Kn+TGeHY5/p3vCBg1G+vX3eEXfyPZ018UdHHPe9BAAAAAAAAAAAAHTQx4rSkX+u25k5HUqjnJ4whR/GIpGxu7NKm3N+vDsWGRv7odB2Ghpz98f20igsTORuB8K0X03szoO5ocFB13DEWGxnzqLcc8k1ODg09+BOG8sq3HvQO+SiND3Gff4pyn2DhXFRmPk2wsTmKUzb1SzKc4OD/YQmpeYV3jHKfHy4v781Z07mzjMr9w62xvS7ItzlKA8jrsHDMMIsb5hF4VU1Knc1i+4R1/CQiwwNDw31LPCmWYgMuYZdrTmuS27OimPREfbzDIX6SVS4pigrE0OHU4ZdI+4YX5jZ16r5aYV3St9I38jIJaavr28k8CXfnEcB9uPWmBEaMxfl2n6FaC+NeZnmEucFfxh5OYWFmeELE3OPvl7NPFcYMTK6ND4+PjraN0p/jC/N8F3wWHRmaWn88SjNGR9/TGMiCwrHmHsBloaNGWVTlua4zsKie+ZwTWxRS6Nprm5WDsPQmMfc1cxGexL5Uj5/kVnO5/MTAa7DsBCYyF9cNq05a+bF/MRElOPuV1jvYWPWrDRFijMRj9qfoqzEe2hFy6/W1BPl6CbGqrm4bI3JL5fyCb5qHhmJhF5aXS0Fg8G1J9VgIhFZ5zhShfV4PFEyN4o0plTeWKM5wiP7Y+6745Rm82qFpXlqligNRzcUhha19oSFqTy11iTX7Ye5JycS/tLqUwpTenZ1rcRXjbKgSZ5kZWOjouvBam0z6JPUdY6DORtNxX16uVYN6nqpXCvqHkletz9mXlbjyWStXAnqwWJtWvfGUxy3ibpblbx6tWZaU0zd61EN+/dzZVtTqZoabRc9SJtGp2qi9sMUckZK8virVd3v1ytmNimp2jrH9a5HNVXyFzcrbE6xXPFKqryu2J2irMgpyeffMa00q1/7PVLKvWU7zJY7pUrJyuaa7tf9m0U2RQ7ZDnNQzVrRClNkBWtR+0/obIxKi/InW789/A2zbnS/N5mkOVRwSs7ZPlJKU6AL5fHrSTZFt9JE7Tf8KEprou3nt6b4fZKUEngaltOSh9ZkLYkOgoeq4Wi4KVM1ktefzE5WkmxJaUPkaVhkV8rj8zI+D+0ajWNRrOFUa0rSmqOmDPe+7TBbIluTx9vikViYHEcYOTX1nY9tGJL0+ia5qlG2BSMQkLyNVbNaLme9akCTcxwPAbM5WQtIrJxkkq42u1DunP0xW6KRVj0H3fh8UiAth27ZnlIPyemA6vF5fMTDphjuXdtTqJoHP/8yvdOYJI2d6X//Z8/I2Q9Dm4+qSUxXdT2pVzYb8bQhhBX7YwpNwdACgYQvOzmZTcQDdKFE+8ebdWNkN64eeGLGDSHD8SwRFox0YCpL+86bjDcCaU0O8ZzLkPHr8+c3r3/CXL/5/DeZq5pYWJBTjWpCJfHKM1UTRPuXm+yKspGON8rPTLNcnlI1maearkKG0kyRLP0idJ2a9qco27Rt0lOm2Zia2ik3rDAcT6BUzd7Pv123/n819fzLjsZXzXZIMGjrBixTe3Sd+D7uvhBkbaeaTZCsuWdwXqj9HI2hI05ZVDrclIbjXFrbxkjFi6ZpVqdUmpKzfzMnuyFjZ6NWK5Ma0YQw18fdQlOkOJqW1jTNkGlJHOeJqWcEeptqzaFNI/IcKPb2QmkO4lAznNV0beUE1jGdyxRbk9jkCkPVyDu16QOakOGsJvZCpDgtgpDh2nrMbvh3Y8QXPHuPpQm30hjWmBxfNXSfyL0WhvNL0MILUd6bNmn/TjfocYS7mlgz91BoEXl3MFNn5bTGhJqc3xeyjZN7OSa8r/CO2XoVJrPN/RV8oUlvDHsP9wR2KPmOU2vOfjgTEkUxF+Yvholth3M0Rsy00Qztv3o4zNKEwk3Oc2C5lbHChMKZdsIUKIxoVcPzxv07ymx9f3d/sb0hJLa4v7tbb/ev+yjN7u5+vd00MbamToTpSDWdo5yqMQAAAAAAAAAAAAAAAAAAAAAAAAAAAP93/gu5sPzi8v547wAAAABJRU5ErkJggg==")
    st.write("This")
elif(choice == "ANALYSIS"):
    url = st.text_input("Enter Google sheet URL")
    c= st.text_input("Enter column")
    btn= st.button("Analyze")
    if btn:   
        df = pd.read_csv(url)
        x = df[c]
        mymodel = SentimentIntensityAnalyzer()
        l=[]

        for k in x:
            pred = mymodel.polarity_scores(k)
            if(pred['compound']>0.05):
            #print("Sentiment is Positive")
                l.append("Positive")
            elif(pred['compound']<0.05):
            #print("Sentiment is Negative")
                l.append("Negative")
            else:
            #print("Sentiment is Neutral")
                l.append("Neutral")

        df['Sentiment']=l
        #print(df)
        df.to_csv("Result.csv",index = False)
        st.header("Analysis Sucessful and result is save as result.csv")
elif(choice == "VISUALIZATIOM"):
    df=pd.read_csv("Result.csv")
    st.dataframe(df)
    choice2 = st.selectbox("Choose Visualizations",("None","Pie","Histogram"))
    if(choice2=="Pie"):
        pos = len(df[df['Sentiment'] == "Positive"])/len(df)*100
        neg = len(df[df['Sentiment'] == "Negative"])/len(df)*100
        neu = len(df[df['Sentiment'] == "Neutral"])/len(df)*100
        fig = px.pie(values=[pos,neg,neu],names = ["Positive","Negative","Neutral"])
        st.plotly_chart(fig)
        #fig.show(renderer ='iframe')
    if(choice2=="Histogram"):
        c=st.selectbox("Choose Column",df.columns)
        ## Histogram
        fig = px.histogram(x= df['Gender'],color = df[c])
        st.plotly_chart(fig)
        #fig.show(renderer ='iframe')

        

