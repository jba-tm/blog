# Generated by Django 3.1.2 on 2020-10-24 14:32

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.contrib.taggit
import modelcluster.fields
import wagtail.core.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('wagtailimages', '0022_uploadedimage'),
        ('wagtailcore', '0052_pagelogentry'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContentCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Content category',
                'verbose_name_plural': 'Content categories',
                'ordering': ['name'],
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='ContentIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
            ],
            options={
                'verbose_name': 'Content index page',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='ContentPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('body', wagtail.core.fields.RichTextField(help_text='Content body', verbose_name='Body')),
                ('category', modelcluster.fields.ParentalKey(help_text='Content category', null=True, on_delete=django.db.models.deletion.SET_NULL, to='content.contentcategory', verbose_name='Category')),
            ],
            options={
                'verbose_name': 'Content page',
                'verbose_name_plural': 'Content pages',
                'permissions': (('import_content', 'Can import content'),),
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='ContentTagIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
            ],
            options={
                'verbose_name': 'Content tag index page',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='ContentPageTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_object', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='tagged_items', to='content.contentpage')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='content_contentpagetag_items', to='taggit.tag')),
            ],
            options={
                'verbose_name': 'Content page tag',
                'verbose_name_plural': 'Content page tags',
            },
        ),
        migrations.CreateModel(
            name='ContentPageGalleryImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('caption', models.CharField(blank=True, max_length=250)),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='wagtailimages.image')),
                ('page', modelcluster.fields.ParentalKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='gallery_images', to='content.contentpage')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='contentpage',
            name='tags',
            field=modelcluster.contrib.taggit.ClusterTaggableManager(blank=True, help_text='A comma-separated list of tags.', through='content.ContentPageTag', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
