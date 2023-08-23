from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from accounts.models import Account
from managements.models import get_default_img_filepath, remove_temp_files


# Question model
def get_question_img_filepath(self, filename):
    remove_temp_files("question_img")
    return "question_img/temp_question_img." + filename.split('.')[-1]


class Question(models.Model):
    created = models.DateTimeField(verbose_name='Created', auto_now_add=True)
    last_modified = models.DateTimeField(verbose_name="Last Modified", auto_now=True)
    account = models.ForeignKey(Account, null=True, blank=True, on_delete=models.SET_NULL, related_name='post_questions')
    image = models.ImageField(verbose_name='Image', max_length=255, null=False, blank=False, default=get_default_img_filepath, upload_to=get_question_img_filepath)
    title = models.CharField(verbose_name="Title", max_length=255, null=False, blank=False)
    description = models.CharField(verbose_name="Description", max_length=7650, null=False, blank=False)
    tags = models.CharField(verbose_name="Tags", max_length=255, null=True, blank=True)

    def __str__(self):
        return str(self.id)

    @property
    def has_accepted_answer(self):
        answers = self.answers.all()
        for answer in answers:
            if answer.is_accepted:
                return answer.is_accepted

    @property
    def get_tags(self):
        tags = self.tags
        tags = tags.replace('#', '')
        return tags

    @property
    def get_tags_list(self):
        tags = self.tags
        tags_list = tags.split(', ')
        return tags_list

    class Meta:
        verbose_name_plural = "Questions"


@receiver(post_save, sender=Question)
def create_question_count(sender, instance, created, **kwargs):
    if created:
        QuestionCounts.objects.create(question=instance)


# Question Count model
class QuestionCounts(models.Model):
    created = models.DateTimeField(verbose_name='Created', auto_now_add=True)
    last_modified = models.DateTimeField(verbose_name="Last Modified", auto_now=True)
    question = models.OneToOneField(Question, null=False, blank=False, on_delete=models.CASCADE, related_name='question_counts')
    votes_count = models.IntegerField(verbose_name="Votes count", null=False, blank=False, default=0)
    voted_by = models.ManyToManyField(Account, through='Vote', blank=True, related_name='question_voted_content')
    views_count = models.IntegerField(verbose_name="Views count", null=False, blank=False, default=0)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = "Question Counts"


# Answer model
def get_answer_img_filepath(self, filename):
    remove_temp_files("answer_img")
    return "answer_img/temp_answer_img." + filename.split('.')[-1]


class Answer(models.Model):
    created = models.DateTimeField(verbose_name='Created', auto_now_add=True)
    last_modified = models.DateTimeField(verbose_name="Last Modified", auto_now=True)
    account = models.ForeignKey(Account, null=True, blank=True, on_delete=models.SET_NULL, related_name='post_answers')
    question = models.ForeignKey(Question, null=False, blank=False, on_delete=models.CASCADE, related_name='answers')
    image = models.ImageField(verbose_name='Image', max_length=255, null=False, blank=False, default=get_default_img_filepath, upload_to=get_answer_img_filepath)
    description = models.CharField(verbose_name="Description", max_length=7650, null=False, blank=False)
    is_accepted = models.BooleanField(verbose_name="Accepted", null=False, blank=False, default=False)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = "Answers"


@receiver(post_save, sender=Answer)
def create_answer_count(sender, instance, created, **kwargs):
    if created:
        AnswerCounts.objects.create(answer=instance)


@receiver(pre_delete, sender=Question)
@receiver(pre_delete, sender=Answer)
def delete_image_file(sender, instance, **kwargs):
    if "default/" not in str(instance.image):
        instance.image.delete(save=False)


# Answer Count model
class AnswerCounts(models.Model):
    created = models.DateTimeField(verbose_name='Created', auto_now_add=True)
    last_modified = models.DateTimeField(verbose_name="Last Modified", auto_now=True)
    answer = models.OneToOneField(Answer, null=False, blank=False, on_delete=models.CASCADE, related_name='answer_counts')
    votes_count = models.IntegerField(verbose_name="Votes count", null=False, blank=False, default=0)
    voted_by = models.ManyToManyField(Account, through='Vote', blank=True, related_name='answer_voted_content')

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = "Answer Counts"


class Vote(models.Model):
    created = models.DateTimeField(verbose_name='Created', auto_now_add=True)
    last_modified = models.DateTimeField(verbose_name="Last Modified", auto_now=True)
    account = models.ForeignKey(Account, null=False, blank=False, on_delete=models.CASCADE)
    question_vote = models.ForeignKey(QuestionCounts, null=True, blank=True, on_delete=models.CASCADE, related_name='question_votes', verbose_name='Question Vote')
    answer_vote = models.ForeignKey(AnswerCounts, null=True, blank=True, on_delete=models.CASCADE, related_name='answer_votes', verbose_name='Answer Vote')
    upvote = models.BooleanField(verbose_name="Upvote", null=False, blank=False, default=False)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = "Votes"


# Problem model
class Problem(models.Model):
    created = models.DateTimeField(verbose_name='Created', auto_now_add=True)
    last_modified = models.DateTimeField(verbose_name="Last Modified", auto_now=True)
    account = models.ForeignKey(Account, null=True, blank=True, on_delete=models.SET_NULL, related_name='chat_problems')
    title = models.CharField(verbose_name="Title", max_length=255, null=False, blank=False)
    tags = models.CharField(verbose_name="Tags", max_length=255, null=True, blank=True)

    def __str__(self):
        return str(self.id)

    @property
    def has_room(self):
        return hasattr(self, 'room') and self.room is not None

    @property
    def get_tags(self):
        tags = self.tags
        tags = tags.replace('#', '')
        return tags

    @property
    def get_tags_list(self):
        tags = self.tags
        tags_list = tags.split(', ')
        return tags_list

    class Meta:
        verbose_name_plural = "Problems"


# Room model
class Room(models.Model):
    created = models.DateTimeField(verbose_name='Created', auto_now_add=True)
    last_modified = models.DateTimeField(verbose_name="Last Modified", auto_now=True)
    problem = models.OneToOneField(Problem, null=True, blank=True, on_delete=models.SET_NULL, related_name='room')
    user = models.ForeignKey(Account, null=True, blank=True, on_delete=models.SET_NULL, related_name='user_rooms')
    expert = models.ForeignKey(Account, null=True, blank=True, on_delete=models.SET_NULL, related_name='expert_rooms')
    ai = models.BooleanField(verbose_name="AI", null=False, blank=False, default=False)
    assigned = models.BooleanField(verbose_name="Assigned", null=False, blank=False, default=False)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = "Rooms"


# Message model
def get_message_img_filepath(self, filename):
    remove_temp_files("message_img")
    return "message_img/temp_message_img." + filename.split('.')[-1]


class Message(models.Model):
    timestamp = models.DateTimeField(verbose_name='Send Time', auto_now_add=True)
    room = models.ForeignKey(Room, null=False, blank=False, on_delete=models.CASCADE, related_name='room_messages')
    account = models.ForeignKey(Account, null=True, blank=True, on_delete=models.SET_NULL, related_name='account_messages')
    image = models.ImageField(verbose_name='Image', max_length=255, null=False, blank=False, default=get_default_img_filepath, upload_to=get_message_img_filepath)
    content = models.TextField(verbose_name="Content", null=True, blank=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = "Messages"


'''
# Contact model
class Contact(models.Model):
    created = models.DateTimeField(verbose_name='Created', auto_now_add=True)
    last_modified = models.DateTimeField(verbose_name="Last Modified", auto_now=True)
    account = models.ForeignKey(Account, null=True, blank=True, on_delete=models.SET_NULL, related_name='user_contacts')
    name = models.CharField(verbose_name="Name", max_length=255, null=False, blank=False)
    subject = models.CharField(verbose_name="Subject", max_length=255, null=False, blank=False)
    email = models.CharField(verbose_name="Email", max_length=255, null=False, blank=False)
    phone = models.CharField(verbose_name="Phone", max_length=255, null=False, blank=False)
    message = models.TextField(verbose_name="Message", null=True, blank=True)
    contacted = models.BooleanField(verbose_name="Contacted", null=False, blank=False, default=False)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = "Contacts"
'''
