from flask_security import current_user
from flask import redirect,url_for
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView



#next classes are child classes of ModelView
#creating respective view for the above model
class AdminMixin():
    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self,name,**kwargs):
        return redirect(url_for('index'))

class AdminView(AdminMixin,ModelView):
    pass


class HomeAdminView(AdminMixin,AdminIndexView):
    pass
