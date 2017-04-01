from functools import partialmethod

base = 'http://lms.nthu.edu.tw'


class CourseRoute():

    rules = {
        'forum': 'forumlist',
        'homework': 'hwlist',
        'document': 'doclist',
        'forum_detail': 'forumlist',
        'homework_detail': 'hw',
        'document_detail': 'doc',
    }

    rule_key = {
        'forum_detail': 'page',
        'homework_detail': 'hw',
        'document_detail': 'cid',
    }

    def __init__(self, course_id):
        self.base = '{}/course.php?courseID={}'.format(base, course_id)

    def gen_rule(self, func, uid=None):
        if uid:
            func += '_detail'
        path = '%s&f=%s' % (self.base, self.rules[func])
        if uid:
            path += '&{}={}'.format(self.rule_key[func], uid)
        return path

    homework = partialmethod(gen_rule, 'homework')
    document = partialmethod(gen_rule, 'document')
    forum = partialmethod(gen_rule, 'forum')


class Routes():

    rules = {
        'home': 'home.php',
        'profile': 'home/profile.php',
        'attach': 'sys/read_attach.php?id={attach_id}',
        'login_submit': 'sys/lib/ajax/login_submit.php',
        'post': 'sys/lib/ajax/post.php'
    }

    def __init__(self):
        for rule, value in self.rules.items():
            setattr(self, rule, '%s/%s' % (base, value))
        self.course = CourseRoute


route = Routes()
