from project.app_config.database import app
from project.app_notification.notification import Notification


class NotificationService:
    def __init__(self, database):
        self.__database = database
        app.logger.info(" NotificationService  [init]")

    def notifications_count(self):
        return Notification.notifications_count()

    def notifications_find(self):
        return Notification.notifications_find()
