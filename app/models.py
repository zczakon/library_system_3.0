import datetime
from app import db


class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(255))
    surname = db.Column(db.String(255))
    pesel = db.Column(db.String(11), unique=True)
    registration_date = db.Column(db.DateTime)

    lendings = db.relationship("BookLending", back_populates="student")  # cascade="all, delete, delete-orphan" ?

    def __str__(self):
        return '({}, {}, {})'.format(self.name + ' ' + self.surname, 'PESEL: ' + str(self.pesel),
                                     'ID:' + str(self.id), 'role: ' + str(self.account.get_role()))

    def __repr__(self):
        return '({}, {}, {})'.format(self.name + ' ' + self.surname, 'PESEL: ' + str(self.pesel),
                                     'ID:' + str(self.id))

    def __eq__(self, other):
        if self.__class__ == other.__class__ and self.id == other.id and self.name == other.name and self.pesel and \
                self.registration_date == other.registration_date:
            return True
        return False

    """
        def __hash__(self):
        return hash(self.x)
    """

    def create(self):
        self.registration_date = datetime.date.today()
        return self

    def fullname(self):
        return str(self.name) + ' ' + str(self.surname)


class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(13))
    title = db.Column(db.String(255))
    author = db.Column(db.String(255))

    lendings = db.relationship("BookLending", back_populates="book")  # cascade="all, delete, delete-orphan" ?

    def __str__(self):
        return '({}, {}, {}, {})'.format(str(self.title), 'author: ' + self.author, 'ISBN: ' +
                                         str(self.isbn), 'ID: ' + str(self.id))

    def __repr__(self):
        return '({}, {}, {}, {})'.format(str(self.title), 'author: ' + self.author, 'ISBN: ' +
                                         str(self.isbn), 'ID: ' + str(self.id))

    def __eq__(self, other):
        if self.__class__ == other.__class__ and self.id == other.id and self.isbn == other.isbn and self.title == \
                other.title and self.author == other.author:
            return True
        return False


class BookLending(db.Model):
    __tablename__ = 'lendings'

    id = db.Column(db.Integer, primary_key=True)
    creation_date = db.Column(db.DateTime)
    max_return_date = db.Column(db.DateTime)
    return_date = db.Column(db.DateTime)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))

    student = db.relationship("Student", back_populates="lendings")
    book = db.relationship("Book", back_populates="lendings")

    return_time = 30

    def __str__(self):
        return '({}, {}, {}, {})'.format(str(self.book), str(self.student), 'creation date: '
                                         + str(self.creation_date), 'return date: ' +
                                         str(self.return_date))

    def __repr__(self):
        return '({}, {}, {}, {})'.format(str(self.book), str(self.student), 'creation date :'
                                         + str(self.creation_date), 'return date: ' +
                                         str(self.return_date))

    def __eq__(self, other):
        if self.__class__ == other.__class__ and self.id == other.id and self.creation_date == other.creation_date and \
                self.max_return_date == other.max_return_date and self.student_id == other.student_id and self.book_id \
                == other.book_id:
            return True
        return False

    def create(self):
        self.creation_date = datetime.date.today()
        self.max_return_date = self.creation_date + datetime.timedelta(days=self.return_time)
        return self

    def rental_time(self):
        return datetime.date.today() - self.creation_date

    def remaining_days(self):
        if self.return_date is None:
            pass
        return self.max_return_date - self.max_return_date
