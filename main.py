# coding: utf-8

__author__ = 'AnnieQin <annie__qin@163.com>'


import datetime
import json

from playhouse.shortcuts import model_to_dict, dict_to_model
from tornado.web import HTTPError
from tornado.web import RequestHandler
from tornado.web import Application
import tornado.ioloop
import os.path

from lib.datetimejson import LazableJSONEncoder
from lib.utils import num_to_string, parse_json, utc_to_local, time_to_string
from lib.task import get_commtasks, get_monthtasks, get_weektasks, \
    get_temptasks_query, get_commtasks_json, get_temptasks_json, \
    get_monthtasks_json, get_weektasks_json

from models.task import (MonthTask, WeekTask, TemporaryTask,
                         CommonTask, TaskRecord, Category,
                         CommonTaskFrequency)
from models.user import User


class BaseHandler(RequestHandler):
    def get_current_user(self):
        user = None
        user_id = self.get_secure_cookie('user_id')
        if user_id:
            try:
                user = User.get(User.id == int(user_id))
            except User.DoesNotExist:
                raise HTTPError(500)
        return user

    def return_json(self, data):
        self.write(json.dumps(data, cls=LazableJSONEncoder))
        self.set_header('Content-Type', 'application/json; charset=UTF-8')

    def return_status(self, status=599, message=''):
        self.write({
            'status': status,
            'message': message
        })


class MainHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        current_user = self.current_user
        selected_date = None
        selected_year = None
        selected_month = None
        selected_day = None
        selected_weekday = None
        selected_week = None
        try:
            selected_date = self.get_argument('selected_date')

            selected_date = datetime.datetime.fromtimestamp(float(selected_date) / 1000.0)

            selected_year = selected_date.year
            selected_month = selected_date.month
            selected_day = selected_date.day

            selected_date = selected_date.date()
            selected_week = selected_date.isocalendar()[1]

            selected_weekday = selected_date.isocalendar()[2]
        except:
            pass
        if selected_date:
            categories = Category.select().where(
                Category.user_id == current_user.id,
                Category.status != Category.DELETED
            )
            commtasks = get_commtasks(
                current_user.id, selected_date, selected_year,
                selected_month, selected_weekday, selected_day
            )
            temptasks = get_temptasks_query(current_user.id, selected_date)
            monthtasks = get_monthtasks(current_user.id, selected_year,
                                        selected_month)
            weektasks = get_weektasks(current_user.id, selected_year,
                                      selected_month, selected_week)
            commtasks_json = get_commtasks_json(current_user.id, selected_date,
                                                selected_year, selected_month)
            temptasks_json = get_temptasks_json(current_user.id, selected_date)
            monthtasks_json = get_monthtasks_json(current_user.id, selected_year,
                                                  selected_month)
            weektasks_json = get_weektasks_json(current_user.id, selected_year,
                                                selected_month, selected_week)
            year = selected_year
            month_num = selected_month
            day_num = selected_day
            week_num = selected_week
            weekday_num = selected_weekday

            data = {
                'categories': categories,
                'monthtasks': monthtasks,
                'weektasks': weektasks,
                'temptasks': temptasks,
                'commtasks': commtasks,

                'user_id': current_user.id,
                'username': current_user.username,

                'year': year,
                'month': num_to_string(month_num, 'month'),
                'week': num_to_string(week_num, 'week'),
                'day': num_to_string(day_num, 'day'),
                'weekday': num_to_string(weekday_num, 'weekday'),

                'month_num': month_num,
                'week_num': week_num,
                'day_num': day_num,
                'weekday_num': weekday_num,

                'commtasks_json': commtasks_json,
                'temptasks_json': temptasks_json,
                'monthtasks_json': monthtasks_json,
                'weektasks_json': weektasks_json
            }
            self.render('home.html', **data)
        else:
            date = datetime.datetime.now()

            year = date.year
            month_num = date.month
            week_num = date.isocalendar()[1]
            day_num = date.day
            weekday_num = date.isocalendar()[2]

            categories = Category.select().where(
                Category.user_id == current_user.id,
                Category.status != Category.DELETED
            )
            temptasks = get_temptasks_query(current_user.id, date.date())

            monthtasks = get_monthtasks(current_user.id, year, month_num)
            weektasks = get_weektasks(current_user.id, year, month_num, week_num)
            commtasks = get_commtasks(current_user.id, date.date(), year, month_num,
                                      weekday_num, day_num)


            commtasks_json = get_commtasks_json(current_user.id, date.date(),
                                                year, month_num)
            temptasks_json = get_temptasks_json(current_user.id, date.date())
            monthtasks_json = get_monthtasks_json(current_user.id, year, month_num)
            weektasks_json = get_weektasks_json(current_user.id, year,
                                                month_num, week_num)

            data = {
                'categories': categories,
                'monthtasks': monthtasks,
                'weektasks': weektasks,
                'temptasks': temptasks,
                'commtasks': commtasks,

                'user_id': current_user.id,
                'username': current_user.username,

                'year': year,
                'month': num_to_string(month_num, 'month'),
                'week': num_to_string(week_num, 'week'),
                'day': num_to_string(day_num, 'day'),
                'weekday': num_to_string(weekday_num, 'weekday'),

                'month_num': month_num,
                'week_num': week_num,
                'day_num': day_num,
                'weekday_num': weekday_num,

                'commtasks_json': commtasks_json,
                'temptasks_json': temptasks_json,
                'monthtasks_json': monthtasks_json,
                'weektasks_json': weektasks_json
            }
            self.render('home.html', **data)


class RegisterHandler(RequestHandler):
    def get(self):
        self.render('register.html')

    def post(self):
        username = self.get_argument('username')
        pwd = self.get_argument('pwd')
        pwd_confirm = self.get_argument('pwd_confirm')
        if pwd == pwd_confirm:
            User.create(username=username, pwd=pwd)
            self.redirect('/')
        else:
            self.redirect('/register')


class LoginHandler(RequestHandler):
    def get(self):
        self.render('login.html')

    def post(self):
        username = self.get_argument('username')
        pwd = self.get_argument('pwd')

        try:
            user = User.get(User.username == username, User.pwd == pwd)
            if user:
                self.set_secure_cookie('user_id', str(user.id))
                self.redirect('/')
            else:
                self.redirect('/login')
        except User.DoesNotExist:
            self.redirect('/login')


class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user_id")
        self.redirect('/login')


class CreateTemptask(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        data = parse_json(self)
        content = data.get('content')
        visible_range = data.get('visible_range')
        scheduled_started_at = data.get('scheduled_started_at')
        scheduled_finished_at = data.get('scheduled_finished_at')

        year = data.get('year')
        month = data.get('month')
        day = data.get('day')

        date = datetime.datetime.strptime(year+'-'+month+'-'+day, '%Y-%m-%d').date()

        temptask = TemporaryTask.create(
            user_id=self.current_user.id,
            content=content,
            visible_range=visible_range,
            scheduled_started_at=scheduled_started_at,
            scheduled_finished_at=scheduled_finished_at,
            date=date
        )

        self.return_json({
            'content': content,
            'visible_range': visible_range,
            'scheduled_started_at': scheduled_started_at,
            'scheduled_finished_at': scheduled_finished_at,
            'id': temptask.id
        })


class CreateCommtask(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        current_user = self.current_user
        data = parse_json(self)

        category_id = data.get('category_id')

        year = int(data.get('year'))
        month = int(data.get('month'))
        day = int(data.get('day'))
        weekday = int(data.get('weekday'))

        started_date = data.get('started_date')
        finished_date = data.get('finished_date')

        scheduled_started_at = data.get('scheduled_started_at')
        scheduled_finished_at = data.get('scheduled_finished_at')

        content = data.get('content')
        frequency = data.get('frequency')
        visible_range = data.get('visible_range')

        scheduled_started_time = None
        scheduled_finished_time = None
        if scheduled_started_at:
            scheduled_started_time = utc_to_local(
                datetime.datetime.strptime(
                    scheduled_started_at, '%Y-%m-%dT%H:%M:%S.000Z'
                )
            ).time()
        if scheduled_finished_at:
            scheduled_finished_time = utc_to_local(
                datetime.datetime.strptime(
                    scheduled_finished_at, '%Y-%m-%dT%H:%M:%S.000Z'
                )
            ).time()

        started_date = utc_to_local(
                datetime.datetime.strptime(
                    started_date, '%Y-%m-%dT%H:%M:%S.000Z'
                )
        ).date()

        finished_date = utc_to_local(
                datetime.datetime.strptime(
                    finished_date, '%Y-%m-%dT%H:%M:%S.000Z'
                )
        ).date()

        the_day = datetime.datetime.strptime(
            str(year)+'-'+str(month)+'-'+str(day), '%Y-%m-%d'
        ).date()

        show = False
        frequency = map(int, frequency)

        if started_date <= the_day <= finished_date:
            if CommonTaskFrequency.EVERYDAY in frequency:
                show = True
            elif weekday == 1:
                if CommonTaskFrequency.MONDAY in frequency:
                    show = True
            elif weekday == 2:
                if CommonTaskFrequency.TUESDAY in frequency:
                    show = True
            elif weekday == 3:
                if CommonTaskFrequency.WEDNESDAY in frequency:
                    show = True
            elif weekday == 4:
                if CommonTaskFrequency.THURSDAY in frequency:
                    show = True
            elif weekday == 5:
                if CommonTaskFrequency.FRIDAY in frequency:
                    show = True
            elif weekday == 6:
                if CommonTaskFrequency.SATURDAY in frequency:
                    show = True
            elif weekday == 7:
                if CommonTaskFrequency.SUNDAY in frequency:
                    show = True

        ret = {
            'category_id': category_id,
            'content': content,
            'frequency': frequency,
            'visible_range': visible_range,
            'finish_status': 0,
            'show': show,
            'scheduled_started_at': '',
            'scheduled_finished_at': ''
        }
        if scheduled_started_time or scheduled_started_time == datetime.time(0, 0):
            ret['scheduled_started_at'] = time_to_string(scheduled_started_time.hour*3600+scheduled_started_time.minute*60)
        if scheduled_finished_time or scheduled_finished_time == datetime.time(0, 0):
            ret['scheduled_finished_at'] = time_to_string(scheduled_finished_time.hour*3600+scheduled_finished_time.minute*60)

        commtask = CommonTask.create(
            user_id=current_user.id,
            category_id=category_id,
            content=content,
            visible_range=visible_range,
            started_date=started_date,
            finished_date=finished_date
        )

        for f in frequency:
            CommonTaskFrequency.create(
                commontask_id=commtask.id,
                frequency=f
            )

        delta = (finished_date - started_date).days
        for i in range(0, delta+1):
            TaskRecord.create(
                user_id=current_user.id,
                date=started_date+datetime.timedelta(i),
                weekday=(started_date+datetime.timedelta(i)).isocalendar()[2],
                commontask_id=commtask.id,
                scheduled_started_at=scheduled_started_time,
                scheduled_finished_at=scheduled_finished_time
            )
        ret['id'] = commtask.id

        ret['color'] = commtask.category.color
        self.return_json(ret)


class CreateMonthTask(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        current_user = self.current_user
        data = parse_json(self)

        category_id = int(data.get('category_id'))
        content = data.get('content')
        visible_range = data.get('visible_range')
        year = int(data.get('year'))
        month = int(data.get('month'))

        ret = {
            'category_id': category_id,
            'content': content,
            'visible_range': visible_range,
        }

        monthtask = MonthTask.create(
            user_id=current_user.id,
            year=year,
            month=month,
            category_id=category_id,
            content=content,
            visible_range=visible_range,
        )
        ret['id'] = monthtask.id

        self.return_json(ret)


class CreateWeekTask(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        current_user = self.current_user
        data = parse_json(self)
        category_id = int(data.get('category_id'))
        content = data.get('content')
        visible_range = int(data.get('visible_range'))

        year = int(data.get('year'))
        month = int(data.get('month'))
        week = int(data.get('week'))

        weektask = WeekTask.create(
            user_id=current_user.id,
            year=year,
            month=month,
            weeknumber=week,
            category_id=category_id,
            content=content,
            visible_range=visible_range
        )

        ret = {
            'content': content,
            'visible_range': visible_range,
            'id': weektask.id
        }

        self.return_json(ret)


class CreateCategory(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        data = parse_json(self)
        current_user = self.current_user
        content = data.get('content')
        color = data.get('color')
        level = data.get('level')

        c = Category.create(
            user_id=current_user.id,
            content=content,
            color=color,
            level=level
        )

        self.return_json({
            'id': c.id,
            'content': content,
            'color': color,
            'level': level
        })


class TaskDone(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        current_user = self.current_user
        data = parse_json(self)

        task_id = data.get('task_id')
        type = data.get('type')
        status = data.get('status')

        year = data.get('year')
        month = data.get('month')
        day = data.get('day')

        date = datetime.datetime.strptime(
            str(year)+'-'+str(month)+'-'+str(day),
            '%Y-%m-%d'
        )

        if type == 'month':
            if status:
                MonthTask.update(
                    status=MonthTask.FINISHED
                ).where(
                    # MonthTask.user_id == current_user.id,
                    MonthTask.id == task_id
                ).execute()
            else:
                MonthTask.update(
                    status=MonthTask.UNFINISHED
                ).where(
                    MonthTask.id == task_id
                ).execute()
        elif type == 'week':
            if status:
                WeekTask.update(
                    status=WeekTask.FINISHED
                ).where(
                    WeekTask.id == task_id
                ).execute()
            else:
                WeekTask.update(
                    status=WeekTask.UNFINISHED
                ).where(
                    WeekTask.id == task_id
                ).execute()
        elif type == 'comm':
            if status:
                TaskRecord.update(
                    status=TaskRecord.FINISHED
                ).where(
                    TaskRecord.user_id == current_user.id,
                    TaskRecord.commontask_id == task_id,
                    TaskRecord.date == date.date()
                ).execute()

            else:
                TaskRecord.update(
                    status=TaskRecord.UNFINISHED
                ).where(
                    TaskRecord.user_id == current_user.id,
                    TaskRecord.commontask_id == task_id,
                    TaskRecord.date == date.date()
                ).execute()
        elif type == 'temp':
            if status:
                TemporaryTask.update(
                    status=TemporaryTask.FINISHED
                ).where(
                    TemporaryTask.id == task_id
                ).execute()
            else:
                TemporaryTask.update(
                    status=TemporaryTask.UNFINISHED
                ).where(
                    TemporaryTask.id == task_id
                ).execute()


class Edit(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        data = parse_json(self)
        id = data.get('id')
        type = data.get('type')
        content = data.get('content')
        if type == 'comm':
            CommonTask.update(
                content=content
            ).where(
                CommonTask.id == id
            ).execute()
        if type == 'temp':
            TemporaryTask.update(
                content=content
            ).where(
                TemporaryTask.id == id
            ).execute()
        if type == 'month':
            MonthTask.update(
                content=content
            ).where(
                MonthTask.id == id
            ).execute()
        if type == 'week':
            WeekTask.update(
                content=content
            ).where(
                WeekTask.id == id
            ).execute()
        self.return_json(True)


class Delete(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        data = parse_json(self)
        id = data.get('id')
        type = data.get('type')
        if type == 'comm':
            CommonTask.update(
                status=CommonTask.DELETED
            ).where(
                CommonTask.id == id
            ).execute()
        elif type == 'temp':
            TemporaryTask.update(
                status=TemporaryTask.DELETED
            ).where(
                TemporaryTask.id == id
            ).execute()
        elif type == 'month':
            MonthTask.update(
                status=MonthTask.DELETED
            ).where(
                MonthTask.id == id
            ).execute()
        elif type == 'week':
            WeekTask.update(
                status=WeekTask.DELETED
            ).where(
                WeekTask.id == id
            ).execute()


        # todo: 1.修改新建的handler，前端要传当前指定的年月日周; 2.简化代码 3.month,week,day,weekday转化为直接可用的 4.hasattr


settings = {
    'static_path': os.path.join(os.path.dirname(__file__), 'static'),
    'template_path': os.path.join(os.path.dirname(__file__), 'templates'),
    'cookie_secret': 'p5IbJLCjRlWA+wpi4nLuDeeAwRN5sUbZgPBdJWCaNxU=',
    'login_url': '/login'
}

application = Application([
    (r'/', MainHandler),
    (r'/register', RegisterHandler),
    (r'/login', LoginHandler),
    (r'/logout', LogoutHandler),
    (r'/create_temptask', CreateTemptask),
    (r'/create_commtask', CreateCommtask),
    (r'/create_monthtask', CreateMonthTask),
    (r'/create_weektask', CreateWeekTask),
    (r'/create_category', CreateCategory),
    (r'/taskdone', TaskDone),
    (r'/edit', Edit),
    (r'/delete', Delete)
], **settings)

if __name__ == '__main__':
    application.listen(8000)
    tornado.ioloop.IOLoop.current().start()