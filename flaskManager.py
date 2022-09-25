from flask import Flask ,render_template ,make_response ,request ,url_for ,Response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime ,timedelta
import mimetypes

import urllib.parse

import os
from flask import Flask, flash, request, redirect, url_for ,send_from_directory
from werkzeug.utils import secure_filename

class Server():

    def __init__(self ,name):

        self.app = Flask(name)

        self.UPLOAD_FOLDER = "media/entryImages/"
        self.ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

        self.app.config['UPLOAD_FOLDER'] = self.UPLOAD_FOLDER

        self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///generalDatabase.db"

        self.db = SQLAlchemy(self.app)

        class Account(self.db.Model):
            id = self.db.Column(self.db.Integer, primary_key=True)
            userName = self.db.Column(self.db.String(20), nullable=False)
            userPassword = self.db.Column(self.db.String(20), nullable=False)
            userDescription = self.db.Column(self.db.String(100),default="")
            entryList = self.db.Column(self.db.Text,default="")
            messageList = self.db.Column(self.db.Text, default="")
            messageThreadList = self.db.Column(self.db.Text,default="")

        class Category(self.db.Model):
            id = self.db.Column(self.db.Integer, primary_key=True)
            categoryName = self.db.Column(self.db.String(10), nullable=False)
            listOfThreadId = self.db.Column(self.db.Text,default="")

        class Thread(self.db.Model):
            id = self.db.Column(self.db.Integer, primary_key=True)
            threadTitle = self.db.Column(self.db.String(60), nullable=False)
            belongingCategory = self.db.Column(self.db.String(20), nullable=False)
            listOfEntryId = self.db.Column(self.db.Text,default="")

        class Entry(self.db.Model):
            id = self.db.Column(self.db.Integer, primary_key=True)
            belongingProfileId = self.db.Column(self.db.Integer,nullable=False)
            entryContent = self.db.Column(self.db.Text, nullable=False)
            listOfLikedUsersId = self.db.Column(self.db.Text,default="")
            listOdDislikedUsersId = self.db.Column(self.db.Text,default="")
            createdDate = self.db.Column(self.db.DateTime, default=datetime.utcnow)

        class MessageThread(self.db.Model):
            id = self.db.Column(self.db.Integer, primary_key=True)
            primaryProfileId = self.db.Column(self.db.Integer, nullable=False)
            secondaryProfileId = self.db.Column(self.db.Integer, nullable=False)
            messageIdList = self.db.Column(self.db.Text,default="")

        class Message(self.db.Model):
            id = self.db.Column(self.db.Integer, primary_key=True)
            messageContent = self.db.Column(self.db.Text, nullable=False)
            createdDate = self.db.Column(self.db.DateTime, default=datetime.utcnow)

        self.Account = Account
        self.Category = Category
        self.Thread = Thread
        self.Entry = Entry
        self.MessageThread = MessageThread
        self.Message = Message

        #when this program is compiled for the first time this next portion has to be included
        #later on it has not to be included
        #this is responsabile for creating the database and initializing it's categories
        #that every thread will be included to
        #------------------------------------------------------------------------------------------------------

        """self.db.create_all()

        c1 = Category(categoryName="Entertainment")
        c2 = Category(categoryName="Politics")
        c3 = Category(categoryName="Sport")
        c4 = Category(categoryName="Media")
        c5 = Category(categoryName="Strange")
        c6 = Category(categoryName="Funny")
        c7 = Category(categoryName="Scary")

        carr = [c1,c2,c3,c4,c5,c6,c7]

        for ci in carr:
            self.db.session.add(ci)
            self.db.session.commit()"""

        #-----------------------------------------------------------------------------------------------------------

        self.listOfCategories = []

        for i in self.Category.query.order_by(self.Category.id).all():

            self.listOfCategories.append(i.categoryName)

        print("available categories on this site:")

        for j in self.listOfCategories:

            print(j)

        @self.app.route("/",methods=["GET","POST"])
        def __index():

            return self.indexPage()

        @self.app.route("/signUp",methods=["GET","POST"])
        def __signUp():

            return self.signUp()

        @self.app.route("/userNameStatus",methods=["GET","POST"])
        def __userNameStatus():

            return self.userNameStatus()

        @self.app.route("/saveAccount",methods=["GET","POST"])
        def __saveAccount():

            return self.saveAccount()

        @self.app.route("/user/<string:userNameGot>",methods=["GET","POST"])
        def __accountPage(userNameGot):

            return self.accountPage(userNameGot)

        @self.app.route("/user/<string:userNameGot>/settings",methods=["GET","POST"])
        def __settingsPage(userNameGot):

            return self.settingsPage(userNameGot)

        @self.app.route("/signInStatus",methods=["GET","POST"])
        def __signInStatus():

            return self.signInStatus()

        @self.app.route("/<string:selectedCategory>",methods=["GET","POST"])
        def __category(selectedCategory):

            return self.category(selectedCategory)

        @self.app.route("/<string:selectedCategory>/<int:threadId>")
        def __thread(selectedCategory,threadId):

            return self.thread(selectedCategory,threadId)

        @self.app.route("/<string:userName>/<int:messageId>")
        def __messagePage(userName,messageId):

            return self.messagePage(userName,messageId)

        @self.app.route("/<string:mediaFolder>/<string:idFolder>/<string:fileName>")
        def __imagePage(mediaFolder, idFolder, fileName):

            return self.imagePage(mediaFolder,idFolder ,fileName)

        @self.app.route("/like/<int:id>",methods=["GET","POST"])
        def __like(id):

            return self.like(id)

        @self.app.route("/dislike/<int:id>",methods=["GET","POST"])
        def __dislike(id):

            return self.dislike(id)

        @self.app.route('/media/<path:filename>')
        def download_file(filename):

            return send_from_directory("media", filename, as_attachment=True)

    def indexPage(self):

        categoryList = self.Category.query.all()

        threadsOfToday = []

        for i in categoryList:

            for j in i.listOfThreadId.split():

                tempEntry = self.db.session.query(self.Entry).filter_by(id=int(self.db.session.query(self.Thread).filter_by(id=int(j)).filter_by(id=int(j)).first().listOfEntryId.split()[0])).first()

                if tempEntry.createdDate.date() == datetime.today().date():

                    threadsOfToday.append(self.db.session.query(self.Thread).filter_by(id=int(j)).first())

        currentUserCookie = request.cookies.get("currentUser")

        currentAccount = "-1"

        if currentUserCookie == None:

            print("no cookie has been found!")

        else:

            currentAccount = self.Account.query.filter_by(userName=currentUserCookie).first()

        return render_template("index.html",currentAccount=currentAccount,category=self.Category,thread=self.Thread,listOfCategories=self.listOfCategories,Db=self.db,account=self.Account,os=os,threadsOfToday=threadsOfToday,Entry=self.Entry)

    def signUp(self):

        currentAccount = "-1"

        currentUserCookie = request.cookies.get("accountId")

        if currentUserCookie == None:

            pass

        else:

            currentAccount = str(currentUserCookie)

        return render_template("signUpPage.html",currentAccount=currentAccount)

    def userNameStatus(self):

        possibleName = request.headers.get("possibleUserName")

        status = self.db.session.query(self.Account).filter_by(userName=possibleName).first()

        userNameAvailable = True

        if status != None:

            userNameAvailable = False


        try:

            return str(userNameAvailable)

        except:

            print("an error has occurred in finding the user name is taken or not!")

    def saveAccount(self):

        userNameGot = request.headers.get("userName")

        userPasswordGot = request.headers.get("userPassword")

        newAccount = self.Account(userName=userNameGot,userPassword=userPasswordGot)

        try:

            self.db.session.add(newAccount)

            self.db.session.commit()

            resultPositive = newAccount.userName

            cookiedResponse = make_response(resultPositive)
            cookiedResponse.mimetype = "text/plain"

            cookiedResponse.set_cookie("currentUser", newAccount.userName, max_age=10)

            return cookiedResponse

        except:

            print("an error occurred during saving the account!")

    def accountPage(self,userNameGot):

        userNameGotStatus = self.db.session.query(self.Account).filter_by(userName=userNameGot).first()

        if userNameGotStatus == None:

            return render_template("profiles/noSuchAccountError.html")

        currentUserCookie = request.cookies.get("currentUser")

        currentAccount = "-1"

        global threadId
        threadId = -1

        if currentUserCookie == None:

            return render_template("profiles/profilePage.html", currentAccount=currentAccount, userNameGot=userNameGot,listOfCategories=self.listOfCategories, threadId=threadId, Db=self.db,message=self.Message, messageThread=self.MessageThread, account=self.Account, os=os)


        else:

            currentAccount = self.Account.query.filter_by(userName=currentUserCookie).first()

            t = self.MessageThread.query.filter_by(primaryProfileId=currentAccount.id,secondaryProfileId=userNameGotStatus.id).first()

            if t != None:

                threadId = t.id

            t = self.MessageThread.query.filter_by(primaryProfileId=userNameGotStatus.id,secondaryProfileId=currentAccount.id).first()

            if t != None:

                threadId = t.id

            return render_template("profiles/profilePage.html",currentAccount=currentAccount,userNameGot=userNameGot,listOfCategories=self.listOfCategories,threadId = threadId,Db=self.db,message=self.Message,messageThread=self.MessageThread,account=self.Account,os=os)
    def settingsPage(self,userNameGot):

        global currentAccount
        currentAccount = None

        currentUserCookie = request.cookies.get("currentUser")

        if(currentUserCookie == None):

            print("no cookie has been found!")

        else:

            currentAccount = self.Account.query.filter_by(userName=currentUserCookie).first()

        if currentAccount == None or currentAccount.userName != userNameGot:

            return "page is not accesible!"

        return render_template("/profiles/settings.html",currentAccount=currentAccount,os=os,userNameGot=userNameGot,listOfCategories=self.listOfCategories)

    def signInStatus(self):

        userNameGot = request.headers.get("userName")

        userPasswordGot = request.headers.get("userPassword")

        response = "-1"

        accountAssociated = self.db.session.query(self.Account).filter_by(userName=userNameGot).first()

        if(accountAssociated != None):

            print(accountAssociated.userName)

            response = "-2"

            if(accountAssociated.userPassword == userPasswordGot):

                response = str(accountAssociated.userName)

        try:

            cookiedResponse = make_response(response)
            cookiedResponse.mimetype = "text/plain"

            cookiedResponse.set_cookie("currentUser",response,max_age=7)

            return cookiedResponse

        except:

            print("an error has occurred in signing in!")

    def category(self,selectedCategory):

        currentUserCookie = request.cookies.get("currentUser")

        global currentAccount

        currentAccount = "-1"

        if currentUserCookie == None:

            print("no cookie found!")

        else:

            currentAccount = self.Account.query.filter_by(userName=currentUserCookie).first()

        if selectedCategory == "deleteCookie":

            resp = Response()

            resp.delete_cookie('currentUser', path='/')

            return resp

        if selectedCategory == "addEntry":

            threadId = request.headers.get("threadId")

            userName = request.headers.get("userName")

            entryContent = urllib.parse.unquote(request.headers.get("entryContent"))

            user = self.Account.query.filter_by(userName=userName).first()

            if user == None:

                return "entryNotAdded"

            thread = self.Thread.query.filter_by(id=int(threadId)).first()

            newEntry = self.Entry(belongingProfileId=user.id,entryContent=entryContent)

            self.db.session.add(newEntry)

            self.db.session.commit()

            thread.listOfEntryId += " " + str(newEntry.id)

            self.db.session.commit()

            user.entryList += " " + str(newEntry.id)

            self.db.session.commit()

            listOfFiles = request.files.getlist("images[]")

            imageFolder = str(newEntry.id)

            for i in listOfFiles:
                filename = secure_filename(i.filename)
                path = os.path.join(self.app.config['UPLOAD_FOLDER'], imageFolder)
                if not os.path.isdir(path):
                    os.mkdir(path)
                i.save(os.path.join(self.app.config['UPLOAD_FOLDER'], imageFolder + "/" + filename))
                i.close

            return "entryAdded"

        if selectedCategory == "createThread":

            entryContent = urllib.parse.unquote(request.headers.get("entryContent"))

            threadTitle = urllib.parse.unquote(request.headers.get("threadTitle"))

            threadCategory = request.headers.get("threadCategory")

            a = currentAccount.id

            newEntry = self.Entry(belongingProfileId=a,entryContent=entryContent)

            self.db.session.add(newEntry)

            self.db.session.commit()

            newThread = self.Thread(threadTitle=threadTitle,belongingCategory=threadCategory,listOfEntryId=str(newEntry.id))

            self.db.session.add(newThread)

            self.db.session.commit()

            currentCategory = self.Category.query.filter_by(categoryName=threadCategory).first()

            currentCategory.listOfThreadId += (" " + str(newThread.id))

            self.db.session.commit()

            currentAccount.entryList += " " + str(newEntry.id)

            self.db.session.commit()

            listOfFiles = request.files.getlist("images[]")

            imageFolder = str(newEntry.id)

            for i in listOfFiles:
                filename = secure_filename(i.filename)
                path = os.path.join(self.app.config['UPLOAD_FOLDER'], imageFolder)
                if not os.path.isdir(path):
                    os.mkdir(path)
                i.save(os.path.join(self.app.config['UPLOAD_FOLDER'], imageFolder + "/" + filename))
                i.close

            return "threadCreated " + str(newThread.id)

        if selectedCategory == "createMessageThread":

            secondaryUserName = request.headers.get("targetAccountName")

            secondaryAccount = self.Account.query.filter_by(userName=secondaryUserName).first()

            threadId = -1

            t = self.MessageThread.query.filter_by(primaryProfileId=currentAccount.id,
                                                   secondaryProfileId=secondaryAccount.id).first()

            if t != None:

                threadId = t.id



            t = self.MessageThread.query.filter_by(primaryProfileId=secondaryAccount.id,
                                                   secondaryProfileId=currentAccount.id).first()

            if t != None:

                threadId = t.id

            messageContent = urllib.parse.unquote(request.headers.get("messageContent"))

            if threadId == -1:

                newMessage = self.Message(messageContent=messageContent)

                self.db.session.add(newMessage)
                self.db.session.commit()

                newMessageThread = self.MessageThread(primaryProfileId=currentAccount.id,secondaryProfileId=secondaryAccount.id,messageIdList=str(newMessage.id))

                self.db.session.add(newMessageThread)
                self.db.session.commit()

                xy = self.MessageThread.query.filter_by(id=newMessageThread.id).first()

                currentAccount.messageThreadList += " " + str(newMessageThread.id)

                self.db.session.commit()

                secondaryAccount.messageThreadList += " " + str(newMessageThread.id)

                self.db.session.commit()

                currentAccount.messageList = str(newMessage.id)

                self.db.session.commit()

                return str("messageThreadCreated")

            newMessage = self.Message(messageContent=messageContent)

            messageThread = self.MessageThread.query.filter_by(id=threadId).first()

            self.db.session.add(newMessage)

            self.db.session.commit()

            messageThread.messageIdList += " " + str(newMessage.id)

            self.db.session.commit()

            currentAccount.messageList += " " + str(newMessage.id)

            self.db.session.commit()

            directory = "media/entryImages/non"

            for filename in os.listdir(directory):

                if os.path.isfile(filename):
                    print("typeof: ",filename)

            return str(messageContent)

        if selectedCategory == "changeProfileImage":

            currentUserCookie = request.cookies.get("currentUser")

            image = request.files.getlist("image")

            currentAccount = self.Account.query.filter_by(userName=currentUserCookie).first()

            path = ("media/profileImages/" + str(currentAccount.id))

            print(path)

            filename = secure_filename("profileImage.jpg")
            print(filename)
            print(self.UPLOAD_FOLDER)

            if not os.path.isdir(path):

                os.mkdir(path)

            else:

                print("itisssss")

            for i in image:

                i.save(os.path.join(path, filename))

            return "profileImageChanged"

        if selectedCategory == "changeUserDescription":

            theDescription = urllib.parse.unquote(request.headers.get("userDescription"))

            currentUserCookie = request.cookies.get("currentUser")

            currentAccount = self.Account.query.filter_by(userName=currentUserCookie).first()

            currentAccount.userDescription = theDescription

            self.db.session.commit()

            return "successsssssssssssss"


        if selectedCategory == "search":

            searchTerm = request.headers.get("searchTerm")

            responseString = ""

            listOfThreads = self.Thread.query.order_by(self.Thread.id).all()

            listOfUsers = self.Account.query.order_by(self.Account.userName).all()

            listOfPotentialThreads = self.givePotentialThreadTuple(listOfThreads,searchTerm)

            listOfPotentialUsers = self.givePotentialAccountsTuple(listOfUsers,searchTerm)

            elementCount = 0
            threadIndexCount = 0
            userIndexCount = 0

            compound = listOfPotentialThreads[1] + listOfPotentialUsers[1]

            sorted = [*set(compound)]
            sorted.sort(reverse=True)

            arr = []

            for i in sorted:

                try:

                 if(listOfPotentialUsers[1][userIndexCount] == i):

                    for j in listOfPotentialUsers[0]:

                        if j[0] == i and elementCount <= 7 and i != 0:

                            arr.append(j)

                            responseString += "@|" + j[1] + "|"

                            elementCount = elementCount + 1
                    userIndexCount = userIndexCount + 1
                except IndexError:
                    print("index error")
                try:

                 if (listOfPotentialThreads[1][threadIndexCount] == i):

                    for t in listOfPotentialThreads[0]:

                        if t[0] == i and elementCount <= 7 and i != 0:
                            arr.append(t)

                            responseString += "$|" + t[1] + "|" + str(t[2]) + "|" + t[3] + "|"
                            elementCount = elementCount + 1
                    userIndexCount = userIndexCount + 1
                except IndexError:
                    print("index error")

            return responseString

        if self.listOfCategories.count(selectedCategory) == 0:

            return render_template("/categories/noSuchCategory.html",selectedCategory=selectedCategory)

        else:

            currentCategory = self.Category.query.filter_by(categoryName=selectedCategory).first()

            listOfThreadsString = currentCategory.listOfThreadId.split()

            listOfThreads = []

            for i in listOfThreadsString:

                listOfThreads.append(self.Thread.query.filter_by(id=int(i)).first())

            for i in listOfThreads:
                print(str(self.Entry.query.filter_by(id=int(i.listOfEntryId.split()[0])).first().entryContent))

            return render_template("/categories/category.html",currentAccount=currentAccount,selectedCategory=selectedCategory,currentCategory=currentCategory,Category=self.Category,Db=self.db,listOfThreads=listOfThreads,Entry=self.Entry,os=os,listOfCategories=self.listOfCategories,Thread=self.Thread,Account=self.Account)

    def thread(self,selectedCategory,threadId):

        global currentAccount
        currentAccount = "-1"

        if self.listOfCategories.count(selectedCategory) == 0:

            return render_template("/categories/noSuchCategory.html",selectedCategory=selectedCategory)

        else:

            arr = self.Thread.query.all()

            currentUserCookie = request.cookies.get("currentUser")

            currentThread = self.Thread.query.filter_by(id=threadId).first()

            listOfEntriesString = currentThread.listOfEntryId.split()

            listOfEntries = []

            for i in listOfEntriesString:
                listOfEntries.append(self.Entry.query.filter_by(id=int(i)).first())

            if currentUserCookie != None:
                currentAccount = self.Account.query.filter_by(userName=currentUserCookie).first()

        return render_template("/categories/threads/thread.html",currentAccount=currentAccount,selectedCategory=selectedCategory,threadId=threadId,listOfEntries=listOfEntries,listOfCategories=self.listOfCategories,Db=self.db,Account=self.Account,os=os,Thread=self.Thread)

    def messagePage(self,userName,messageId):

        if request.method == "GET":

            accountIdCookie = request.cookies.get("userId")

            if  accountIdCookie == None :

                return render_template("/profiles/messages/notAllowedToSeeMessage.html")

            else:

                currentUserAccountId = int(accountIdCookie)

                if userName == currentUserAccountId.userName:

                    return render_template("/profiles/message.html",currentUserAccountId=currentUserAccountId,messageId=messageId)

                else:

                    return render_template("/profiles/messages/notAllowedToSeeMessage.html")

        elif request.method == "POST":

            pass

    def imagePage(self,mediaFolder,idFolder,fileName):

        path = mediaFolder + "/" + idFolder + "/" + fileName

        return render_template("/imagePage.html",mediaFolder=mediaFolder,idFolder=idFolder,fileName=fileName)

    def like(self,id):

        global currentAccount
        currentAccount = None

        currentUserCookie = request.cookies.get("currentUser")

        if (currentUserCookie == None):

            pass

        else:

            currentAccount = self.Account.query.filter_by(userName=currentUserCookie).first()

            theEntry = self.Entry.query.filter_by(id=id).first()

            global userLikedStatus

            if theEntry.listOfLikedUsersId.split().count(str(currentAccount.id)) == 0:

                userLikedStatus = False

            else:

                userLikedStatus = True

            if not userLikedStatus:

                theEntry.listOfLikedUsersId += " " + str(currentAccount.id)

                self.db.session.commit()

                userLikedStatus = True

                if theEntry.listOdDislikedUsersId.split().count(str(currentAccount.id)) != 0:

                    temp = theEntry.listOdDislikedUsersId + " "

                    index = temp.index(str(currentAccount.id))

                    theEntry.listOdDislikedUsersId = temp[index-1] + temp[index+1]

                    self.db.session.commit()


                return str(theEntry.id) + " likes " + str(len(theEntry.listOfLikedUsersId.split())) + " dislikes " + str(len(theEntry.listOdDislikedUsersId.split())) + " " + str(userLikedStatus)

            return str(theEntry.id) + " likes " + str(len(theEntry.listOfLikedUsersId.split())) + " dislikes " + str(len(theEntry.listOdDislikedUsersId.split())) + " " + str(userLikedStatus)

        return "-1"

    def dislike(self, id):

        global currentAccount
        currentAccount = None

        currentUserCookie = request.cookies.get("currentUser")

        if (currentUserCookie == None):

            pass

        else:

            currentAccount = self.Account.query.filter_by(userName=currentUserCookie).first()

            theEntry = self.Entry.query.filter_by(id=id).first()

            global userDislikedStatus

            if theEntry.listOdDislikedUsersId.split().count(str(currentAccount.id)) == 0:

                userDislikedStatus = False

            else:

                userDislikedStatus = True

            global userLikedStatus

            if not userDislikedStatus:

                theEntry.listOdDislikedUsersId += " " + str(currentAccount.id)

                self.db.session.commit()

                if theEntry.listOfLikedUsersId.split().count(str(currentAccount.id)) != 0:

                    temp = theEntry.listOfLikedUsersId + " "

                    index = temp.index(str(currentAccount.id))

                    theEntry.listOfLikedUsersId = temp[index - 1] + temp[index + 1]

                    self.db.session.commit()

                    userLikedStatus = False

                return str(theEntry.id) + " likes " + str(len(theEntry.listOfLikedUsersId.split())) + " dislikes " + str(len(theEntry.listOdDislikedUsersId.split())) + " " + str(userLikedStatus)#"it was disliked"

            return str(theEntry.id) + " likes " + str(len(theEntry.listOfLikedUsersId.split())) + " dislikes " + str(len(theEntry.listOdDislikedUsersId.split())) + " " + str(userLikedStatus)#"it is already disliked"

        return "-1"


    def allowed_file(self,filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS

    def compareStrings(self,first,second):

        global count
        count = 0

        a = len(first)
        b = len(second)

        if a < b:

            for i in range(0,a):

                if first[i] == second[i]:

                    count = count + 1

        else:

            for i in range(0,b):

                if(first[i] == second[i]):

                    count = count + 1

        return count

    def givePotentialThreadTuple(self,list,string):

        threadList = []

        for i in list:
            temp = [self.compareStrings(i.threadTitle,string),i.belongingCategory,i.id,i.threadTitle]

            threadList.append(temp)

        tempArr = []

        for j in threadList:

            tempArr.append(j[0])

        tempArr.sort()

        tempArrCollapsed = []

        tempNumber = -1

        for i in tempArr:

            if(i>tempNumber):

                tempArrCollapsed.append(i)

                tempNumber = i

        tempArrCollapsed.sort(reverse=True)

        return (threadList,tempArrCollapsed)

    def givePotentialAccountsTuple(self, list, string):
        threadList = []

        for i in list:
            temp = [self.compareStrings(i.userName, string), i.userName]

            threadList.append(temp)

        tempArr = []

        for j in threadList:
            tempArr.append(j[0])

        tempArr.sort()

        tempArrCollapsed = []

        tempNumber = -1

        for i in tempArr:

            if (i > tempNumber):
                tempArrCollapsed.append(i)

                tempNumber = i

        tempArrCollapsed.sort(reverse=True)

        return (threadList, tempArrCollapsed)
