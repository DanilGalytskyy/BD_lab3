from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql.functions import now
from sqlalchemy import update

DATABASE_URI = 'postgresql://postgres:qwerty123@localhost:5432/postgres'
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)

Base = declarative_base()


class User(Base):
    __tablename__ = 'User'

    user_id = Column(Integer, primary_key=True)
    name = Column(String)
    phone_number = Column(String)
    email = Column(String)
    password = Column(String)

    def __init__(self, name, phone_number, email, password):
        self.name = name
        self.phone_number = phone_number
        self.email = email
        self.password = password


class Post(Base):
    __tablename__ = 'Post'

    post_id = Column(Integer, primary_key=True)
    datetime = Column(DateTime)
    title = Column(String)
    body = Column(String)
    user_id = Column(Integer, ForeignKey('User.user_id'))
    user = relationship("User", backref="Post")

    def __init__(self, datetime, title, body, user_id):
        self.datetime = datetime
        self.title = title
        self.body = body
        self.user_id = user_id


class Post_Reaction(Base):
    __tablename__ = 'Post_Reaction'

    post_reaction_id = Column(Integer, primary_key=True)
    value = Column(Boolean)
    datetime = Column(DateTime)
    user_id = Column(Integer, ForeignKey('User.user_id'))
    post_id = Column(Integer, ForeignKey('Post.post_id'))
    user = relationship("User", backref=backref("Post_Reaction", uselist=False))
    post = relationship("Post", backref=backref("Post_Reaction", uselist=False))

    def __init__(self, value, datetime, user_id, post_id):
        self.value = value
        self.datetime = datetime
        self.user_id = user_id
        self.post_id = post_id


class Comment(Base):
    __tablename__ = 'Comment'

    comment_id = Column(Integer, primary_key=True)
    datetime = Column(DateTime)
    body = Column(String)
    user_id = Column(Integer, ForeignKey('User.user_id'))
    user = relationship("User", backref="Comment")
    post_id = Column(Integer, ForeignKey('Post.post_id'))
    post = relationship("Post", backref="Comment")

    def __init__(self, datetime, body, user_id, post_id):
        self.datetime = datetime
        self.body = body
        self.user_id = user_id
        self.post_id = post_id


class Comment_Reaction(Base):
    __tablename__ = 'Comment_Reaction'

    comment_reaction_id = Column(Integer, primary_key=True)
    value = Column(Boolean)
    datetime = Column(DateTime)
    user_id = Column(Integer, ForeignKey('User.user_id'))
    comment_id = Column(Integer, ForeignKey('Comment.comment_id'))
    user = relationship("User", backref=backref("Comment_Reaction", uselist=False))
    comment = relationship("Comment", backref=backref("Comment_Reaction", uselist=False))

    def __init__(self, value, datetime, user_id, comment_id):
        self.value = value
        self.datetime = datetime
        self.user_id = user_id
        self.comment_id = comment_id


Base.metadata.create_all(engine)
session = Session()
try:
    Post = Post(now(), "My dreams", "Come true", 59)
    session.add(Post)
except Exception as err:
    print(err)

try:
    session.query(Post_Reaction).filter(Post_Reaction.post_reaction_id == 1).update({Post_Reaction.value: True})
except Exception as err:
    print(err)

try:
    session.query(User).filter(User.user_id == 57).delete()
except Exception as err:
    print(err)
session.commit()
session.close()
