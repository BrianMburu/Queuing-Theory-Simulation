import pandas as pd
import numpy as np

#Linear Congrential Generator Function
def LCG(Xo, m, a, c, N):
    randnums=[0]*N

    # Initialize the seed state
    randnums[0]=Xo

    # Traverse to generate required
    # Generating of random numbers using Linear Congrential Generator
    for i in range(1,N):
        randnums[i]=((randnums[i - 1] * a) + c ) % m
    return randnums

#Combined Linear Congrential Generator Function
def CLCG(Xo, M, A, N):
    gen1=[0]*N
    gen2=[0]*N

    #Computing LCG gor gen1 with c=0
    gen1=LCG(Xo[0],M[0],A[0],0,N)

    #Computing LCG gor gen2 with c=0
    gen2=LCG(Xo[1],M[1],A[1],0,N)
    randnums=[]

    # Generating of random numbers using combined Linear Congrential Generator
    for i in range(N):
        if (gen1[i]-gen2[i] % (M[0]-1) > 0):
            randnums.append((gen1[i]-gen2[i] % (M[0]-1))/M[0])
        if (gen1[i]-gen2[i] % (M[0]-1) < 0):
            randnums.append((gen1[i]-gen2[i] % (M[0]-1))/M[0] + 1)
        if (gen1[i]-gen2[i] % (M[0]-1) == 0):
            randnums.append((M[0]-1)/M[0])
    return randnums

def data_gen(st,iat,N):
    cs=[i+1 for i in range(N)]      #Customer Index generator. Is of len(N)
    iat[0]=np.NaN
    df={"Customer":cs,"Inter Arrival Time":iat,"Service Time":st} #Creating a dictionary to store the values above with respective names
    data=pd.DataFrame(df)   #Creating a dateframe table using the dictionary
    data=data.set_index("Customer") #setting the customer number as the index of the table.
    return data     #return the table

def que_gen(data):
    wt=[]   #waiting time 
    tsb=[]  #Time server begins 
    tse=[]  #Time Server Ends
    ist=[]  #Idle Server TIme
    art=[]  #Arrival Time

    iat=list(data["Inter Arrival Time"].values) #Getting the Inter-arrival Time data.
    st=list(data["Service Time"].values)   #Getting the Service Time data.

    for i in range(len(st)):
        if (i>=1):
            art.append(iat[i]+art[i-1]) #update s/t curr(art) = curr(iat)+prev(art)
            tsb.append(art[i]) if (art[i]-tse[i-1] >=0) else tsb.append(tse[i-1])   
            tse.append(st[i]+tsb[i])
            wt.append(0) if (art[i]-tse[i-1] >=0) else wt.append(abs(art[i]-tse[i-1])) #curr(wt)=0 if rs>=0 else curr(wt)=abs(rs)
            ist.append(art[i]-tse[i-1]) if (art[i]-tse[i-1] >= 0) else ist.append(0)   #curr(ist)=rs if rs>0, if rs<=0 curr(ist)=0
               
        else:
            art.append(0)   #setting initial art = 0
            wt.append(0)    #setting initial wt = 0
            tsb.append(0)   #setting initial tsb = 0
            ist.append(0)   #setting initial ist = 0 
            tse.append(st[i]+tsb[i])    #setting initial tse = curr(st)+(first(tsb)=0)

    data["Arrival Time"]=art    #creating Arrival Time Column in table
    data["Waiting Time"]=wt     #creating Waiting Time Column in table and then populating with wt values
    data["Time Server Begin"]=tsb   #creating Time Server Begin Column in table then populating with wt values
    data["Time Server Ends"]=tse    #creating Time Server Ends Column in table  then populating with wt values
    data["Idle Server Time"]=ist    #creating Idle Server Time Column in table  then populating with wt values
    data.to_csv("Queue_result.csv") #creating a csv file with the resulting values. then populating with wt values

    return data

if __name__== '__main__':
    n=input("Input the Number of the Customers expected: ")
    N=int(n)
    m= 110               #Linear Congrential Generator Mode
    M=(2599963,2760089) #Combined Linear Congrential Generator Modes

    xo=np.random.randint(0,m-1)  #Linear Congrential Generator seed
    Xo1=np.random.randint(0,M[0]-1) 
    Xo2=np.random.randint(0,M[1]-1) 
    X=(Xo1,Xo2)                 #Combined Linear Congrential Generator seeds

    a= np.random.randint(0,m-1) #Linear Congrential Generator a
    Ao=np.random.randint(0,M[1]-1)
    A1=np.random.randint(0,M[1]-1)
    A=(Ao,A1)                   #Linear Congrential Generator As

    c=np.random.randint(0,m-1)  #Linear Congrential Generator c

    iat_xi=LCG(xo,m,a,c,N)        #generating Inter arrival Time using Linear Congruential generator (xi)
    iat = [i/m for i in iat_xi]   #Ri = xi/m
    st=CLCG(X,M,A,N)            #generating Server time using Combined Linear Congruential generator
    data = data_gen(st,iat,N)
    
    print("Total waiting time is {t}".format(t=sum(que_gen(data)["Waiting Time"])))
    print("Average  Waiting time is {a}".format(a=np.mean(que_gen(data)["Waiting Time"])))
    print("Total Idle Server time is {t}".format(t=sum(que_gen(data)["Idle Server Time"])))
    print("Average Idle Server time is {a}".format(a=np.mean(que_gen(data)["Idle Server Time"])))
    print("Total Service time is {t}".format(t=sum(que_gen(data)["Service Time"])))
    print("Average  Server time is {a}".format(a=np.mean(que_gen(data)["Service Time"])))

    print(que_gen(data))        #displaying the queing Theory results results, data table.
