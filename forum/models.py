from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from taggit.managers import TaggableManager

def user_dir(instace, filename):
    return f'{instance.user.id}/{filename}'

def project_code_dir(instace, filename):
    return f'{instance.project.id}/code/{filename}'

def project_schematics_dir(instace, filename):
    return f'{instance.project.id}/schematics/{filename}'


def project_gallery_dir(instace, filename):
    return f'{instance.project.id}/gallery/{filename}'


class ProjectManager(models.Manager):

    def get_queryset(self):
        return Project.objects.prefetch_related('collaborators')


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    display_picture = models.ImageField(upload_to=user_dir)
    birth_date = models.DateField(null=True, blank=True)
    github = models.TextField(max_length=50, blank=True)
    website = models.TextField(max_length=150, blank=True)

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
    

class Project(models.Model):
    title = models.CharField(max_length=200, blank=False)
    description = models.TextField(max_length=1000, blank=False)
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    collaborators = models.ManyToManyField(User, related_name='collaborators')
    gallery = models.OneToOneField('Gallery', blank=True, on_delete=models.CASCADE)
    stars = models.IntegerField(default=0)
    tags = TaggableManager(blank=False)
    github = models.CharField(max_length=50,blank=True)
    website = models.CharField(max_length=150,blank=True)
    funding = models.CharField(max_length=150,blank=True)

    objects = ProjectManager

    def __str__(self):
        return self.title



class CodeFile(models.Model):
    code_file = models.FileField(upload_to=project_code_dir)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='codefiles') 
    is_public = models.BooleanField(default=True)


class SchematicsFile(models.Model):
    schematic_file = models.FileField(upload_to=project_schematics_dir)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='schematicsfiles') 
    is_public = models.BooleanField(default=True)


class Gallery(models.Model):
    title = models.CharField(max_length=200, blank=False)
    is_public = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    @receiver(post_save, sender=Project)
    def create_gallery(sender, instance, created, **kwargs):
        if created:
            Gallery.objects.create(title=instance.title)

    @receiver(post_save, sender=Project)
    def save_gallery(sender, instance, **kwargs):
        instance.gallery.save()


class Image(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to=project_gallery_dir)
    slug = models.SlugField()
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, related_name='gallery_image')

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        pass
        
