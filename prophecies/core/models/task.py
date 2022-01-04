from actstream import action
from colorfield.fields import ColorField
from django.contrib.auth.models import User
from django.db import models
from django.db.models import signals
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from prophecies.core.models.project import Project
from prophecies.core.models.choice_group import ChoiceGroup
from prophecies.core.contrib.colors import hex_scale_brightness


class StatusType(models.TextChoices):
    OPEN = 'OPEN', _('Open')
    CLOSED = 'CLOSED', _('Closed')
    LOCKED = 'LOCKED', _('Locked')


class Task(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks", help_text="Project this task belong to")
    checkers = models.ManyToManyField(User, through='TaskChecker', through_fields=('task', 'checker'), verbose_name="User in charge of checking this task's data", related_name='task')
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')
    rounds = models.PositiveIntegerField(default=3, verbose_name="Number of rounds")
    automatic_round_attributions = models.BooleanField(default=False, verbose_name="Attribute rounds (if not checked, all checkers will participate in all rounds)")
    allow_multiple_checks = models.BooleanField(default=False, verbose_name="Allow checkers to check several time the same item")    
    allow_items_addition = models.BooleanField(default=False, verbose_name="Allow checker to add items (not implemented yet)")
    priority = models.PositiveIntegerField(default=1, verbose_name="Priority")
    choice_group = models.ForeignKey(ChoiceGroup, verbose_name="Choices", on_delete=models.SET_NULL, null=True, blank=True)
    color = ColorField(default='#31807D')
    record_link_template = models.CharField(max_length=1000, null=True, blank=True, verbose_name="Record link template", help_text="A link template to build a link for each task record. Task record can override this value with their own link")
    embeddable_links = models.BooleanField(default=False, verbose_name="Allow end-users to preview links within an iframe (targeted website must allow it)")
    embeddable_record_link_template = models.CharField(max_length=1000, null=True, blank=True, verbose_name="Embeddable record link template", help_text="An optional alternative link template to use within the link preview.")
    status = models.CharField(blank=True, choices=StatusType.choices, default=StatusType.OPEN, max_length=6, help_text="Status of the task. Set to closed or locked will prevent any update of the records.")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


    def progress_by_round(self, **task_record_review_filter):
        from prophecies.core.models.task_record_review import TaskRecordReview
        filter = dict(task_record__task=self, **task_record_review_filter)
        progress = TaskRecordReview.objects.progress_by_round(**filter)
        # Get all task's rounds to only display the progress by existing rounds
        rounds = range(1, self.rounds + 1)
        return { round: progress.get(round, 0) for round in rounds }

    def stats_by_round(self, **task_record_review_filter):   
        from prophecies.core.models.task_record_review import TaskRecordReview
        filter = dict(task_record__task=self, **task_record_review_filter)
        stats = TaskRecordReview.objects.stats_by_round(**filter)
        # Get all task's rounds to only display the progress by existing rounds
        rounds = range(1, self.rounds + 1)
        return { round: stats.get(round, 0) for round in rounds }

    def open(self):
        self.status = StatusType.OPEN
        self.save()

    def close(self):
        self.status = StatusType.CLOSED
        self.save()

    def lock(self):
        self.status = StatusType.LOCKED
        self.save()

    @property
    def is_open(self):
        return self.status == StatusType.OPEN

    @property
    def is_open_changed(self):
        if self.pk is not None:
            instance = Task.objects.get(pk=self.pk)
            return self.is_open != instance.is_open
        return False

    @property
    def is_closed(self):
        return self.status == StatusType.CLOSED

    @property
    def is_closed_changed(self):
        if self.pk is not None:
            instance = Task.objects.get(pk=self.pk)
            return self.is_closed != instance.is_closed
        return False

    @property
    def is_locked(self):
        return self.status == StatusType.LOCKED

    @property
    def is_locked_changed(self):
        if self.pk is not None:
            instance = Task.objects.get(pk=self.pk)
            return self.is_locked != instance.is_locked
        return False

    @cached_property
    def progress(self):
        from prophecies.core.models.task_record_review import TaskRecordReview, StatusType as st
        tasks_reviews = TaskRecordReview.objects.filter(task_record__task_id=self.id)
        done_reviews= tasks_reviews.filter(status=st.DONE)
        all_reviews = len(tasks_reviews)
        done_reviews = len(done_reviews)
        return 100 if all_reviews == 0 else done_reviews / all_reviews * 100

    @cached_property
    def colors(self):
        """
        Generate 3 colors tones based on the `color` attribute
        """
        scales = [0.75, 1.0, 1.25]
        return tuple(hex_scale_brightness(self.color, s) for s in scales)

    @staticmethod
    def signal_log_task_locked(sender, instance, **kwargs):
        if instance.is_locked_changed and instance.is_locked:
            if instance.creator:
                action.send(instance.creator, verb='locked', target=instance)

    @staticmethod
    def signal_log_task_closed(sender, instance, **kwargs):
        if instance.is_closed_changed and instance.is_closed:
            if instance.creator:
                action.send(instance.creator, verb='closed', target=instance)

    @staticmethod
    def signal_log_task_open(sender, instance, **kwargs):
        if instance.is_open_changed and instance.is_open:
            if instance.creator:
                action.send(instance.creator, verb='open', target=instance)


signals.pre_save.connect(Task.signal_log_task_locked, sender=Task)
signals.pre_save.connect(Task.signal_log_task_closed, sender=Task)
signals.pre_save.connect(Task.signal_log_task_open, sender=Task)
