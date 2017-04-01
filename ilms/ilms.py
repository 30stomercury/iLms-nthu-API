import os

from ilms import parser
from ilms.route import route
from ilms.request import RequestProxyer
from ilms.utils import ProgressBar


class Homework():

    def __init__(self, raw, callee):
        self.raw = raw
        self.callee = callee
        self.homework_id = raw['id']

    def detail(self, download=False):
        resp = self.callee.callee.requests.get(
            route.course(self.callee.course_id).homework(self.homework_id))
        if download:
            pass
        return parser.parse_homework_detail(resp.text)


class Material():

    def __init__(self, raw, callee):
        self.raw = raw
        self.callee = callee
        self.material_id = raw['id']

    def detail(self, download=False):
        resp = self.callee.callee.requests.get(
            route.course(self.callee.course_id).document(self.material_id))
        if download:
            pass
        return parser.parse_material_detail(resp.text)


class Course():

    def __init__(self, raw, callee):
        self.raw = raw
        self.callee = callee
        self.course_id = raw['id']

    def get_homeworks(self):
        resp = self.callee.requests.get(route.course(self.course_id).homework())
        self.homeworks = [
            Homework(homework, callee=self)
            for homework in parser.parse_homework_list(resp.text).result
        ]
        return self.homeworks

    def get_materials(self, download=False):
        resp = self.callee.requests.get(route.course(self.course_id).document())
        self.materials = [
            Material(material, callee=self)
            for material in parser.parse_material_list(resp.text).result
        ]
        return self.materials

    def get_forum_list(self, page=1):
        resp = self.callee.requests.get(
            route.course(self.course_id).forum() + '&page=%d' % page)
        return parser.parse_forum_list(resp.text)


class System():

    def __init__(self, user):
        self.session = user.session
        self.requests = RequestProxyer(self.session)
        self.profile = None
        self.courses = None

    def get_profile(self):
        resp = self.requests.get(route.profile)
        self.profile = parser.parse_profile(resp.text)
        return self.profile

    def get_courses(self):
        resp = self.requests.get(route.home)
        self.courses = [
            Course(course, callee=self)
            for course in parser.parse_course_list(resp.text).result]
        return self.courses

    def get_post_detail(self, post_id):
        resp = self.requests.post(route.post, data={'id': post_id})
        return parser.parse_post_detail(resp.json())

    def download(self, attach_id, folder='download'):
        return download(self.requests, attach_id, folder)


def download(sess, attach_id, folder='download'):
    resp = sess.get(route.attach.format(attach_id=attach_id), stream=True)

    filename = resp.headers['content-disposition'].split("'")[-1]
    filesize = int(resp.headers['content-length'])

    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, filename)

    chunk_size = 1024
    progress = ProgressBar()
    progress.max = filesize // chunk_size
    with open(path, 'wb') as f:
        for chunk in resp.iter_content(chunk_size=chunk_size):
            if chunk:
                f.write(chunk)
            progress.next()
    progress.finish()
    return filename
